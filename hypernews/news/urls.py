from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home_view, name='all_posts'),
    path('news/<int:id>/', views.news_by_id, name='post'),
    path('news/create/', views.create_post, name='create_post'),
    path('news/', views.news, name='news'),

]
