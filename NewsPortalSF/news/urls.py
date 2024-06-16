from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
                  # path('news/', news_home, name='news_home'),
                  path('news/', PostListView.as_view(), name='news_home'),
                  path('articles/', articles_home, name='articles_home'),
                  # path('news/search', search_view, name='news_search'),
                  # path('articles/search', search_view, name='articles_search'),
                  path('news/search/', NewsArticleSearchView.as_view(), name='news_search'),
                  path('articles/search', NewsArticleSearchView.as_view(), name='articles_search'),
                  path('news/create/', NewsCreateView.as_view(), name='news_create'),
                  path('articles/create/', ArticleCreateView.as_view(), name='articles_create'),
                  path('news/<int:pk>/edit/', NewsArticleUpdateView.as_view(), name='news_edit'),
                  path('news/<int:pk>/delete/', NewsArticleDeleteView.as_view(), name='news_delete'),
                  path('articles/<int:pk>/edit/', NewsArticleUpdateView.as_view(), name='article_edit'),
                  path('articles/<int:pk>/delete/', NewsArticleDeleteView.as_view(), name='article_delete'),
                  path('news/<int:pk>/', PostDetailView.as_view(), name='news_detail'),
                  path('articles/<int:pk>/', ArticlesDetailView.as_view(), name='articles_detail'),
                  path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
                  path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
