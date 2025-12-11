class BankAccount:
    def __init__(self, balance):
        # Using a single underscore indicates a "protected" attribute
        # By convention, it's a hint not to access directly
        self._balance = balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited {amount}. New balance: {self._balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            print(f"Withdrew {amount}. New balance: {self._balance}")
        else:
            print("Invalid withdrawal amount or insufficient funds.")

    def get_balance(self):
        return self._balance


# Usage
account = BankAccount(1000)
account.deposit(500)
account.withdraw(200)
# Direct access is discouraged, but Python doesn't strictly prevent it
# account._balance = -500 # This would break encapsulation principles
print(f"Current balance: {account.get_balance()}")
