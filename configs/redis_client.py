from redis import Redis
from configs import envs

cache = Redis(
    decode_responses=True,
    host=envs.REDIS_HOST,
    port=envs.REDIS_PORT,
    password=envs.REDIS_PASSWORD,
)
