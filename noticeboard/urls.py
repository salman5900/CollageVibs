from django.urls import path
from . import views

app_name = 'noticeboard'

urlpatterns = [
    path('', views.noticeboard_view, name='main'),
]