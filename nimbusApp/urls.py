from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('', views.register),
    path('', views.login), 
]