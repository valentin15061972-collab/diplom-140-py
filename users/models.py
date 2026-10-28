from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):

    USER_TYPE = [('buyer', 'покупатель'), ('shop', 'магазин-поставщик')]

    email = models.EmailField(unique=True)
    company = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=10, choices=USER_TYPE, default='buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.username} ({self.email})'


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=15)
    apartment = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house}, {self.phone}'


class ConfirmEmailToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirm_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_token(cls, user):
        token = uuid.uuid4().hex
        obj = cls.objects.create(user=user, token=token)
        return obj

    def __str__(self):
        return f'{self.user.email} — {self.token[:8]}...'