from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from users.models import Contact
from products.models import ProductInfo
from .models import Order, OrderItem
from .tasks import send_order_confirmation_email, send_invoice_to_admin
from .serializers import (OrderSerializer, OrderDetailSerializer, BasketItemSerializer,
                          OrderConfirmSerializer, OrderStatusSerializer,)


class BasketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = self.get_or_create_basket(request.user)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BasketItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        product_info_id = serializer.validated_data['product_info_id']
        quantity = serializer.validated_data['quantity']
        try:
            product_info = ProductInfo.objects.select_related('shop', 'product').get(id=product_info_id)
        except ProductInfo.DoesNotExist:
            return Response({'error': 'Товар не найден.'}, status=404)
        if product_info.quantity < quantity:
            return Response({'error': f'Недостаточно товара. Доступно: {product_info.quantity}.'}, status=400,)
        order = self.get_or_create_basket(request.user)
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product_info=product_info,
            shop=product_info.shop,
            defaults={'quantity': quantity},
        )
        if not created:
            order_item.quantity += quantity
            order_item.save()

        return Response({'status': 'ok', 'message': 'Товар добавлен в корзину.'})

    def delete(self, request, *args, **kwargs):
        serializer = BasketItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        product_info_id = serializer.validated_data['product_info_id']
        order = self.get_or_create_basket(request.user)
        try:
            order_item = OrderItem.objects.get(order=order, product_info_id=product_info_id,)
        except OrderItem.DoesNotExist:
            return Response({'error': 'Товар не найден в корзине.'}, status=404)
        quantity_to_remove = serializer.validated_data['quantity']
        if order_item.quantity <= quantity_to_remove:
            order_item.delete()
        else:
            order_item.quantity -= quantity_to_remove
            order_item.save()
        return Response({'status': 'ok', 'message': 'Товар удалён из корзины.'})

    def get_or_create_basket(self, user):
        order, _ = Order.objects.get_or_create(user=user, status='new',)
        return order


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).exclude(status='new').prefetch_related('items')

    def post(self, request, *args, **kwargs):
        serializer = OrderConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        contact_id = serializer.validated_data['contact_id']
        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
        except Contact.DoesNotExist:
            return Response({'error': 'Адрес доставки не найден.'}, status=404)
        try:
            order = Order.objects.get(user=request.user, status='new')
        except Order.DoesNotExist:
            return Response({'error': 'Корзина пуста.'}, status=400)
        if not order.items.exists():
            return Response({'error': 'Корзина пуста.'}, status=400)
        with transaction.atomic():
            order.confirm(contact)
        items_summary = self._build_items_summary(order)
        total_sum = str(order.total_sum)
        delivery_address = f'{contact.city}, {contact.street}, {contact.house}'
        send_order_confirmation_email(
            user_email=request.user.email,
            order_id=order.id,
            items_summary=items_summary,
            total_sum=total_sum,
            delivery_address=delivery_address,
        )
        send_invoice_to_admin(
            order_id=order.id,
            user_email=request.user.email,
            items_summary=items_summary,
            total_sum=total_sum,
            delivery_address=delivery_address,
        )
        return Response({
            'status': 'ok',
            'message': 'Заказ подтверждён.',
            'order_id': order.id,
        })

    def _build_items_summary(self, order):
        lines = []
        for item in order.items.all():
            lines.append(
                f'  — {item.product_info.product.name} '
                f'({item.shop.name}): {item.quantity} шт. '
                f'по {item.product_info.price} руб.'
            )
        return '\n'.join(lines)


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product_info__product')


class OrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        if request.user.type != 'shop' and not request.user.is_staff:
            return Response(
                {'error': 'Изменение статуса доступно только магазинам.'},
                status=403,
            )
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден.'}, status=404)

        serializer = OrderStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        order.status = serializer.validated_data['status']
        order.save()

        return Response({
            'status': 'ok',
            'order_id': order.id,
            'new_status': order.status,
        })

