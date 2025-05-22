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

        # Save message
        message = GlobalChatMessage.objects.create(
            user=self.user,
            message=message_text
        )

        # Broadcast to all clients 
        event = {
            'type': 'chat_message',
            'message_id': message.id,
            'sender_channel_name': self.channel_name, 
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
        # Skip sending to the sender again
        if self.channel_name == event.get('sender_channel_name'):
            return

        message_id = event['message_id']
        message = GlobalChatMessage.objects.get(id=message_id)
        context = {
            'chat': message,
            'user': self.user,
        }

        # Render the message HTML
        message_html = render_to_string('globalchat/global_chat_message.html', context=context)

        # Wrap it with hx-swap-oob directive and class for animation
        html_response = f'<div hx-swap-oob="beforeend:#chat_messages"><div class="chat-message">{message_html}</div></div>'

        self.send(text_data=html_response)
