from django.urls import path
from . import views

app_name = 'clubs'

urlpatterns = [
    path('create/', views.create_club, name='create_club'),
    path('<int:club_id>', views.club_chat, name='club_chat'),
    path('invite/<int:club_id>/<int:user_id>/', views.send_invite, name='send_invite'),
    path('invite/respond/<int:invite_id>/<str:response>/', views.respond_invite, name='respond_invite'),
    path('notifications/', views.notifications, name='notifications'),
]