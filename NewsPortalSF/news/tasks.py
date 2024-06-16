
from celery import shared_task
from django.core.mail import send_mail
from news.models import Subscription, Post
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_weekly_newsletter():
    one_week_ago = timezone.now() - timedelta(days=7)
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        articles = Post.objects.filter(category=subscription.category, created_at__gte=one_week_ago)
        if articles:
            article_list = "\n".join(["{}: {}".format(article.title, article.get_absolute_url()) for article in articles])
            send_mail(
                'Weekly Newsletter for {}'.format(subscription.category.name),
                'Here are the new articles from the past week:\n\n{}'.format(article_list),
                'from@example.com',
                [subscription.user.email],
                fail_silently=False,
            )