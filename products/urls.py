from django.urls import path
from .views import ShopListView, CategoryListView, ProductListView, ProductDetailView, ProductImportView



urlpatterns = [
    path('shops', ShopListView.as_view()),
    path('categories', CategoryListView.as_view()),
    path('products', ProductListView.as_view()),
    path('<int:pk>', ProductDetailView.as_view()),
    path('import', ProductImportView.as_view()),
]
