import json
import os
from datetime import datetime as dt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "transactions.json")

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
        
#Implementing transaction adding function
def add_transactions(transactions):

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
                # Try parsing the month
                dt.strptime(month, "%Y-%m")
                break  # valid format
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
        for category, amount in income_by_category.items():
            print(f"{category}: {amount}")
        print("Total Income:",total_income)

        print("\nExpense by Category:")
        for category, amount in expense_by_category.items():
            print(f"{category}: {amount}")
        print("Total Expense:", total_expense)
        
        print(f"\nFinal Balance of {month} is: {balance}")

    elif choice == "3":
        return
    else:
        print("Invalid option. Try again")

#Main Menu
def main():
    transactions = load_transaction()

    while True:
        print("\n---Personal Finance Tracker---\n")
        print("1. Add")
        print("2. List Transactions")
        print("3. Show Summary")
        print("4. Exit")
        

        choice = input("\nSelect from Menu: ")

        if choice == "1":
            add_transactions(transactions)
        elif choice == "2":
            list_transactions(transactions)
        elif choice =="3":
            show_summary(transactions)
        elif choice == "4":
            print("\nExiting")
            save_transaction(transactions)
            break

        else:
            print("Invalid option. Try again")
if __name__ == "__main__":
    main()
