from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .tasks import send_not_about_new_post
from sign.tasks import send_welcome_email_task



@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if not created:
        return
    categories = instance.category.all()
    subscribers_emails = set()
    for category in categories:
        for subscriber in category.subscribers.all():
            subscribers_emails.add(subscriber.email)
    if not subscribers_emails:
        return
    html_content = render_to_string(
        'email/new_post_not.html',
        {
            'post': instance,
            'username': instance.author.user.username,
            'preview_text': instance.text[:100],
        }
    )

    subject = f'Новый пост: {instance.title}'
    msg = EmailMultiAlternatives(
        subject=subject,
        body=instance.text[:200],
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscribers_emails)
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()


def send_week_news():
    week_ago = timezone.now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        new_posts = category.post_set.filter(time_in__gte=week_ago).order_by('-time_in')

        if not new_posts.exists():
            continue

        subscribers = category.subscribers.all()

        if not subscribers.exists():
            continue

        emails = [subscriber.email for subscriber in subscribers]

        html_content = render_to_string(
            'email/week_news.html',
            {
                'category': category,
                'posts': new_posts,
                'week_ago': week_ago,
            }
        )

        subject = f'Новые статьи в категории "{category.name}" за неделю'

        msg = EmailMultiAlternatives(
            subject=subject,
            body=f'В категории "{category.name}" появилось {new_posts.count()} новых статей.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=emails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string(
            'email/welcome.html',
            {
                'username': instance.username,
                'email': instance.email,
            }
        )

        send_mail(
            subject='Добро пожаловать на News Portal!',
            message=f'Привет, {instance.username}! Спасибо за регистрацию, приятного чтения!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=html_content,
        )

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        send_not_about_new_post.delay(instance.id)


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_welcome_email_task.delay(instance.id)