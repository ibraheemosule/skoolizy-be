from redis import Redis

cache = Redis(decode_responses=True)
