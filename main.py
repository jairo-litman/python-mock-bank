import os

def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        

def main_menu() -> tuple[int,str]:
    clear_screen()
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Statement")
    print("4. Exit")

    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        return -1, "Invalid choice. Please enter a number."
    
    return choice, ""


def deposit(balance: float, operations: list[str]) -> float:
    try:
        amount = float(input("Enter amount to deposit: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return balance
    
    if amount < 0:
        print("Invalid amount. Please enter a positive number.")
        return balance
    
    balance += amount

    operation: str = f"Deposited ${amount:.2f}, new balance: ${balance:.2f}"
    operations.append(operation)
    print(operation)

    return balance


def validate_withdrawal(amount: float, balance: float, withdrawals: int) -> tuple[bool, str]:
    LIMIT: float = 500.0
    MAX_WITHDRAWALS: int = 3

    if amount < 0:
        return False, "Invalid amount. Please enter a positive number."
    
    if amount > balance:
        return False, "Insufficient funds."
    
    if amount > LIMIT:
        return False, "Exceeded withdrawal limit."
    
    if withdrawals >= MAX_WITHDRAWALS:
        return False, "Exceeded maximum number of withdrawals."
    
    return True, ""
    
def withdraw(balance: float, withdrawals: int, operations: list[str]) -> float:
    try:
        amount = float(input("Enter amount to withdraw: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return balance
    
    valid, message = validate_withdrawal(amount, balance, withdrawals)
    if not valid:
        print(message)
        return balance
    
    balance -= amount
    withdrawals += 1

    operation: str = f"Withdrew ${amount:.2f}, new balance: ${balance:.2f}"
    operations.append(operation)
    print(operation)

    return balance

def statement(balance: float, operations: list[str]) -> None:
    print("=== Statement ===")
    for operation in operations:
        print(operation)
    print(f"\nBalance: ${balance:.2f}")
    print("=================")
    

def main() -> None:
    balance: float = 0.0
    withdrawals: int = 0
    operations: list[str] = []

    while True:
        choice, message = main_menu()

        clear_screen()
        match choice:
            case 1:
                balance = deposit(balance, operations)
            case 2:
                balance = withdraw(balance, withdrawals, operations)
            case 3:
                statement(balance, operations)
            case 4:
                break
            case -1:
                print(message)
                pass
            case _:
                print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")

    print("Thank you, goodbye!")
    

if __name__ == "__main__":
    main()