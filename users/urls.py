"""URL-шаблоны для аутентификации, регистрации и управления контактами."""

from django.urls import path


from .views import RegisterAccountView, ConfirmAccountView, LoginAccountView, AccountDetailsView, \
    ContactDetailView

urlpatterns = [
    path('register', RegisterAccountView.as_view()),
    path('register/confirm', ConfirmAccountView.as_view()),
    path('login', LoginAccountView.as_view()),
    path('details', AccountDetailsView.as_view()),
    path('contact', ContactDetailView.as_view()),
]
