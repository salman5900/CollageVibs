import os
import redis
from urllib.parse import urlparse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Parse Redis URL (works locally and in production with Upstash)
redis_url = os.environ.get(
    "REDIS_URL",
    "rediss://default:AXdrAAIjcDFhY2I0YmVlMzQ0YjI0MWJmYjFiMTQ1NjRiZWU1NDVkY3AxMA@evolved-cricket-30571.upstash.io:6379"
)
parsed_url = urlparse(redis_url)

#  Redis connection instance
redis_instance = redis.StrictRedis(
    host=parsed_url.hostname,
    port=parsed_url.port,
    password=parsed_url.password,
    db=0,
    decode_responses=True,
    ssl=parsed_url.scheme == 'rediss'
)

# Real-time notifications using Django Channels
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

# Club online users tracking
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
