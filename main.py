from router.router import route 

def menu():
    print("Welcome to the Service Request System!")
    print("1. Submit a new request")
    print("2. Exit")
    choice = input("Enter your choice (1-2): ").strip()
    while choice not in ["1", "2"]:
        print("Invalid choice. Please enter 1 or 2.")
        choice = input("Enter your choice (1-2): ").strip()
    if choice == "1":
        route()
    else:
        print("Thank you for using the Service Request System. Goodbye!")

if __name__ == "__main__":
    menu() 