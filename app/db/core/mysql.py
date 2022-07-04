import pymysql
from pymysql import cursors


MYSQL_CONN_SETTINGS = {
    "host": "mysql",
    "user": "root",
    "password": "mysql",
    "database": "share_course_plan",
    "cursorclass": cursors.DictCursor
}


def mysql_transaction(func):
    def wrapper(*args, **kwargs):
        result = None
        conn = pymysql.connect(**MYSQL_CONN_SETTINGS)
        try:
            with conn.cursor() as cur:
                result = func(cur, *args, **kwargs)
            conn.commit()
        except Exception as e:
            print(e, flush=True)
        conn.close()
        return result
    return wrapper
