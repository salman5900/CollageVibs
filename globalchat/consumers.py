from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
import json
from asgiref.sync import async_to_sync
from .models import GlobalChatMessage
from .utils import redis_instance 

class GlobalChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']

        async_to_sync(self.channel_layer.group_add)(
            'global_chat',
            self.channel_name
        )

        redis_instance.sadd('global_online_users', str(self.user.id))

        self.Update_Online_Count()

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        message = GlobalChatMessage.objects.create(
            user=self.user,
            message=message_text
        )

        event = {
            'type': 'chat_message',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send)(
            'global_chat',
            event
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'global_chat',
            self.channel_name
        )

        
        redis_instance.srem('global_online_users', str(self.user.id))
   
        self.Update_Online_Count()

    def chat_message(self, event):
        message_id = event['message_id']
        message = GlobalChatMessage.objects.get(id=message_id)

        context = {
            'chat': message,
            'user': self.user, 
        }

        message_html = render_to_string('globalchat/global_chat_message.html', context=context)
        self.send(text_data=message_html)

    def Update_Online_Count(self):
        online_count = redis_instance.scard('global_online_users')
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(
            'global_chat',
            event
        )

    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string('globalchat/online_count.html', {'online_count': online_count})
        self.send(text_data=html)
