from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .models import Post, Category


@shared_task
def send_not_about_new_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        categories = post.category.all()
        emails = set()
        for category in categories:
            for subscriber in category.subscribers.all():
                emails.add(subscriber.email)

        if not emails:
            return f"Нет подписчиков для поста {post_id}"

        html_content = render_to_string('email/new_post_not.html', {
            'post': post,
            'username': post.author.user.username,
        })

        msg = EmailMultiAlternatives(
            subject=f'Новый пост: {post.title}',
            body=post.text[:200],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=list(emails)
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return f"Уведомления отправлены {len(emails)} подписчикам"

    except Post.DoesNotExist:
        return f"Пост {post_id} не найден"


@shared_task
def send_week_news_task():
    week_ago = timezone.now() - timedelta(days=7)
    categories = Category.objects.all()

    sent_count = 0

    for category in categories:
        new_posts = category.post_set.filter(time_in__gte=week_ago).order_by('-time_in')

        if not new_posts.exists():
            continue

        subscribers = category.subscribers.all()
        if not subscribers.exists():
            continue

        emails = [subscriber.email for subscriber in subscribers]

        html_content = render_to_string('email/week_news.html', {
            'category': category,
            'posts': new_posts,
            'week_ago': week_ago,
        })

        msg = EmailMultiAlternatives(
            subject=f'Новые посты в категории "{category.name}" за неделю',
            body=f'В категории "{category.name}" появилось {new_posts.count()} новых постов.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=emails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        sent_count += len(emails)

    return f"Еженедельная рассылка отправлена {sent_count} подписчикам"