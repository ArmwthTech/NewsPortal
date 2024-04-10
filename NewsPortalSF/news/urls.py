from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path('', views.news_home, name='news_home'),
                  path('<int:pk>/', views.PostDetailView.as_view(), name='news_detail'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
