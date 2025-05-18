from django.urls import path
from . import views

app_name = 'globalchat'

urlpatterns = [
    path('', views.global_chat, name='global_chat'),
]