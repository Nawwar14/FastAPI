import sqlite3
import json
import os

db_path = 'glossary.db'

if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS glossary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL,
        value TEXT NOT NULL
    )
    ''')

    with open('glossary.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        cursor.execute('''
        INSERT INTO glossary (key, value)
        VALUES (?, ?)
        ''', (item['key'], item['value']))

    conn.commit()
    conn.close()
    print("Создаем БД")
else:
    print("БД уже существует")