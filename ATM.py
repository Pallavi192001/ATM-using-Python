import mysql.connector
from datetime import datetime

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root123',
    database='atm'
)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Account_Number VARCHAR(255) NOT NULL,
        PIN VARCHAR(4) NOT NULL,
        balance FLOAT NOT NULL
    )
''')
conn.commit()

# Sample data for testing
cursor.execute('''
    INSERT INTO accounts (Account_Number, PIN, balance)
    VALUES ('123456789', '1234', 1000.0), ('987654321', '5678', 2000.0)
''')
conn.commit()

# ATM functions
def display_menu():
    print("1. Create Account")
    print("2. Login")
    print("3. Quit")

def create_account():
    account_number = input("Enter account number: ")
    pin = input("Enter 4-digit PIN: ")
    balance = float(input("Enter initial balance: "))

    cursor.execute("INSERT INTO accounts (Account_Number, PIN, balance) VALUES (%s, %s, %s)", (account_number, pin, balance))
    conn.commit()
    print("Account created successfully.")

def login():
    account_number = input("Enter account number: ")
    pin = input("Enter PIN: ")

    cursor.execute("SELECT * FROM accounts WHERE Account_Number=%s AND PIN=%s", (account_number, pin))
    account = cursor.fetchone()

    if account:
        print("Login successful.")
        while True:
            display_logged_in_menu()
            choice = input("Enter choice (1-4): ")

            if choice == '1':
                check_balance(account_number)
            elif choice == '2':
                amount = float(input("Enter withdrawal amount: "))
                withdraw(account_number, amount)
            elif choice == '3':
                amount = float(input("Enter deposit amount: "))
                deposit(account_number, amount)
            elif choice == '4':
                break
            else:
                print("Invalid choice.")
    else:
        print("Login failed. Invalid account number or PIN.")

def display_logged_in_menu():
    print("1. Check Balance")
    print("2. Withdraw")
    print("3. Deposit")
    print("4. Logout")

def check_balance(account_number):
    cursor.execute("SELECT balance FROM accounts WHERE Account_Number=%s", (account_number,))
    balance = cursor.fetchone()[0]
    print(f"Account Balance: {balance}")
    print_transaction_details(account_number, "Balance Check")

def withdraw(account_number, amount):
    cursor.execute("SELECT balance FROM accounts WHERE Account_Number=%s", (account_number,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        new_balance = balance - amount
        cursor.execute("UPDATE accounts SET balance=%s WHERE Account_Number=%s", (new_balance, account_number))
        conn.commit()
        print(f"Withdrawal successful. New Balance: {new_balance}")
        print_transaction_details(account_number, "Withdrawal")
    else:
        print("Insufficient balance.")

def deposit(account_number, amount):
    cursor.execute("SELECT balance FROM accounts WHERE Account_Number=%s", (account_number,))
    balance = cursor.fetchone()[0]

    new_balance = balance + amount
    cursor.execute("UPDATE accounts SET balance=%s WHERE Account_Number=%s", (new_balance, account_number))
    conn.commit()
    print(f"Deposit successful. New Balance: {new_balance}")
    print_transaction_details(account_number, "Deposit")

def print_transaction_details(account_number, transaction_type):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Transaction Time: {timestamp}")
    print(f"Account Number: {account_number}")
    print(f"Transaction Type: {transaction_type}")
    print()

# Main program loop
while True:
    display_menu()
    choice = input("Enter choice (1-3): ")

    if choice == '1':
        create_account()
    elif choice == '2':
        login()
    elif choice == '3':
        break
    else:
        print("Invalid choice.")

# Close the database connection
conn.close()
