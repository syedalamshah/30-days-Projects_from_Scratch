# Multi-Pattern Generator in Python
# -------------------------------

# Function to print right-angled triangle
def right_angled_triangle(rows):
    for i in range(1, rows + 1):
        for j in range(1, i + 1):
            print("*", end=" ")
        print()

# Function to print inverted triangle
def inverted_triangle(rows):
    for i in range(rows, 0, -1):
        for j in range(i):
            print("*", end=" ")
        print()

# Function to print pyramid
def pyramid(rows):
    for i in range(1, rows + 1):
        # Print spaces
        for space in range(rows - i):
            print(" ", end=" ")
        # Print stars
        for star in range(2 * i - 1):
            print("*", end=" ")
        print()

# Function to print number triangle
def number_triangle(rows):
    for i in range(1, rows + 1):
        for j in range(1, i + 1):
            print(j, end=" ")
        print()


# Main program starts here
print("Welcome to the Pattern Generator!")
print("Choose a pattern to print:")
print("1. Right-Angled Triangle")
print("2. Inverted Triangle")
print("3. Pyramid")
print("4. Number Triangle")

# Input: pattern type
choice = input("Enter your choice (1-4): ")

# Input: number of rows
rows = int(input("Enter the number of rows: "))

# Run the chosen pattern function
if choice == "1":
    right_angled_triangle(rows)
elif choice == "2":
    inverted_triangle(rows)
elif choice == "3":
    pyramid(rows)
elif choice == "4":
    number_triangle(rows)
else:
    print("Invalid choice. Please select a number between 1 and 4.")
