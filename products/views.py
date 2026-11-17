"""Представления для работы с товарами, магазинами и категориями."""
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .imports import import_from_uploaded_file
from .models import Shop, Category, Product
from .serializers import ShopSerializer, CategorySerializer, ProductListSerializer, ProductDetailSerializer



class ShopListView(ListAPIView):
    """Список магазинов."""
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]


class CategoryListView(ListAPIView):
    """Список категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductListView(ListAPIView):
    """Список товаров с фильтрацией."""
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['category', 'category__shops']
    search_fields = ['name', 'category__name']
    ordering_fields = ['name', 'category__name']

    def get_queryset(self):
        queryset = Product.objects.select_related('category').prefetch_related('product_info__shop')
        shop_id = self.request.query_params.get('shop')
        if shop_id:
            queryset = queryset.filter(product_info__shop_id=shop_id).distinct()
        return queryset


class ProductDetailView(RetrieveAPIView):
    """Детальная информация о товаре."""
    queryset = Product.objects.prefetch_related('product_info__parameters', 'product_info__shop')
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]


class ProductImportView(APIView):
    """Импорт товаров из файла для магазинов-поставщиков."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return Response({'error': 'Импорт доступен только для магазинов-поставщиков.'}, status=status.HTTP_403_FORBIDDEN,)
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'Файл не передан.'}, status=status.HTTP_400_BAD_REQUEST)
        shop_name = None  # Определяем имя магазина по пользователю
        if hasattr(request.user, 'shop') and request.user.shop:
            shop_name = request.user.shop.name
        try:
            result = import_from_uploaded_file(file_obj, shop_name)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'status': 'ok',
            'created': result['created'],
            'updated': result['updated'],
            'errors': result['errors'],
        })




