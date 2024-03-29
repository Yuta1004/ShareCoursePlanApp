from db.core.mysql import mysql_transaction


@mysql_transaction
def save_classes_from_csv(cur, pdobj):
    if not {"科目番号", "科目名", "単位数"}.issubset(pdobj.columns):
        return False, []

    cur.executemany(
        """
            INSERT INTO classes
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                credits = VALUES(credits)
        """,
        pdobj[["科目番号", "科目名", "単位数"]].values.tolist()
    )

    return True, pdobj["科目番号"].values


@mysql_transaction
def register_classes(cur, user_id, classes):
    cur.executemany(
        """
            INSERT INTO users_classes (user_id, class_id)
            VALUES (%s, %s)
        """,
        list(map(lambda class_id: [user_id, class_id], classes))
    )


@mysql_transaction
def remove_class(cur, user_id, class_id):
    cur.execute(
        """
            DELETE
            FROM users_classes
            WHERE user_id = %s AND class_id = %s 
        """,
        [user_id, class_id]
    )

@mysql_transaction
def set_grade(cur, user_id, class_id, grade):
    cur.execute(
        """
            UPDATE users_classes
            SET grade = %s
            WHERE user_id = %s AND class_id = %s
        """,
        [grade ,user_id, class_id]
    )


@mysql_transaction
def get_classes_not_registered(cur, user_id):
    cur.execute(
        """
            SELECT classes.class_id as class_id, classes.name as name, classes.credits as credits
            FROM classes
            LEFT JOIN (SELECT * from users_classes WHERE user_id = %s) as users_classes
                ON classes.class_id = users_classes.class_id
            WHERE users_classes.user_id is NULL
        """,
        [user_id]
    )
    return cur.fetchall()


@mysql_transaction
def get_classes_taking(cur, user_id):
    cur.execute(
        """
            SELECT classes.class_id as class_id, classes.name as name, classes.credits as credits
            FROM classes
            LEFT JOIN (SELECT * from users_classes WHERE user_id = %s) as users_classes
                ON classes.class_id = users_classes.class_id
            WHERE users_classes.user_id is not NULL AND
                  users_classes.grade is NULL
        """,
        [user_id]
    )
    return cur.fetchall()


@mysql_transaction
def get_classes_completed(cur, user_id):
    cur.execute(
        """
            SELECT classes.class_id as class_id, classes.name as name, classes.credits as credits, users_classes.grade as grade
            FROM classes
            LEFT JOIN (SELECT * from users_classes WHERE user_id = %s) as users_classes
                ON classes.class_id = users_classes.class_id
            WHERE users_classes.user_id is not NULL AND
                  users_classes.grade is not NULL
        """,
        [user_id]
    )
    return cur.fetchall()
