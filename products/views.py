from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Shop, Category, Product
from .serializers import ShopSerializer, CategorySerializer, ProductListSerializer, ProductDetailSerializer



class ShopListView(ListAPIView):
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductListView(ListAPIView):
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
    queryset = Product.objects.prefetch_related('product_info__parameters', 'product_info__shop')
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]



