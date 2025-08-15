# Simple Contact Book for Python Beginners
# Uses only basic concepts: variables, lists, dictionaries, functions, loops

# Store contacts in a list of dictionaries
contacts = []

def show_menu():
    """Display the main menu"""
    print("\n" + "="*30)
    print("    CONTACT BOOK")
    print("="*30)
    print("1. Add Contact")
    print("2. Show All Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")
    print("="*30)

def add_contact():
    """Add a new contact"""
    print("\n--- Add New Contact ---")
    
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    
    # Create a dictionary for this contact
    new_contact = {
        "name": name,
        "phone": phone
    }
    
    # Add to our list
    contacts.append(new_contact)
    print(f"Added {name} to contacts!")

def show_all_contacts():
    """Show all contacts"""
    if len(contacts) == 0:
        print("\nNo contacts found!")
        return
    
    print("\n--- All Contacts ---")
    for i in range(len(contacts)):
        contact = contacts[i]
        print(f"{i+1}. {contact['name']} - {contact['phone']}")

def search_contact():
    """Search for a contact by name"""
    if len(contacts) == 0:
        print("\nNo contacts to search!")
        return
    
    search_name = input("\nEnter name to search: ")
    
    found = False
    for contact in contacts:
        if contact["name"].lower() == search_name.lower():
            print(f"\nFound: {contact['name']} - {contact['phone']}")
            found = True
            break
    
    if not found:
        print(f"Contact '{search_name}' not found!")

def delete_contact():
    """Delete a contact"""
    if len(contacts) == 0:
        print("\nNo contacts to delete!")
        return
    
    # Show all contacts first
    show_all_contacts()
    
    try:
        choice = int(input("\nEnter contact number to delete: "))
        
        if choice >= 1 and choice <= len(contacts):
            removed_contact = contacts.pop(choice - 1)
            print(f"Deleted {removed_contact['name']} from contacts!")
        else:
            print("Invalid contact number!")
            
    except ValueError:
        print("Please enter a valid number!")

def main():
    """Main program"""
    print("Welcome to Contact Book!")
    
    while True:
        show_menu()
        
        try:
            choice = int(input("Choose option (1-5): "))
            
            if choice == 1:
                add_contact()
            elif choice == 2:
                show_all_contacts()
            elif choice == 3:
                search_contact()
            elif choice == 4:
                delete_contact()
            elif choice == 5:
                print("\nGoodbye!")
                break
            else:
                print("Please choose 1-5 only!")
                
        except ValueError:
            print("Please enter a number!")
        
        # Wait before showing menu again
        input("\nPress Enter to continue...")

# Start the program
main()


# LEARNING NOTES FOR BEGINNERS:
# --------------------------------
# 1. VARIABLES: contacts = [] creates a list
# 2. DICTIONARIES: {"name": "John", "phone": "123"} stores key-value pairs
# 3. LISTS: contacts.append() adds items, contacts.pop() removes items
# 4. FUNCTIONS: def function_name(): creates reusable code blocks
# 5. LOOPS: for loop goes through each item, while loop repeats until condition
# 6. CONDITIONALS: if/elif/else makes decisions
# 7. INPUT/OUTPUT: input() gets user input, print() shows output
# 8. TRY/EXCEPT: handles errors when user enters wrong input
# 9. STRING METHODS: .lower() makes text lowercase for comparison
# 10. LIST METHODS: len() gets length, range() creates number sequences