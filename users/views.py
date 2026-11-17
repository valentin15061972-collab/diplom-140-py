"""Представления для аутентификации, регистрации и управления контактами."""

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from .models import User, Contact, ConfirmEmailToken
from .serializers import UserSerializer, UserRegisterSerializer, ContactSerializer, LoginSerializer


class RegisterAccountView(APIView):
    """Регистрация нового пользователя."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token_obj = ConfirmEmailToken.generate_token(user)
            # Отправляем email с токеном подтверждения
            send_mail(
                subject='Подтверждение регистрации',
                message=f'Ваш токен подтверждения: {token_obj.token}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            return Response({
                'status': 'ok',
                'message': 'Письмо отправлено на ваш email.',
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmAccountView(APIView):
    """Подтверждение регистрации по токену."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        token = request.data.get('token')
        if not email or not token:
            return Response({'error': 'Необходимо указать email и token.'}, status=status.HTTP_400_BAD_REQUEST,)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_obj = ConfirmEmailToken.objects.get(user=user, token=token)
        except ConfirmEmailToken.DoesNotExist:
            return Response({'error': 'Неверный токен.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        token_obj.delete()
        return Response({'status': 'ok', 'message': 'Регистрация подтверждена.'})


class LoginAccountView(APIView):
    """Авторизация пользователя (получение токена)."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
            )
            if user and user.is_active:
                token = Token.objects.get_or_create(user=user)
                return Response({
                    'status': 'ok',
                    'token': token,
                })
            return Response(
                {'error': 'Неверный email или пароль, либо аккаунт не активирован.'},
                      status=status.HTTP_400_BAD_REQUEST,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailsView(RetrieveUpdateAPIView):
    """Получение и обновление данных пользователя."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ContactViewSet(ModelViewSet):
    """Управление адресами доставки."""
    queryset = Contact.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
