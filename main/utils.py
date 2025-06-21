# utils.py
import os
import redis
from urllib.parse import urlparse

redis_url = os.environ.get(
    "REDIS_URL",
    "rediss://default:AXdrAAIjcDFhY2I0YmVlMzQ0YjI0MWJmYjFiMTQ1NjRiZWU1NDVkY3AxMA@evolved-cricket-30571.upstash.io:6379"
)

parsed_url = urlparse(redis_url)

redis_instance = redis.StrictRedis(
    host=parsed_url.hostname,
    port=parsed_url.port,
    password=parsed_url.password,
    db=0,
    decode_responses=True,
    ssl=parsed_url.scheme == 'rediss'
)


def get_global_online_count():
    return redis_instance.scard('global_online_users')

def get_club_online_counts(club_ids):
    counts = {}
    for club_id in club_ids:
        key = f'clubchat_online_{club_id}'  # Match your consumer
        counts[club_id] = redis_instance.scard(key)
    return counts
