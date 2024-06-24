from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category
from django.contrib.auth.models import User


@shared_task
def send_notification(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.category.all()
    subscribers = set()
    for category in categories:
        subscribers.update(category.subscribers.all())

    for subscriber in subscribers:
        send_mail(
            subject=f'Новая статья в категории {", ".join(category.name for category in categories)}',
            message=f'Здравствуйте, {subscriber.username}!\n\nНовая статья "{post.title}" была опубликована в категории, на которую вы подписаны.',
            from_email='your@email.com',
            recipient_list=[subscriber.email],
        )


@shared_task
def weekly_newsletter():
    last_week = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    subscribers = User.objects.filter(subscriptions__isnull=False).distinct()

    for subscriber in subscribers:
        subscribed_categories = subscriber.subscriptions.all()
        relevant_posts = posts.filter(category__in=subscribed_categories)

        if relevant_posts:
            send_mail(
                subject='Еженедельная рассылка новостей',
                message=f'Здравствуйте, {subscriber.username}!\n\nВот список новых статей за прошедшую неделю:\n\n' +
                        '\n'.join(f'- {post.title}' for post in relevant_posts),
                from_email='your@email.com',
                recipient_list=[subscriber.email],
            )