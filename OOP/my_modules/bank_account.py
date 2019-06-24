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
        print("Balance ${}".format(self.balance))
        return self
    def yield_interest(self):
        if self.balance > 0:
            mult = 1 + self.int_rate
            self.balance = self.balance * mult
            return self
        else:
            return self

class CreateAccount:
    def __init__(self, type):
        self.account_type = type
        self.account = BankAccount(0.2)