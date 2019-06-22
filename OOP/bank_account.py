class BankAccount:
    def __init__(self, int_rate, balance=0):
        self.int_rate = int_rate
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
        return self
    def withdraw(self, amount):
        if self.balance - amount < 0:
            print('Insufficient funds: Charging a $5 fee')
            self.balance -= 5
        else:
            self.balance -= amount
        return self
    def display_account_info(self):
        print(f"Balance ${self.balance}")
        return self
    def yield_interest(self):
        if self.balance > 0:
            mult = 1 + self.int_rate
            self.balance = self.balance * mult
            return self
        else:
            return self


amanda = BankAccount(0.05, 100).deposit(300).deposit(300).deposit(500).withdraw(100).yield_interest().display_account_info()
smalls = BankAccount(0.05).deposit(20).deposit(50).deposit(2).withdraw(100).withdraw(5).withdraw(5).withdraw(5).yield_interest().display_account_info()