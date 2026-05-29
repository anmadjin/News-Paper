from django.urls import path
from .views import PostsList, PostDetail, PostsSearch, NewsCreate, NewsUpdate, NewsDelete, PaperCreate, PaperUpdate, PaperDelete



urlpatterns = [
   path('news/', PostsList.as_view(), name='posts'),
   path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('news/search/', PostsSearch.as_view(), name='post_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', PaperCreate.as_view(), name='paper_create'),
   path('articles/<int:pk>/edit/', PaperUpdate.as_view(), name='paper_edit'),
   path('articles/<int:pk>/delete/', PaperDelete.as_view(), name='paper_delete'),
]