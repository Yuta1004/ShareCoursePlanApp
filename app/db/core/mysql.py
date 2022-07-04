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
        conn = pymysql.connect(**MYSQL_CONN_SETTINGS)
        try:
            with conn.cursor() as cur:
                func(cur, args, kwargs)
            conn.commit()
        except:
            pass
        conn.close()
    return wrapper
