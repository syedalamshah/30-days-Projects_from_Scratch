# Simple Personal Expense Tracker
# A beginner-friendly Python project demonstrating core concepts

import json
import datetime

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.categories = ["Food", "Transport", "Entertainment", "Bills", "Other"]
        self.load_expenses()
    
    def add_expense(self, amount, category, description=""):
        """Add a new expense"""
        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": str(datetime.date.today())
        }
        self.expenses.append(expense)
        self.save_expenses()
        print(f"Added: ${amount} - {category}")
    
    def view_expenses(self):
        """Display all expenses"""
        if not self.expenses:
            print("No expenses recorded.")
            return
        
        print("\nYour Expenses:")
        print("-" * 50)
        total = 0
        for i, expense in enumerate(self.expenses, 1):
            print(f"{i}. ${expense['amount']:.2f} - {expense['category']}")
            print(f"   {expense['date']} | {expense['description']}")
            total += expense['amount']
        print("-" * 50)
        print(f"Total: ${total:.2f}")
    
    def get_category_total(self):
        """Show spending by category"""
        if not self.expenses:
            print("No expenses to analyze.")
            return
        
        category_totals = {}
        for expense in self.expenses:
            category = expense['category']
            category_totals[category] = category_totals.get(category, 0) + expense['amount']
        
        print("\nSpending by Category:")
        for category, total in category_totals.items():
            print(f"{category}: ${total:.2f}")
    
    def save_expenses(self):
        """Save expenses to file"""
        try:
            with open("expenses.json", "w") as f:
                json.dump(self.expenses, f)
        except:
            print("Error saving expenses")
    
    def load_expenses(self):
        """Load expenses from file"""
        try:
            with open("expenses.json", "r") as f:
                self.expenses = json.load(f)
        except:
            self.expenses = []

def get_amount():
    """Get valid amount from user"""
    while True:
        try:
            amount = float(input("Enter amount: $"))
            if amount > 0:
                return amount
            print("Please enter a positive amount.")
        except ValueError:
            print("Please enter a valid number.")

def get_category(tracker):
    """Get category choice from user"""
    print("\nCategories:")
    for i, cat in enumerate(tracker.categories, 1):
        print(f"{i}. {cat}")
    
    while True:
        try:
            choice = int(input("Choose category (1-5): "))
            if 1 <= choice <= 5:
                return tracker.categories[choice-1]
            print("Please choose 1-5.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    """Main program"""
    tracker = ExpenseTracker()
    
    while True:
        print("\n--- EXPENSE TRACKER ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Category Summary")
        print("4. Exit")
        
        choice = input("Choose (1-4): ")
        
        if choice == "1":
            amount = get_amount()
            category = get_category(tracker)
            description = input("Description (optional): ")
            tracker.add_expense(amount, category, description)
        
        elif choice == "2":
            tracker.view_expenses()
        
        elif choice == "3":
            tracker.get_category_total()
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()