from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


def send_order_confirmation_email(user_email, order_id, items_summary, total_sum, delivery_address):
    message = (
        f"Ваш заказ: {order_id} принят.\n"
        f"Состав заказа:\n{items_summary}\n"
        f"Итого: {total_sum} руб.\n"
        f"Адрес доставки: {delivery_address}\n"
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
        f"Новая накладная для исполнения заказа: {order_id}\n"
        f"Клиент: {user_email}\n"
        f"Состав заказа: \n{items_summary}\n"
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


@shared_task
def send_order_confirmation_email_task(*args, **kwargs):
    send_order_confirmation_email(*args, **kwargs)


@shared_task
def send_invoice_to_admin_task(*args, **kwargs):
    send_invoice_to_admin(*args, **kwargs)
