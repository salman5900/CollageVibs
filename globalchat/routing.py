from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/globalchat/<chatroom_name>/', GlobalChatConsumer.as_asgi()),
]