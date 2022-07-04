from redis import Redis
import redis


REDIS_CONN_SETTINGS = {
    "host": "mysql",
    "port": 6379,
    "db": 0
}


def redis_conn(func):
    def wrapper(*args, **kwargs):
        conn = Redis(**REDIS_CONN_SETTINGS)
        func(conn, args, kwargs)
    return wrapper
