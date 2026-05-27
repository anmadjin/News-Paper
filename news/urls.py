from django.urls import path
from .views import PostsList, PostDetail



urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('<int:pk>/', PostDetail.as_view(), name='post'),
]