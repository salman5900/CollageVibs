from .models import Club, ClubMessage, ClubChatStatus
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import json
from django.utils import timezone

class ClubChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.club_id = self.scope['url_route']['kwargs']['club_id']
        self.club_group_name = f'club_{self.club_id}'
        self.user = self.scope['user']

        is_member = await self.check_membership()

        if self.user.is_authenticated and is_member:
            await self.channel_layer.group_add(
                self.club_group_name,
                self.channel_name
            )

            # Ensure ClubChatStatus exists
            self.status = await self.get_or_create_status()

            # Add user to online list
            await sync_to_async(self.status.user_online.add)(self.user)
            await self.update_online_count()

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.club_group_name,
            self.channel_name
        )

        self.status = await self.get_or_create_status()
        await sync_to_async(self.status.user_online.remove)(self.user)
        await self.update_online_count()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.club_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'first_name': self.user.first_name,
                'timestamp': timezone.now().strftime("%I:%M %p"),
                'profile_picture': await self.get_profile_picture_url(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'username': event['username'],
            'first_name': event['first_name'],
            'timestamp': event['timestamp'],
            'profile_picture': event['profile_picture'],
        }))

    async def online_count(self, event):
        await self.send(text_data=json.dumps({
            'type': 'online_count',
            'count': event['count'],
        }))

    async def update_online_count(self):
        count = await sync_to_async(self.status.user_online.count)()
        await self.channel_layer.group_send(
            self.club_group_name,
            {
                'type': 'online_count',
                'count': count
            }
        )

    @sync_to_async
    def get_or_create_status(self):
        club = Club.objects.get(id=self.club_id)
        status, _ = ClubChatStatus.objects.get_or_create(club=club)
        return status

    @sync_to_async
    def check_membership(self):
        try:
            club = Club.objects.get(id=self.club_id)
            return self.user in club.members.all()
        except Club.DoesNotExist:
            return False

    @sync_to_async
    def save_message(self, message):
        club = Club.objects.get(id=self.club_id)
        return ClubMessage.objects.create(club=club, user=self.user, message=message)

    @sync_to_async
    def get_profile_picture_url(self):
        try:
            profile = self.user.profile
            if profile.profile_picture:
                return profile.profile_picture.url
        except:
            return None
