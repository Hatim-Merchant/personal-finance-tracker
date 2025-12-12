import json
import os
import csv
from db.db import get_monthly_summary, insert_transaction, fetch_transactions, get_simple_summary, get_transactions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "transactions.json")
BUDGET_FILE = os.path.join(DATA_DIR, "budget.json")

EXPORT_DIR = os.path.join(BASE_DIR, "..", "exports")

if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

#exporting to CSV
def export_csv(transactions, filename="transactions.csv"):
    csv_path = os.path.join(EXPORT_DIR, filename)
    with open (csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, "amount,date,category,type,description".split(","))
        writer.writeheader()
        writer.writerows(transactions)
        print(f"CSV saved → {csv_path}")


#Loading data file
def load_transaction():
    if not os.path.exists(DATA_FILE):
        return[]
    with open (DATA_FILE, "r") as f:
        return json.load(f)
#saving transactions to data file
def save_transaction(transactions):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2)

#loading budget file
def load_budgets():
    if not os.path.exists(BUDGET_FILE):
        return {}
    try:
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("22")
        return {}    

#saving budget to data file
def save_budgets(budgets):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budgets, f, indent=2)
        
#Implementing transaction adding function
def add_transactions(transactions, budgets):

    print("\n---Add Transaction---\n")
    amount = float(input("\nAmount: "))
    date = input("\nDate (YYYY-MM-DD): ")
    category = input("\nCategory: ")
    type = input("\nType(income or expense): ").lower()
    description = input("\nDescription: ")

    insert_transaction(amount, date, category, type, description)
    print("Transaction saved to database!")

#budget checking
    month = date[:7]
    total_expense = 0
    for t in transactions:
        if type == "expense" and category in budgets:
            if t["date"].startswith(month):
                total_expense += t["amount"]

    if category in budgets and total_expense > budgets[category]:
        print(f"Warning: Budget limit exceeded for {category}!")

#Implementing transaction lisiting function
def list_transactions():
    transactions = fetch_transactions()
    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n#  Date        Type      Category     Amount     Description")
    print("-" * 70)

    for i, t in enumerate(transactions, start=1):
        print(
            f"{i:<3}"
            f"{t['date']:<12}"
            f"{t['type']:<10}"
            f"{t['category']:<12}"
            f"{t['amount']:<10}"
            f"{t.get('description', '')}"
        )
#Implementing summary function
def show_summary():
    print("\n1. Simple Summary")
    print("2. Monthly Summary")
    print("3. Previous Menu")

    choice = input("\nSelect Summary Type: ")

    if choice == "1":
        income, expense = get_simple_summary()
        balance = income - expense

        print("\n--- Summary ---")
        print("Total Income:", income)
        print("Total Expense:", expense)
        print("Balance:", balance)

    elif choice == "2":
        month = input("Enter month (YYYY-MM): ")
        income_cat, expense_cat = get_monthly_summary(month)

        if not income_cat and not expense_cat:
            print("No transactions for this month.")
            return
        
        print("\n--- Monthly Summary ---")
        print("Income by Category:")
        for cat, amt in income_cat.items():
            print(f"{cat}: {amt}")

        print("\nExpense by Category:")
        for cat, amt in expense_cat.items():
            print(f"{cat}: {amt}")

    elif choice == "3":
        return
    else:
        print("Invalid option. Try again")

#Implementing budget setting function
def set_budget(budgets):
    category = input("\nCategory: ")
    amount = float(input("\nBudget Limit: "))
    budgets[category] = amount
    save_budgets(budgets)
    print(f"Budget for {category} set to {amount}")

#implementing transaction search function
def search_transactions():
        category = input("Search by category (leave blank to skip): ")
        type = input("Search by type (income/expense, leave blank to skip): ")

        results = get_transactions(category, type)       
        if not results:
            print("\nNo transactions found.")
            return

        print("\n#  Date        Type      Category     Amount     Description")
        print("-" * 70)
        for i, t in enumerate(results, start=1):
            print(
                f"{i:<3}"
                f"{t['date']:<12}"
                f"{t['type']:<10}"
                f"{t['category']:<12}"
                f"{t['amount']:<10}"
                f"{t.get('description','')}"
            )
#Implementing data export function
def export_data():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    filepath = os.path.join(EXPORT_DIR, "transactions.csv")
    transactions = get_transactions()  

    if not transactions:
        print("No transactions to export.")
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "amount", "date", "category", "type", "description"])
        writer.writeheader()
        writer.writerows(transactions)

    print(f"{len(transactions)} transactions exported to {filepath}")
#Main Menu
def main():
    transactions = fetch_transactions()
    budgets = load_budgets()

    while True:
        print("\n---Personal Finance Tracker---\n")
        print("1. Add Transaction")
        print("2. Show Summary")
        print("3. List Transactions")
        print("4. Edit Budget Limit")
        print("5. Search Transactions")
        print("6. Export Data to CSV")
        print("7. Exit")
        

        choice = input("\nSelect from Menu: ")

        if choice == "1":
            add_transactions(transactions, budgets)
        elif choice == "3":
            list_transactions()
        elif choice =="2":
            show_summary()
        elif choice == "4":
            set_budget(budgets)
        elif choice == "5":
            search_transactions()
        elif choice == "6":
            export_data()
        elif choice == "7":
            print("\nExiting")
            save_transaction(transactions)
            break

        else:
            print("Invalid option. Try again")
if __name__ == "__main__":
    main()
