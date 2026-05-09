from router.router import route
import os
from typing import *


def print_final_response(response: Dict[str, Any]) -> None:
    '''
    Print the final response in a readable format.
    Args:
        response (Dict[str, Any]): The final response to print.
    '''
    print("\nFinal Response:")
    for key, value in response.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")


def menu() -> None:
    '''
    Display the main menu and handle user navigation.
    Loops until the user chooses to exit.
    '''
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to the Smart Campus Service Request System!")
        print("1. Submit a new request")
        print("2. Exit")

        choice = input("Enter your choice (1-2): ").strip()
        while choice not in ["1", "2"]:
            print("Invalid choice. Please enter 1 or 2.")
            choice = input("Enter your choice (1-2): ").strip()

        if choice == "2":
            print("Thank you for using the Service Request System. Goodbye!")
            break

        final_response = route()
        print_final_response(final_response)
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    menu()