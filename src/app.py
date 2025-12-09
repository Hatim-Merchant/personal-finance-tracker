import json
import os
from datetime import datetime as dt
import csv

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

    while True:
        date = input("\nDate (YYYY-MM-DD): ")
        try:
            date_obj = dt.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")

    category = input("\nCategory: ")
    type = input("\nType(income or expense): ")
    description = input("\nDescription: ")

    transaction = {
        "amount":amount, 
        "date":date,
        "category":category,
        "type":type,
        "description":description
    }

    transactions.append(transaction)
    print("Transaction Added!")

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
def list_transactions(transactions):
    print("\n--- All Transactions ---")

    if not transactions:
        print("No transactions found.")
        return

    print("#  Date         Type      Category     Amount     Description")
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
def show_summary(transactions):
    print("\n1. Simple Summary")
    print("\n2. Monthly Summary")
    print("\n3. Previous Menu")

    choice = input("\nSelect Summary Type: ")
    #Simple summary calculating total income, expense and balance
    if choice == "1":
        income = 0
        expense = 0
        for t in transactions:
            if t['type'] == 'income':
                income += t['amount']
            elif t['type'] == 'expense':
                expense += t['amount']
        balance = income - expense

        print("\n--- Summary---")
        print(f"Total Income: {income}")
        print(f"Total Expense: {expense}")
        print(f"Balance: {balance}")
        
    elif choice == "2":
        income_by_category = {}
        expense_by_category = {}
        found = False
        while True:
            month = input("\nEnter month to view (YYYY-MM): ")
            try:
                #validating month format
                dt.strptime(month, "%Y-%m")
                break 
            except ValueError:
                print("Invalid month format. Please use YYYY-MM")

        for t in transactions:
            if not t["date"].startswith(month):
                continue

            found = True
            category = t["category"]
            amount = t["amount"]

            if t["type"] == "income":
                income_by_category[category] = income_by_category.get(category, 0) + amount
            else:
                expense_by_category[category] = expense_by_category.get(category, 0) + amount
        if not found:
            print(f"\nNo transactions found for {month}")
            return
        
        total_income = sum(income_by_category.values())
        total_expense = sum(expense_by_category.values())
        balance = total_income - total_expense

        print("\n--- Monthly Summary ---")

        print("\nIncome by Category:")
        for category, amount in sorted(income_by_category.items(), key=lambda x: x[1], reverse=True):
            percent = (amount / total_income) * 100 if total_income > 0 else 0
            print(f"{category}: {amount} ({percent:.1f}%)")


        print("Total Income:",total_income)

        print("\nExpense by Category:")
        for category, amount in sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True):
            percent = (amount / total_expense) * 100 if total_expense > 0 else 0
            print(f"{category}: {amount} ({percent:.1f}%)")

        print("Total Expense:", total_expense)
        
        print(f"\nFinal Balance of {month} is: {balance}")

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

#Implementing search function
def search_transactions(transactions, query):
    q = query.strip().lower()
    matches = []

    for t in transactions:
        amount = str(t.get("amount", "")).lower()
        category = t.get("category", "").lower()
        date = t.get("date", "").lower()
        type = t.get("type", "").lower()
        desc = t.get("description", "").lower()

        if (q in amount) or (q in category) or (q in date) or (q in type) or (q in desc):
            matches.append(t)

    if not matches:
        print("No transactions found.")
        return
    
    print(f"Found {len(matches)} Transaction(s):")
    for i, m in enumerate(matches, start=1):
        print(
            f"{i}. {m.get('date','')} | {m.get('type','')} | "
            f"{m.get('category','')} | {m.get('amount','')} | {m.get('description','')}"
        )
        
#Main Menu
def main():
    transactions = load_transaction()
    budgets = load_budgets()

    while True:
        print("\n---Personal Finance Tracker---\n")
        print("1. Add")
        print("2. List Transactions")
        print("3. Show Summary")
        print("4. Edit Budget Limit")
        print("5. Search Transactions")
        print("6. Export Data to CSV")
        print("7. Exit")
        

        choice = input("\nSelect from Menu: ")

        if choice == "1":
            add_transactions(transactions, budgets)
        elif choice == "2":
            list_transactions(transactions)
        elif choice =="3":
            show_summary(transactions)
        elif choice == "4":
            set_budget(budgets)
        elif choice == "5":
            query = input("Search: ")
            search_transactions(transactions, query)
        elif choice == "6":
            export_csv(transactions)
            print("Data exported to CSV file.")
        elif choice == "7":
            print("\nExiting")
            save_transaction(transactions)
            break

        else:
            print("Invalid option. Try again")
if __name__ == "__main__":
    main()
