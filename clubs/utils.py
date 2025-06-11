# utils.py or below your views
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_club_disbanded(club_name, member_ids):
    channel_layer = get_channel_layer()
    for user_id in member_ids:
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "system.message",
                "message": f"🚨 The club '{club_name}' has been disbanded by the admin.",
            }
        )

def notify_member_left(club, user):
    channel_layer = get_channel_layer()
    for member in club.members.all():
        async_to_sync(channel_layer.group_send)(
            f"user_{member.id}",
            {
                "type": "system.message",
                "message": f"⚠️ {user.username} has left the club '{club.name}'.",
            }
        )
