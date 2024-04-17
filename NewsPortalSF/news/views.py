from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Post
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.core.paginator import Paginator
from django.db.models import Q
#from .filtres import NewsFilter
from .filtres import NewsArticFilter
from .forms import NewsForm, ArticleForm


class PostListView(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news/news_home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Получение изначального queryset через суперметод
        queryset = super().get_queryset()
        # Фильтрация по полю 'type' равному 'A'
        queryset = queryset.filter(type='N')
        return queryset


# def news_home(request):
#     # Получение только новостей:
#     posts = Post.objects.filter(type='N').order_by('-created_at')
#     paginator = Paginator(posts, 10)
#     page = request.GET.get('page')
#     posts = paginator.get_page(page)
#     return render(request, 'news/news_home.html', {'posts': posts})


# Функция для отображения статей:
def articles_home(request):
    articles = Post.objects.filter(type='A').order_by('-created_at')
    paginator = Paginator(articles, 10)  # преобразовать в число
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles/articles_home.html', {'articles': articles})


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'news_detail'  # или 'post_detail'

    def get_queryset(self):
        # Получение изначального queryset через суперметод
        queryset = super().get_queryset()
        # Фильтрация по полю 'type' равному 'A'
        queryset = queryset.filter(type='N')
        return queryset


class ArticlesDetailView(DetailView):
    model = Post
    template_name = 'articles/articles_detail.html'
    context_object_name = 'articles_detail'

    def get_queryset(self):
        # Получение изначального queryset через суперметод
        queryset = super().get_queryset()
        # Фильтрация по полю 'type' равному 'A'
        queryset = queryset.filter(type='A')
        return queryset


# Изменения в представлениях, связанных с записями:


class NewsArticleCreateView(CreateView):
    model = Post
    template_name = 'news/post_create.html'  # или 'articles/article_create.html'
    fields = '__all__'  # или список полей, которые вы хотите включить


class NewsCreateView(CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/post_create.html'
    success_url = reverse_lazy('news_home')

    def form_valid(self, form):
        form.instance.type = 'N'  # Устанавливаем значение поля
        return super().form_valid(form)


class ArticleCreateView(CreateView):
    model = Post
    form_class = ArticleForm
    template_name = 'news/post_create.html'
    success_url = reverse_lazy('articles_home')

    def form_valid(self, form):
        form.instance.type = 'A'  # Устанавливаем значение поля
        return super().form_valid(form)


class NewsArticleUpdateView(UpdateView):
    model = Post
    template_name = 'news/post_update.html'  # или 'articles/article_update.html'
    fields = '__all__'

    def get_success_url(self):
        print("get_success_url called")
        if self.object.type == 'N':
            return reverse_lazy('news_home')
        elif self.object.type == 'A':
            return reverse_lazy('articles_home')


class NewsArticleDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_home')

    def get_success_url(self):
        if self.object.type == 'N':
            return reverse_lazy('news_home')
        elif self.object.type == 'A':
            return reverse_lazy('articles_home')


# def search_view(request):
#     query = request.GET.get('q')
#     post_list = Post.objects.all()
#
#     # Применяем фильтр, если запрос не пустой
#     if query:
#         post_list = NewsFilter(request.GET, queryset=post_list).qs
#
#     paginator = Paginator(post_list, 10)
#     page = request.GET.get('page')
#     posts = paginator.get_page(page)
#
#     # Создаем пустой фильтр, чтобы отобразить форму в шаблоне
#     post_filter = NewsFilter()
#
#     return render(request, 'news/search.html', {'posts': posts, 'query': query, 'post_filter': post_filter})


class NewsArticleSearchView(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news/search.html'
    context_object_name = 'search_results'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsArticFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context
