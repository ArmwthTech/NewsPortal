import django_filters
from django import forms
from .models import Post
from django_filters import FilterSet


# class NewsFilter(django_filters.FilterSet):
#     title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Название')
#     author = django_filters.CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Автор')
#     created_at__gt = django_filters.DateFilter(field_name='created_at', lookup_expr='gt', label='Позже даты', widget=forms.DateInput(attrs={'type': 'date'}))
#
#     class Meta:
#         model = Post
#         fields = ['title', 'author', 'created_at__gt']

class NewsArticFilter(FilterSet):
    # class Meta:
    #     model = Post
    #     fields = {
    #         'title': ['icontains'],
    #         'author__user__username': ['icontains'],
    #         'created_at': ['gt'],
    #     }
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Название')
    author = django_filters.CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Автор')
    created_at__gt = django_filters.DateFilter(field_name='created_at', lookup_expr='gt', label='Позже даты',
                                               widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['title', 'author', 'created_at__gt']
