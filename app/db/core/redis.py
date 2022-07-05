from redis import Redis
import redis


REDIS_CONN_SETTINGS = {
    "host": "redis",
    "port": 6379,
    "db": 0
}


def redis_conn(func):
    def wrapper(*args, **kwargs):
        try:
            conn = Redis(**REDIS_CONN_SETTINGS)
            result = func(conn, *args, **kwargs)
        except Exception as e:
            print(e, flush=True)
        conn.close()
        return result
    return wrapper
