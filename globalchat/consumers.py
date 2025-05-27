from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
import json
from asgiref.sync import async_to_sync
from .models import GlobalChatMessage, GlobalChatStatus

class GlobalChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(
            'global_chat',
            self.channel_name
        )

        # Make sure GlobalChatStatus exists (singleton pattern)
        status, _ = GlobalChatStatus.objects.get_or_create(pk=1)

        # Add user to online users if not already online
        if self.user not in status.user_online.all():
            status.user_online.add(self.user)
            self.Update_Online_Count(status)

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

        # Remove user from online users if they were online
        status, _ = GlobalChatStatus.objects.get_or_create(pk=1)
        if self.user in status.user_online.all():
            status.user_online.remove(self.user)
            self.Update_Online_Count(status)

    def chat_message(self, event):
        message_id = event['message_id']
        message = GlobalChatMessage.objects.get(id=message_id)
        context = {
            'chat': message,
            'user': self.user,  # for styling (sender sees their own differently)
        }

        # Render only the <li> element for the message
        message_html = render_to_string('globalchat/global_chat_message.html', context=context)
        self.send(text_data=message_html)

    def Update_Online_Count(self, status):
        online_count = status.user_online.count()
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
