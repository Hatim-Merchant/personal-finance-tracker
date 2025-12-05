import json

transaction = {
    "amount": 10,
    "date": "2025-08-30",
    "category": "hobby",
    "type": "expense",
    "description": "tennis"}
transactions = []

#Add new transaction
transactions.append(transaction)

#New transaction
transactions.append({
    "amount": 20,
    "date": "2025-11-30",
    "category": "food",
    "type": "expense",
    "description": "lunch"
})
transactions.append({
    "amount": 300,
    "date": "2025-09-30",
    "category": "salary",
    "type": "income",
    "description": "salary"
})

transactions.append({
    "amount": 40,
    "date": "2025-08-10",
    "category": "food",
    "type": "expense",
    "description": "breakfast"
})
transactions.append({
    "amount": 30,
    "date": "2025-12-30",
    "category": "food",
    "type": "expense",
    "description": "dinner"
})


# Save to a file
with open("data.json", "w") as f:
    json.dump(transactions, f, indent=2)

print("Transactions saved!")

# Load from file
with open("data.json", "r") as f:
    loaded_transactions = json.load(f)

# Print each transaction
for t in loaded_transactions:
    print(t["date"], t["category"], t["amount"])

