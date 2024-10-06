from dataclasses import dataclass, field
import os
import textwrap

def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        

def main_menu() -> tuple[int,str]:
    clear_screen()
    menu: str = """
    ================= Main Menu =================

    [1]\tDeposit
    [2]\tWithdraw
    [3]\tStatement
    [4]\tNew Account
    [5]\tList Accounts
    [6]\tNew User
    [7]\tExit

    ============================================
    """

    print(textwrap.dedent(menu))

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
    stmnt = "=============== Statement =================\n"
    stmnt += "\n".join(operations) if operations else "No operations to display."
    stmnt += f"\n\nBalance:\t${balance:.2f}"
    stmnt += "\n==========================================="

    print(stmnt)

@dataclass
class Account:
    cpf: str
    agency: str
    number: int

@dataclass
class User:
    name: str
    cpf: str
    address: str
    date_of_birth: str
    accounts: list[Account] = field(default_factory=list)

def new_user(users: dict[str, User]) -> None:
    cpf = input("Enter CPF: ")

    if cpf in users:
        print("User already exists.")
        return

    name = input("Enter full name: ")
    address = input("Enter full address: ")
    date_of_birth = input("Enter date of birth (yyyy-mm-dd): ")

    user = User(name, cpf, address, date_of_birth)
    users[cpf] = user

    print("User created successfully.")

def new_account(users: dict[str, User], accounts: list[Account]) -> None:
    AGENCY: str = "0001"

    cpf = input("Enter CPF: ")

    if cpf not in users:
        print("User not found.")
        return

    user = users[cpf]
    account = Account(cpf, AGENCY, len(accounts) + 1)
    user.accounts.append(account)
    accounts.append(account)

    print("Account created successfully.")

def list_accounts(accounts: list[Account]) -> None:
    if not accounts:
        print("No accounts to display.")
        return

    for account in accounts:
        line = f"""
        ================= Account =================
        Owner:\t\t\t {account.cpf}
        Agency:\t\t\t {account.agency}
        Account Number:\t\t {account.number}
        ===========================================
        """
        print(textwrap.dedent(line))

def main() -> None:
    balance: float = 0.0
    withdrawals: int = 0
    operations: list[str] = []

    users: dict[str, User] = {}
    accounts: list[Account] = []

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
                new_account(users, accounts)
            case 5:
                list_accounts(accounts)
            case 6:
                new_user(users)
            case 7:
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