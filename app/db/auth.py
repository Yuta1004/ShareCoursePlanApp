from uuid import uuid4 as uuid
from bcrypt import checkpw, gensalt, hashpw

from db.core.mysql import mysql_transaction


@mysql_transaction
def login(cur, email, password):
    if email == "" or password == "":
        return False, "", "", False

    cur.execute(
        """
            SELECT users.user_id as user_id, users.name as name, users.is_admin as is_admin, users_auth.hashed_pw as hashed_pw
            FROM users
            INNER JOIN users_auth ON users.user_id = users_auth.user_id
            where users.email = %s
        """,
        [email]
    )
    user_auth_info = cur.fetchall()
    if len(user_auth_info) != 1:
        return False, "", "", False
    user_auth_info = user_auth_info[0]

    return checkpw(password.encode(), user_auth_info["hashed_pw"].encode()),\
           user_auth_info["user_id"],\
           user_auth_info["name"],\
           user_auth_info["is_admin"]


@mysql_transaction
def register(cur, name, email, password):
    if name == "" or email == "" or password == "" or len(password) < 8:
        return False, "", "", False

    user_id = str(uuid()).replace("-", "")
    hashed_password = hashpw(password.encode(), gensalt(rounds=12, prefix=b'2a'))

    cur.execute("INSERT INTO users (user_id, email, name) VALUES (%s, %s, %s)", [user_id, email, name])
    cur.execute("INSERT INTO users_auth VALUES (%s, %s)", [user_id, hashed_password])
    cur.execute("INSERT INTO users_settings (user_id) VALUES (%s)", [user_id])

    return True, user_id, name, False
