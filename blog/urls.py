# blog/urls.py
from django.urls import path
from .views import (
    TherapyArticleListView, TherapyArticleDetailView, TherapyArticleBySlugView,
    TherapyArticleCreateView, TherapyArticleUpdateView, TherapyArticleDeleteView
)

urlpatterns = [
    path('articles/', TherapyArticleListView.as_view(), name='therapy_article_list'),
    path('articles/<int:pk>/', TherapyArticleDetailView.as_view(), name='therapy_article_detail'),
    path('articles/slug/<slug:slug>/', TherapyArticleBySlugView.as_view(), name='therapy_article_by_slug'),
    path('articles/create/', TherapyArticleCreateView.as_view(), name='therapy_article_create'),
    path('articles/<int:pk>/update/', TherapyArticleUpdateView.as_view(), name='therapy_article_update'),
    path('articles/<int:pk>/delete/', TherapyArticleDeleteView.as_view(), name='therapy_article_delete'),
]
