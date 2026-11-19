"""URL-шаблоны для работы с заказами и корзиной."""

from django.urls import path
from .views import BasketView, OrderListView, OrderDetailView, OrderStatusView



urlpatterns = [
    path('basket', BasketView.as_view()),
    path('list_orders', OrderListView.as_view()),
    path('<int:pk>', OrderDetailView.as_view()),
    path('<int:pk>/status', OrderStatusView.as_view()),
]
