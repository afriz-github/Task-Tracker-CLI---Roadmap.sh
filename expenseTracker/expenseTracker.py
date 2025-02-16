#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime

# Nama file untuk menyimpan data expense
EXPENSES_FILE = "expenses.json"


def load_expenses():
    """Membaca data expenses dari file JSON."""
    if not os.path.exists(EXPENSES_FILE):
        return []
    with open(EXPENSES_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_expenses(expenses):
    """Menyimpan data expenses ke file JSON."""
    with open(EXPENSES_FILE, "w") as f:
        json.dump(expenses, f, indent=4)


def add_expense(description, amount):
    """Menambahkan expense baru."""
    expenses = load_expenses()
    # Menghasilkan ID baru dengan mencari ID terbesar dan menambah 1
    new_id = max([expense["id"] for expense in expenses], default=0) + 1
    expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")


def update_expense(expense_id, description, amount):
    """Memperbarui expense yang sudah ada."""
    expenses = load_expenses()
    for expense in expenses:
        if expense["id"] == expense_id:
            if description is not None:
                expense["description"] = description
            if amount is not None:
                expense["amount"] = amount
            save_expenses(expenses)
            print("Expense updated successfully")
            return
    print("Expense with given ID not found")


def delete_expense(expense_id):
    """Menghapus expense berdasarkan ID."""
    expenses = load_expenses()
    new_expenses = [expense for expense in expenses if expense["id"] != expense_id]
    if len(new_expenses) == len(expenses):
        print("Expense with given ID not found")
    else:
        save_expenses(new_expenses)
        print("Expense deleted successfully")


def list_expenses():
    """Menampilkan daftar semua expense."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    print("ID  Date       Description       Amount")
    print("--  ---------- ----------------- ------")
    for expense in expenses:
        # Format output: ID, Date, Description, dan Amount
        print(f'{expense["id"]: <3}{expense["date"]: <12}{expense["description"]: <20}${expense["amount"]:.2f}')


def summary_expenses(month=None):
    """Menampilkan ringkasan total expenses.
    
    Jika parameter month diisi (angka 1-12), maka akan menampilkan total expense untuk bulan tersebut.
    """
    expenses = load_expenses()
    if month:
        try:
            month = int(month)
            filtered = [
                e for e in expenses
                if datetime.strptime(e["date"], "%Y-%m-%d").month == month
            ]
            total = sum(e["amount"] for e in filtered)
            month_name = datetime(1900, month, 1).strftime("%B")
            print(f"Total expenses for {month_name}: ${total:.2f}")
        except ValueError:
            print("Invalid month")
    else:
        total = sum(e["amount"] for e in expenses)
        print(f"Total expenses: ${total:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="Expense Tracker Application"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: add
    parser_add = subparsers.add_parser("add", help="Add an expense")
    parser_add.add_argument("--description", required=True, help="Expense description")
    parser_add.add_argument("--amount", required=True, type=float, help="Expense amount")

    # Command: update
    parser_update = subparsers.add_parser("update", help="Update an expense")
    parser_update.add_argument("--id", required=True, type=int, help="Expense ID")
    parser_update.add_argument("--description", help="Updated description")
    parser_update.add_argument("--amount", type=float, help="Updated amount")

    # Command: delete
    parser_delete = subparsers.add_parser("delete", help="Delete an expense")
    parser_delete.add_argument("--id", required=True, type=int, help="Expense ID")

    # Command: list
    subparsers.add_parser("list", help="List all expenses")

    # Command: summary
    parser_summary = subparsers.add_parser("summary", help="Show expenses summary")
    parser_summary.add_argument("--month", help="Month number (1-12) for summary of specific month")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        summary_expenses(args.month)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
