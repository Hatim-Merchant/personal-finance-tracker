import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "finance.db")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               amount REAL NOT NULL,
               date TEXT NOT NULL,
               category TEXT  NOT NULL,
               type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
               description TEXT
               );
               """)
connection.commit()
connection.close()

print("Database created successfully.")
