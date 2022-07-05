from uuid import uuid4 as uuid

from db.core.redis import redis_conn
from db.core.mysql import mysql_transaction


@redis_conn
@mysql_transaction
def save_post(mcur, rconn, user_id, text):
    if text == "":
        return False

    post_id = str(uuid()).replace("-", "")

    mcur.execute(
        """
            INSERT INTO posts
            VALUES (%s, %s, NOW(), %s, NULL)
        """,
        [post_id, user_id, text]
    )
    rconn.set("scp:"+post_id, 0)
    return True


@redis_conn
@mysql_transaction
def get_post(mcur, rconn, post_id):
    mcur.execute(
        """
            SELECT posts.post_id as post_id, posts.user_id as user_id, users.name as name, posts.post_on as post_on, posts.text as text
            FROM posts
            LEFT JOIN users
                ON posts.user_id = users.user_id
            WHERE posts.post_id = %s
        """,
        [post_id]
    )
    post = mcur.fetchall()
    if len(post) != 1:
        return False, {}
    post[0]["like_count"] = rconn.get("scp:"+post_id)
    return True, post[0]


@redis_conn
@mysql_transaction
def get_posts(mcur, rconn, page=1, page_size=10):
    mcur.execute(
        """
            SELECT posts.post_id as post_id, posts.user_id as user_id, users.name as name, posts.post_on as post_on, posts.text as text,
                (SELECT COUNT(*) FROM posts as posts2 where posts.post_id = posts2.reply_to) as replies_num
            FROM posts
            LEFT JOIN users
                ON posts.user_id = users.user_id
            WHERE posts.reply_to is NULL
            ORDER BY posts.post_on DESC
            LIMIT %s
            OFFSET %s
        """,
        [page_size, (page-1)*page_size]
    )
    posts = mcur.fetchall()
    for idx in range(len(posts)):
        posts[idx]["like_count"] = rconn.get("scp:"+posts[idx]["post_id"])
    return posts


@redis_conn
@mysql_transaction
def save_reply(mcur, rconn, reply_to, user_id, text):
    if text == "":
        return False

    post_id = str(uuid()).replace("-", "")

    mcur.execute(
        """
            INSERT INTO posts
            VALUES (%s, %s, NOW(), %s, %s)
        """,
        [post_id, user_id, text, reply_to]
    )
    rconn.set("scp:"+post_id, 0)
    return True


@redis_conn
@mysql_transaction
def get_replies(mcur, rconn, post_id):
    mcur.execute(
        """
            SELECT posts.post_id as post_id, posts.user_id as user_id, users.name as name, posts.post_on as post_on, posts.text as text
            FROM posts
            LEFT JOIN users
                ON posts.user_id = users.user_id
            WHERE posts.reply_to is not NULL
            ORDER BY posts.post_on ASC
        """
    )
    replies = mcur.fetchall()
    for idx in range(len(replies)):
        replies[idx]["like_count"] = rconn.get("scp:"+replies[idx]["post_id"])
    return replies
