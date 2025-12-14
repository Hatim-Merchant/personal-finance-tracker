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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, category, SUM(amount)
        FROM transactions
        WHERE date LIKE ?
        GROUP BY type, category;
    """, (f"{month}-%",))

    rows = cursor.fetchall()
    conn.close()

    income_cat = {}
    expense_cat = {}

    for type, category, total in rows:
        if type == "income":
            income_cat[category] = total
        else:
            expense_cat[category] = total

    return income_cat, expense_cat

def get_simple_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, SUM(amount)
        FROM transactions
        GROUP BY type;
    """)

    rows = cursor.fetchall()
    conn.close()

    income = 0
    expense = 0

    for type, total in rows:
        if type == "income":
            income = total
        else:
            expense = total
    
    return income, expense

def get_transactions(category, type, min_amt, max_amt, start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT id, amount, date, category, type, description FROM transactions WHERE 1=1"
    params = []

    if category:
        sql += " AND category LIKE ?"
        params.append(f"%{category}%") 

    if type:
        sql += " AND type = ?"
        params.append(type.lower())  

    if min_amt:
        sql += " AND amount >= ?"
        params.append(min_amt)
    if max_amt:
        sql += " AND amt <= ?"
        params.append(max_amt)
    if start_date:
        sql += " AND date >= ?"
        params.append(start_date)
    if end_date:
        sql += " AND date <= ?"
        params.append(end_date)

    sql += " ORDER BY date;"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    connection.close()

    transactions = []
    for r in rows:
        transactions.append({
            "id": r[0],
            "amount": r[1],
            "date": r[2],
            "category": r[3],
            "type": r[4],
            "description": r[5]
        })

    return transactions

#implementing POST transaction (inserting transaction)

def insert_transaction(amount, date, category, type, description):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO transactions (amount, date, category, type, description)
        VALUES (?, ?, ?, ?, ?);
    """, (amount, date, category, type, description))
    connection.commit()
    connection.close()