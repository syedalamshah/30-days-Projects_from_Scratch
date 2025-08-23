import json
import os

class InventoryTracker:
    def __init__(self, filename="inventory.json"):
        self.filename = filename
        self.inventory = {}
        self.load_inventory()

    def load_inventory(self):
        """Load inventory from file if it exists"""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    self.inventory = json.load(f)
                except json.JSONDecodeError:
                    self.inventory = {}
        else:
            self.inventory = {}

    def save_inventory(self):
        """Save current inventory to file"""
        with open(self.filename, "w") as f:
            json.dump(self.inventory, f, indent=4)

    def add_item(self, item, quantity):
        """Add an item to inventory"""
        item = item.lower()
        self.inventory[item] = self.inventory.get(item, 0) + quantity
        self.save_inventory()
        print(f"✅ Added {quantity} {item}(s).")

    def remove_item(self, item, quantity):
        """Remove an item from inventory"""
        item = item.lower()
        if item in self.inventory:
            if self.inventory[item] >= quantity:
                self.inventory[item] -= quantity
                if self.inventory[item] == 0:
                    del self.inventory[item]
                self.save_inventory()
                print(f"✅ Removed {quantity} {item}(s).")
            else:
                print("⚠️ Not enough items in stock!")
        else:
            print("⚠️ Item not found!")

    def show_inventory(self):
        """Display current inventory"""
        if not self.inventory:
            print("📦 Inventory is empty.")
        else:
            print("\n--- Current Inventory ---")
            for item, qty in self.inventory.items():
                print(f"{item.capitalize()} : {qty}")
            print("--------------------------")

    def search_item(self, item):
        """Search for a specific item"""
        item = item.lower()
        if item in self.inventory:
            print(f"🔍 Found: {item.capitalize()} → Quantity: {self.inventory[item]}")
        else:
            print("❌ Item not found in inventory.")

    def clear_inventory(self):
        """Delete all inventory"""
        confirm = input("⚠️ Are you sure you want to clear the entire inventory? (yes/no): ").lower()
        if confirm == "yes":
            self.inventory = {}
            self.save_inventory()
            print("🗑️ All inventory cleared.")
        else:
            print("❌ Clear action cancelled.")

    def total_items(self):
        """Show total number of items"""
        total = sum(self.inventory.values())
        print(f"📊 Total items in stock: {total}")


def main():
    tracker = InventoryTracker()

    while True:
        print("\n--- Inventory Menu ---")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Show Inventory")
        print("4. Search Item")
        print("5. Clear Inventory")
        print("6. Total Items Count")
        print("7. Exit")

        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            item = input("Enter item name: ").strip()
            try:
                quantity = int(input("Enter quantity: "))
                tracker.add_item(item, quantity)
            except ValueError:
                print("⚠️ Quantity must be a number!")

        elif choice == "2":
            item = input("Enter item name: ").strip()
            try:
                quantity = int(input("Enter quantity: "))
                tracker.remove_item(item, quantity)
            except ValueError:
                print("⚠️ Quantity must be a number!")

        elif choice == "3":
            tracker.show_inventory()

        elif choice == "4":
            item = input("Enter item name to search: ").strip()
            tracker.search_item(item)

        elif choice == "5":
            tracker.clear_inventory()

        elif choice == "6":
            tracker.total_items()

        elif choice == "7":
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("⚠️ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
