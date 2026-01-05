import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM expenses").fetchall()

print("Expenses in DB:")
for row in rows:
    print(row)

conn.close()
