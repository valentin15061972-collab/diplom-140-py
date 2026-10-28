from django.db import models
from users.models import User


class Shop(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='shop')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    shops = models.ManyToManyField(Shop, related_name='categories', blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    @property
    def shops_with_product(self):
        return list(Shop.objects.filter(product_info__product=self).distinct())


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_info')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='product_info')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} — {self.shop.name} — {self.price}'

    @property
    def total_cost(self):
        return self.price * self.quantity

class Parameter(models.Model):
        name = models.CharField(max_length=50)

        def __str__(self):
            return self.name

class ProductParameter(models.Model):
        product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='parameters')
        parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='product_parameters')
        value = models.CharField(max_length=100)

        def __str__(self):
            return f'{self.parameter.name}: {self.value}'


