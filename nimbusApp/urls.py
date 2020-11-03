from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login), 
    path('logout', views.logout),
    path('home', views.home),
    path('create_post', views.create),
    path('delete_post/<int:post_id>', views.delete),
    path('user_profile/<int:user_id>', views.profile),
    path('user_post/<int:post_id>', views.post), 
]