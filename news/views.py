from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm, PostForm2
from .models import Post
from .filters import PostFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_event'] = "В четверг пройдет ежегодная встреча авторов!"
        if self.request.user.is_authenticated:
            context['is_it_author'] = not self.request.user.groups.filter(name='authors').exists()
        else:
            context['is_it_author'] = False
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['next_event'] = "В четверг пройдет ежегодная встреча авторов!"
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_add.html'

    def handle_no_permission(self):
        return redirect('/news/')

    def form_valid(self, form):
        post = form.save()
        post.post_type = 'NE'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.id])


class NewsUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm2
    model = Post
    template_name = 'new_edit.html'

    def handle_no_permission(self):
        return redirect('/news/')

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.id])


class NewsDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('posts')

    def handle_no_permission(self):
        return redirect('/news/')


class PaperCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_add.html'

    def handle_no_permission(self):
        return redirect('/news/')

    def form_valid(self, form):
        post = form.save()
        post.post_type = 'PA'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.id])


class PaperUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm2
    model = Post
    template_name = 'new_edit.html'

    def handle_no_permission(self):
        return redirect('/news/')

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.id])


class PaperDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('posts')

    def handle_no_permission(self):
        return redirect('/news/')

#def create_post(request):
#    form = PostForm()
#    if request.method == 'POST':
#        form = PostForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect('/news')
#    return render(request, 'new_edit.html', {'form': form})