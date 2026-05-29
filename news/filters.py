from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название:'
    )

    author__user__username = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор:'
    )

    time_in = DateFilter(
        field_name='time_in',
        lookup_expr='gte',
        label='Позже даты:',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'time_in']