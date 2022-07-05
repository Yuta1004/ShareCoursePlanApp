from db.core.mysql import mysql_transaction


@mysql_transaction
def get_visibility(cur, user_id):
    cur.execute(
        """
            SELECT *
            FROM users_settings
            WHERE user_id = %s
        """,
        [user_id]
    )
    return cur.fetchone()
