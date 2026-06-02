from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User


@shared_task
def send_welcome_email_task(user_id):
    try:
        user = User.objects.get(id=user_id)

        html_content = render_to_string('email/welcome_email.html', {
            'username': user.username,
            'email': user.email,
        })

        send_mail(
            subject='Добро пожаловать на News Portal!',
            message=f'Привет, {user.username}! Спасибо за регистрацию.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_content,
        )

        return f"Приветственное письмо отправлено {user.email}"

    except User.DoesNotExist:
        return f"Пользователь {user_id} не найден"