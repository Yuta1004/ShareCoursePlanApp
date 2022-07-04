from bcrypt import checkpw

from db.core.mysql import mysql_transaction


@mysql_transaction
def login(cur, user_id, password):
    if user_id == "" or password == "":
        return False
    
    user_auth_info = cur.execute("SELECT * FROM users_auth WHERE user_id = ?", (user_id, )).fetchall()
    if len(user_auth_info) != 1:
        return False
    return checkpw(password, user_auth_info[0][1])
