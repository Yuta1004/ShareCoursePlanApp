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


@mysql_transaction
def get_post(cur, post_id):
    cur.execute(
        """
            SELECT posts.post_id as post_id, posts.user_id as user_id, users.name as name, posts.post_on as post_on, posts.text as text
            FROM posts
            LEFT JOIN users
                ON posts.user_id = users.user_id
            WHERE posts.post_id = %s
        """,
        [post_id]
    )
    post = cur.fetchall()
    if len(post) != 1:
        return False, {}
    return True, post[0]


@mysql_transaction
def get_posts(cur, page=1, page_size=10):
    cur.execute(
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
    return cur.fetchall()


@mysql_transaction
def get_replies(cur, post_id):
    cur.execute(
        """
            SELECT posts.post_id as post_id, posts.user_id as user_id, users.name as name, posts.post_on as post_on, posts.text as text
            FROM posts
            LEFT JOIN users
                ON posts.user_id = users.user_id
            WHERE posts.reply_to is not NULL
            ORDER BY posts.post_on ASC
        """
    )
    return cur.fetchall()
