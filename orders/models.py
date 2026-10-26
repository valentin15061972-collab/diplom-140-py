from django.core.validators import MinValueValidator
from django.db import models

from products.models import Shop, ProductInfo
from users.models import User, Contact


class Order(models.Model):

    STATUS_CHOICES = [('new', 'новый'), ('confirmed', 'подтверждён'), ('sent', 'отправлен'),
                      ('delivered', 'доставлен'), ('canceled', 'отменён')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders')

    def __str__(self):
        return f'Заказ #{self.id} — {self.user.email} — {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='order_items')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='order_shops')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return f'{self.product_info.product.name} x {self.quantity}'
