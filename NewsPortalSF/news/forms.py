# forms.py
from django import forms
from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type = 'N'  # Устанавливаем значение поля
        if commit:
            instance.save()
        return instance


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type = 'A'  # Устанавливаем значение поля
        if commit:
            instance.save()
        return instance
