from uuid import uuid4 as uuid
from bcrypt import checkpw, gensalt, hashpw

from db.core.mysql import mysql_transaction


@mysql_transaction
def login(cur, user_id, password):
    if user_id == "" or password == "":
        return False

    user_auth_info = cur.execute("SELECT * FROM users_auth WHERE user_id = ?", (user_id, )).fetchall()
    if len(user_auth_info) != 1:
        return False
    return checkpw(password, user_auth_info[0][1])


@mysql_transaction
def register(cur, name, email, password):
    if name == "" or email == "" or password == "" or len(password) < 8:
        return False

    user_id = str(uuid()).replace("-", "")
    hashed_password = hashpw(password.encode(), gensalt(rounds=12, prefix=b'2a'))

    cur.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, email, name))
    cur.execute("INSERT INTO users_auth VALUES (?, ?)", (user_id, hashed_password))
    cur.execute("INSERT INTO users_settings VALUES (?)", (user_id, ))
