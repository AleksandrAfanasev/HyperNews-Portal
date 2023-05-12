from django.urls import path
from .views import *

urlpatterns = [
    path('', ComingSoonView.as_view()),
    path('news/<int:link>/', NewsView.as_view()),
    path('news/', NewsListView.as_view()),
    path('news/create/', CreateNews.as_view()),
]