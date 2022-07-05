from uuid import uuid4 as uuid

from db.core.mysql import mysql_transaction


@mysql_transaction
def save_post(cur, user_id, text):
    if text == "":
        return False

    post_id = str(uuid()).replace("-", "")

    cur.execute(
        """
            INSERT INTO posts
            VALUES (%s, %s, NOW(), %s, NULL)
        """,
        [post_id, user_id, text]
    )
    return True
