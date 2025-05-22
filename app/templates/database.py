import pymysql
import os

host = os.getenv("localhost")
user = os.getenv("root")
password = os.getenv("root")
db = os.getenv("harvester_db")


pymysql.connect(
    host=host,
    user=user,
    password=password,
    db=db,
    cursorclass=pymysql.cursors.DictCursor
)


def get_all_tables_data():
    connection = get_connection()
    tables_data = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [row[f'Tables_in_harvester_connect'] for row in cursor.fetchall()]
            for table in tables:
                cursor.execute(f"SELECT * FROM `{table}`")
                rows = cursor.fetchall()
                if rows:
                    tables_data[table] = rows
    finally:
        connection.close()
    return tables_data

def delete_selected_rows(table_name, ids):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            for row_id in ids:
                cursor.execute(f"DELETE FROM `{table_name}` WHERE id=%s", (row_id,))
        connection.commit()
    finally:
        connection.close()
