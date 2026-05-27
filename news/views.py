from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_event'] = "В четверг пройдет ежегодная встреча авторов!"
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'