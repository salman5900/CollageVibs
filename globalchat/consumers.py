from channels.generic.websocket import WebsocketConsumer 
from django.template.loader import render_to_string 
import json 
from asgiref.sync import async_to_sync
from .models import GlobalChatMessage

class GlobalChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(
            'global_chat',
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        # Save the message
        message = GlobalChatMessage.objects.create(
            user=self.user,
            message=message_text
        )

        # Broadcast the message to all clients
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

    def chat_message(self, event):
        print("Sending OOB update to:", self.channel_name)
        message_id = event['message_id']
        message = GlobalChatMessage.objects.get(id=message_id)
        context = {
            'chat': message,
            'user': self.user,  # sender can see their own message styled correctly
        }

        # Just render the <li> message
        message_html = render_to_string('globalchat/global_chat_message.html', context=context)

        self.send(text_data=message_html)
