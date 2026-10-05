import csv
import os
from datetime import date

FILE_NAME = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, newline="") as f:
        return list(csv.DictReader(f))


def save_expenses(expenses):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def add_expense():
    category = input("Category (Food/Travel/Shopping/Bills/Other): ").strip().title()
    description = input("Description: ").strip()
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    expenses = load_expenses()
    expenses.append({
        "date": str(date.today()),
        "category": category,
        "description": description,
        "amount": amount,
    })
    save_expenses(expenses)
    print("Expense added!")


def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses yet.")
        return False
    print(f"\n{'No':<4}{'Date':<12}{'Category':<12}{'Description':<22}{'Amount':>10}")
    print("-" * 60)
    for i, e in enumerate(expenses, start=1):
        print(f"{i:<4}{e['date']:<12}{e['category']:<12}{e['description']:<22}{float(e['amount']):>10.2f}")
    return True


def show_summary():
    expenses = load_expenses()
    if not expenses:
        print("No expenses yet.")
        return
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + float(e["amount"])
    print("\nCategory-wise spending")
    print("-" * 22)
    for category, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f"{category:<12}{total:>10.2f}")
    print("-" * 22)
    print(f"{'Total':<12}{sum(totals.values()):>10.2f}")


def delete_expense():
    if not view_expenses():
        return
    expenses = load_expenses()
    try:
        number = int(input("Enter expense number to delete: "))
        removed = expenses.pop(number - 1)
    except (ValueError, IndexError):
        print("Invalid number.")
        return
    save_expenses(expenses)
    print(f"Deleted: {removed['description']}")


def main():
    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category-wise Summary")
        print("4. Delete Expense")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
