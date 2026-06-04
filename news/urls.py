from django.urls import path
from django.views.decorators.cache import cache_page
from .views import PostsList, PostDetail, PostsSearch, NewsCreate, NewsUpdate, NewsDelete, PaperCreate, PaperUpdate, \
    PaperDelete, CategoryPostsView, subscribe, unsubscribe

urlpatterns = [
    path('news/', cache_page(60)(PostsList.as_view()), name='posts'),
    path('news/<int:pk>/', cache_page(300)(PostDetail.as_view()), name='post_detail'),
    path('category/<int:pk>/', cache_page(300)(CategoryPostsView.as_view()), name='category_posts'),
    path('news/search/', PostsSearch.as_view(), name='post_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', PaperCreate.as_view(), name='paper_create'),
    path('articles/<int:pk>/edit/', PaperUpdate.as_view(), name='paper_edit'),
    path('articles/<int:pk>/delete/', PaperDelete.as_view(), name='paper_delete'),
    path('category/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('category/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
]