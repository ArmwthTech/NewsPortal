from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField('Рейтинг', default=0)

    def update_rating(self):
        postRat = sum([3 * p.rating for p in Post.objects.filter(author=self)])
        commRat = sum([c.rating for c in Comment.objects.filter(user=self.user)])
        postCommRat = sum([c.rating for c in Comment.objects.filter(post__in=Post.objects.filter(author=self))])
        self.rating = postRat + commRat + postCommRat
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User,related_name='categories',verbose_name='Подписчики')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    TYPES = (
        ('N', 'News'),
        ('A', 'Article'),
    )
    type = models.CharField(max_length=20, choices=TYPES, verbose_name='Тип поста')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    categories = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категории')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def __str__(self):
        return self.title

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Post)
def send_new_article_notification(sender, instance, created, **kwargs):
    if created:
        subscriptions = Subscription.objects.filter(category=instance.category)
        for subscription in subscriptions:
            send_mail(
                'New Article in {}'.format(instance.category.name),
                'A new article "{}" has been added. Read it here: {}'.format(instance.title, instance.get_absolute_url()),
                'from@example.com',
                [subscription.user.email],
                fail_silently=False,
            )