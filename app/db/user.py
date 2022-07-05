from db.core.mysql import mysql_transaction


@mysql_transaction
def get_user_info(cur, user_id):
    cur.execute(
        """
            SELECT user_id, email, name
            FROM users
            WHERE user_id = %s
        """,
        [user_id]
    )
    user_info = cur.fetchall()
    if len(user_info) != 1:
        return False, {"user_id": "", "email": "", "name": ""}
    return True, user_info[0]
