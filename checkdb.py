import sqlite3

conn = sqlite3.connect('glossary.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM glossary')
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()