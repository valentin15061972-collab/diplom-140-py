from rest_framework import serializers
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id', 'name']


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ['parameter', 'value']


class ProductInfoSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    parameters = ProductParameterSerializer(many=True, read_only=True)

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'quantity', 'price', 'parameters',]


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    shops = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'shops']

    def get_shops(self, obj):
        product_infos = ProductInfo.objects.filter(product=obj).select_related('shop')
        return [{'shop': pi.shop.name, 'price': str(pi.price), 'quantity': pi.quantity,} for pi in product_infos]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    product_info = ProductInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'product_info']