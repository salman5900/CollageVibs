from django.urls import path
from . import views

app_name = 'clubs'

urlpatterns = [
    path('create/', views.create_club, name='create_club'),
    path('<int:club_id>', views.club_chat, name='club_chat'),
]