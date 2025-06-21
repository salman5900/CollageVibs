# utils.py
import redis

redis_instance = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

def get_global_online_count():
    return redis_instance.scard('global_online_users')

def get_club_online_counts(club_ids):
    counts = {}
    for club_id in club_ids:
        key = f'clubchat_online_{club_id}'  # Match your consumer
        counts[club_id] = redis_instance.scard(key)
    return counts
