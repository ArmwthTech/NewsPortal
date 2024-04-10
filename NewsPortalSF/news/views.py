from django.shortcuts import render
from .models import Post
from django.views.generic import DetailView, UpdateView, DeleteView


def news_home(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'news/news_home.html', {'posts': posts})


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post_detail'


