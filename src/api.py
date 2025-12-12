from fastapi import FastAPI
from db.db import insert_transaction, fetch_transactions, get_monthly_summary, get_simple_summary, get_transactions
from pydantic import BaseModel
from typing import Optional


app = FastAPI(title="Finance Tracker")

#pydantic model for input validation
class Transaction(BaseModel):
    amount: float
    date: str
    category: str
    type: str
    description: Optional[str] = ""

#adding transaction
@app.post("/transactions/")
def add_transactions(transaction: Transaction):
    insert_transaction(transaction.amount,
                       transaction.date,
                       transaction.category,
                       transaction.type,
                       transaction.description
                       )
    return {"message": "Transaction added successfully"}

#list all transactions
@app.get("/transactions/")
def list_transactions():
    transactions = fetch_transactions()
    return transactions

#simple summary
@app.get("/summary/simple/")
def simple_summary():
    income, expense = get_simple_summary()
    return {
        "Total Income": income,
        "Total Expense": expense,
        "Balance": income - expense
    }

#monthly summary
@app.get("/summary/monthly/")
def monthly_summary(month: str):
    income_cat, expense_cat = get_monthly_summary(month)
    return {
        "Income: ": income_cat,
        "Expense:": expense_cat
    }