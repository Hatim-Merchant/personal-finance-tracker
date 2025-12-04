import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "transactions.json")


def load_transaction():
    if not os.path.exists(DATA_FILE):
        return[]
    with open (DATA_FILE, "r") as f:
        return json.load(f)

def save_transaction(transactions):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2)
    
def add_transactions(transactions):

    print("\n---Add Transaction---\n")

    amount = float(input("\nAmount: "))
    date = input("\nDate: ")
    category = input("\nCategory: ")
    type = input("Type(income or expense): ")
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

#Main Menu
def main():
    transactions = load_transaction()

    while True:
        print("\n---Personal Finance Tracker---\n")
        print("1. Add")
        print("2. List Transactions")
        print ("3. Exit")

        choice = input("\nSelect from Menu:")

        if choice == "1":
            add_transactions(transactions)
        elif choice == "2":
            print("\nShowing transactions..")
        elif choice == "3":
            print("\nExiting")
            save_transaction(transactions)
            break

        else:
            print("Invalid option. Try again")
if __name__ == "__main__":
    main()
