import argparse
import json
import os
from datetime import datetime

FILE_NAME = "expenses.json"


# ----------------------------
# File Handling Functions
# ----------------------------
def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# ----------------------------
# Core Features
# ----------------------------
def add_expense(description, amount):
    expenses = load_expenses()

    if amount <= 0:
        print("Amount must be greater than 0.")
        return

    expense_id = 1 if not expenses else expenses[-1]["id"] + 1

    new_expense = {
        "id": expense_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount,
    }

    expenses.append(new_expense)
    save_expenses(expenses)

    print(f"Expense added successfully (ID: {expense_id})")


def list_expenses():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.")
        return

    print("ID  Date       Description       Amount")
    print("----------------------------------------")

    for expense in expenses:
        print(
            f'{expense["id"]:<3} {expense["date"]:<10} {expense["description"]:<15} ${expense["amount"]}'
        )


def summary(month=None):
    expenses = load_expenses()

    if month:
        total = sum(
            expense["amount"]
            for expense in expenses
            if datetime.strptime(expense["date"], "%Y-%m-%d").month == month
        )
        print(f"Total expenses for month {month}: ${total}")
    else:
        total = sum(expense["amount"] for expense in expenses)
        print(f"Total expenses: ${total}")


def update_expense(expense_id, description=None, amount=None):
    expenses = load_expenses()

    for expense in expenses:
        if expense["id"] == expense_id:
            if description:
                expense["description"] = description

            if amount is not None:
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    return
                expense["amount"] = amount

            save_expenses(expenses)
            print("Expense updated successfully")
            return

    print("Expense ID not found.")


def delete_expense(expense_id):
    expenses = load_expenses()

    updated_expenses = [expense for expense in expenses if expense["id"] != expense_id]

    if len(updated_expenses) == len(expenses):
        print("Expense ID not found.")
        return

    save_expenses(updated_expenses)
    print("Expense deleted successfully")


# ----------------------------
# Main CLI
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True)

    # List command
    subparsers.add_parser("list")

    # Summary command
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", type=int)

    # Update command
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", type=int, required=True)
    update_parser.add_argument("--description")
    update_parser.add_argument("--amount", type=float)

    # Delete command
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)

    elif args.command == "list":
        list_expenses()

    elif args.command == "summary":
        summary(args.month)

    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)

    elif args.command == "delete":
        delete_expense(args.id)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()