from django.urls import path
from rest_framework import routers

from .views import RegisterAccountView, ConfirmAccountView, LoginAccountView, AccountDetailsView, \
    ContactViewSet

router = routers.DefaultRouter()
router.register('contacts', ContactViewSet)

urlpatterns = [
    path('register', RegisterAccountView.as_view()),
    path('register/confirm', ConfirmAccountView.as_view()),
    path('login', LoginAccountView.as_view()),
    path('details', AccountDetailsView.as_view()),
] + router.urls
