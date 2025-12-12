import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "finance.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def insert_transaction(amount, date, category, type, description):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO transactions (amount, date, category, type, description)
                   values (?, ?, ?, ?, ?);
                   """,(amount, date, category, type, description))
    connection.commit()
    connection.close()

def fetch_transactions():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, amount, date, category, type, description FROM transactions ORDER BY date;")
    rows = cursor.fetchall()
    connection.close()
    transactions = []
    for row in rows:
        transactions.append({
            "id": row[0],
            "amount": row[1],
            "date": row[2],
            "category": row[3],
            "type": row[4],
            "description": row[5]
        })
    return transactions

#monthly summary function
def get_monthly_summary(month):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT type, category, sum(amount) FROM transactions
        WHERE date LIKE ?
        GROUP BY type, category;
    """, (f"{month}-%",))

    rows = cursor.fetchall()
    connection.close()

    income_cat = {}
    expense_cat = {}

    for r in rows:
        t_type, category, total = r
        if t_type == "income":
            income_cat[category] = total
        else:
            expense_cat[category] = total
    return income_cat, expense_cat               
