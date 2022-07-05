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
