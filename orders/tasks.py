from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(user_email, order_id, items_summary, total_sum, delivery_address):
    message = (
        f"Ваш заказ: {order_id} принят.\n\n"
        f"Состав заказа:\n{items_summary}\n\n"
        f"Итого: {total_sum} руб.\n\n"
        f"Адрес доставки: {delivery_address}\n\n"
    )
    send_mail(
        subject=f'Подтверждение заказа: {order_id}',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=True,
    )


def send_invoice_to_admin(order_id, user_email, items_summary, total_sum, delivery_address):
    admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
    message = (
        f"Новая накладная для исполнения заказа: {order_id}\n\n"
        f"Клиент: {user_email}\n"
        f"Состав заказа: \n{items_summary}\n\n"
        f"Итого: {total_sum} руб.\n"
        f"Адрес доставки: {delivery_address}\n"
    )
    send_mail(
        subject=f'Накладная к заказу: {order_id}',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin_email],
        fail_silently=True,
    )

