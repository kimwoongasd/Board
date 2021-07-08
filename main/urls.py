from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('count/', views.count, name='count'),
    path('word/', views.word, name='word'),
    path('detail/<int:blog_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('postcreate/', views.postcreate, name='postcreate'),
    path('update/<int:blog_id>/', views.update, name='update'),
    path('delete/<int:blog_id>/', views.delete, name='delete'),
    path('search', views.search, name='search'),
    path('newreply/<int:blog_id>/', views.newreply, name="newreply"),
    path('like/<int:blog_id>/', views.likes, name="likes"),
]