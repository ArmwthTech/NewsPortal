from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('news.urls')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls'), name='sign'),
    path('', include('protect.urls'), name= 'protect'),
    path('accounts/', include('allauth.urls')),
]
