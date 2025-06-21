# utils.py or below your views
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import redis

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

redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_club_online_users_key(club_id):
    return f"club_online_users:{club_id}"

def add_user_to_club(club_id, user_id):
    key = get_club_online_users_key(club_id)
    redis_instance.sadd(key, user_id)

def remove_user_from_club(club_id, user_id):
    key = get_club_online_users_key(club_id)
    redis_instance.srem(key, user_id)

def get_club_online_count(club_id):
    key = get_club_online_users_key(club_id)
    return redis_instance.scard(key)
