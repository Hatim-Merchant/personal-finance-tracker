from fastapi import FastAPI
from db.db import insert_transaction, fetch_transactions, get_monthly_summary, get_simple_summary, get_transactions
from pydantic import BaseModel, Field
from typing import Optional, Literal
from fastapi.responses import StreamingResponse
import io, csv
from schemas import TransactionCreate

app = FastAPI(title="Finance Tracker")

#list all transactions
@app.get("/transactions/")
def list_transactions(category: Optional[str] = None, type: Optional[str] = None):
    transactions = fetch_transactions()
    if not transactions:
        return {"message": "No transactions found"}
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

@app.get("/transactions/search/")
def search_transactions(category: Optional[str] = None, 
                        type: Optional[str] = None, 
                        min_amt: Optional[float] = None, 
                        max_amt: Optional[float] = None, 
                        start_date: Optional[str] = None, 
                        end_date: Optional[str] = None):
    transactions = get_transactions(category=category, 
                                    type=type, 
                                    min_amt=min_amt, 
                                    max_amt=max_amt, 
                                    start_date=start_date, 
                                    end_date=end_date)
    return transactions

#export transactions as CSV
@app.get("/exports/csv")
def export_transactions_csv():
    transactions = fetch_transactions()

    if not transactions:
        return {"message": "No transactions to export"}

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["id", "date", "type", "category", "amount", "description"]
    )

    writer.writeheader()
    writer.writerows(transactions)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"}
    )
#implementing POST endpoint to add transaction
@app.post("/transactions/")
def create_transaction(transaction: TransactionCreate):
    insert_transaction(
        transaction.amount,
        transaction.date,
        transaction.category,
        transaction.type,
        transaction.description
    )
    return {"message": "Transaction added successfully"}
