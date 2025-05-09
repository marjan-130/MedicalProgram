# -*- coding: utf-8 -*-
import sqlite3

# ������� ��� ��������� ���� ����� �� �������
def create_database():
    # ϳ��������� �� ���� �����
    conn = sqlite3.connect('medical_program.db')
    
    # ��������� ������� ��� ��������� SQL ������
    cursor = conn.cursor()
    
    # ��������� �������, ���� ���� �� ����
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            hash_password TEXT NOT NULL
        )
    ''')
    
    # ϳ����������� ��� �� �������� �'�������
    conn.commit()
    conn.close()
    print("Database and table created successfully.")

# ��������� ������� ��� ��������� ���� �����
create_database()
