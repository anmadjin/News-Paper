from datetime import datetime, date
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm, PostForm2
from .models import Post, Category, Author
from .filters import PostFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.cache import cache


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

    def get_object(self, *args, **kwargs):
        cache_key = f'post-{self.kwargs["pk"]}'
        obj = cache.get(cache_key)
        if obj is None:
            obj = super().get_object(*args, **kwargs)
            cache.set(cache_key, obj)

        return obj


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


class NewsCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_add.html'
    permission_required = 'news.add_post'

    def handle_no_permission(self):
        return redirect('/news/')

    def form_valid(self, form):
        post = form.save()
        post.post_type = 'NE'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.id])

    def form_valid(self, form):
        user = self.request.user
        today = date.today()

        # categories = post.category.all()
        # emails = []
        # for cat in categories:
        #     for user in cat.subscribers.all():
        #         emails.append(user.email)
        #
        # emails = list(set(emails))
        #
        # if emails:
        #     html_content = render_to_string('email/new_post_not.html', {
        #         'post': post,
        #         'username': self.request.user.username,
        #     })
        #
        #     send_mail(
        #         subject=post.title,
        #         message=post.text[:100],
        #         from_email=settings.DEFAULT_FROM_EMAIL,
        #         recipient_list=emails,
        #         html_message=html_content,
        #     )
        try:
            author = Author.objects.get(user=user)
        except Author.DoesNotExist:
            messages.error(self.request, 'Ваш аккаунт не связан с автором. Обратитесь к администратору.')
            return redirect('news_create')
        posts_today = Post.objects.filter(
            author__user=user,
            time_in__date=today
        ).count()
        if posts_today >= 3:
            messages.error(self.request, 'Вы не можете публиковать более 3 постов в сутки!')
            return redirect('news_create')
        post = form.save(commit=False)
        post.post_type = 'NE'
        post.save()
        form.save_m2m()
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
    permission_required = 'news.add_post'

    def handle_no_permission(self):
        return redirect('/news/')

    def form_valid(self, form):
        post = form.save()
        post.post_type = 'PA'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.id])

    def form_valid(self, form):
        user = self.request.user
        today = date.today()

        # categories = post.category.all()
        # emails = []
        # for cat in categories:
        #     for user in cat.subscribers.all():
        #         emails.append(user.email)
        #
        # emails = list(set(emails))
        #
        # if emails:
        #     html_content = render_to_string('email/new_post_not.html', {
        #         'post': post,
        #         'username': self.request.user.username,
        #     })
        #
        #     send_mail(
        #         subject=post.title,
        #         message=post.text[:100],
        #         from_email=settings.DEFAULT_FROM_EMAIL,
        #         recipient_list=emails,
        #         html_message=html_content,
        #     )
        try:
            author = Author.objects.get(user=user)
        except Author.DoesNotExist:
            messages.error(self.request, 'Ваш аккаунт не связан с автором. Обратитесь к администратору.')
            return redirect('news_create')
        posts_today = Post.objects.filter(
            author__user=user,
            time_in__date=today
        ).count()
        if posts_today >= 3:
            messages.error(self.request, 'Вы не можете публиковать более 3 постов в сутки!')
            return redirect('article_create')
        post = form.save(commit=False)
        post.post_type = 'PA'
        post.save()
        form.save_m2m()

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

class CategoryPostsView(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-time_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        if self.request.user.is_authenticated:
            context['is_subscribed'] = self.category.subscribers.filter(id=self.request.user.id).exists()
        return context


@login_required
def subscribe(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.subscribers.add(request.user)
    return redirect('category_posts', pk=pk)


@login_required
def unsubscribe(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.subscribers.remove(request.user)
    return redirect('category_posts', pk=pk)