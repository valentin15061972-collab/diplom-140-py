from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import ContactSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_info.product.name', read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    price = serializers.DecimalField(source='product_info.price', max_digits=10, decimal_places=2, read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'shop_name', 'price', 'quantity', 'total_cost']
        read_only_fields = ['id']

    def get_total_cost(self, obj):
        return str(obj.total_cost)


class OrderSerializer(serializers.ModelSerializer):
    total_sum = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'total_sum', 'total_quantity',]
        read_only_fields = ['id', 'created_at', 'status']

    def get_total_sum(self, obj):
        return str(obj.total_sum)

    def get_total_quantity(self, obj):
        return obj.total_quantity


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    contact = ContactSerializer(read_only=True)
    total_sum = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'contact', 'items', 'total_sum', 'total_quantity',]

    def get_total_sum(self, obj):
        return str(obj.total_sum)

    def get_total_quantity(self, obj):
        return obj.total_quantity


class BasketItemSerializer(serializers.Serializer):
    product_info_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(min_value=1, default=1)


class OrderConfirmSerializer(serializers.Serializer):
    contact_id = serializers.IntegerField(required=True)


class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)