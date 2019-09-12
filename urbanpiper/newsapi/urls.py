from django.urls import path
from newsapi import views


urlpatterns = [
    path('api/top_article/', views.TopArticalView.as_view()),
    path('api/sentiment/', views.SentiMentView.as_view()),
    path('api/info/', views.ArticleInfoView.as_view()),  
    path('api/search/',views.SearchArticleView.as_view()),
]