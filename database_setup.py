import sqlite3

def create_database():
    conn = sqlite3.connect('medical_program.db')
    cursor = conn.cursor()

    # ������� ��� �����
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL UNIQUE,
            hash_password TEXT NOT NULL
        )
    ''')

    # ������� � ������������, ���������� �� �������� �����������
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT,
            birth_date TEXT,
            gender TEXT,
            email TEXT,
            phone TEXT,
            role TEXT CHECK(role IN ('�������', '����')) DEFAULT '�������',
            blood_type TEXT,
            chronic_diseases TEXT,
            allergies TEXT,
            medications TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("Database and all tables created successfully.")

create_database()
