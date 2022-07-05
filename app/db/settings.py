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


@mysql_transaction
def update_visibility(cur, user_id, taking_class_is_public, complete_class_is_public, grade_is_public):
    cur.execute(
        """
            UPDATE users_settings
            SET taking_class_is_public = %s,
                complete_class_is_public = %s,
                grade_is_public = %s
            WHERE
                user_id = %s
        """,
        [taking_class_is_public, complete_class_is_public, grade_is_public, user_id]
    )
