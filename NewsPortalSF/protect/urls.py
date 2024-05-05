from django.urls import path
from .views import IndexView

urlpatterns = [
    path('protect/', IndexView.as_view()),
]