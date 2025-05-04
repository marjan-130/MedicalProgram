import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='medic',
            user='root',
            password='abba',
            port=3306
        )
        if connection.is_connected():
            return connection
        else:
            return None
    except Error as err:
        print(f"[DB ERROR] {err}")
        return None
