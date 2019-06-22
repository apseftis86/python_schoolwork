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

class CreateAccount:
    def __init__(self, type):
        self.account_type = type
        self.account = BankAccount(0.2)

class User:
    def __init__(self, name, email, type=None):
        self.name = name
        self.email = email
        if type:
            self.accounts = []
            for x in range(0, len(type)):
                self.accounts.append(CreateAccount(type[x]))

    def make_deposit(self, account, amount):
        self.accounts[account].account.deposit(amount)
        return self
    def withdraw_money(self, amount):
        self.accounts[account].account.withdraw(amount)
        return self
    def transfer_money(self, transfer_to, amount):
        self[account].withdraw(amount)
        transfer_to.self[account].deposit(amount)
        return self

    def display_user_balance(self, account):
        self.accounts[account].account.display_account_info()
        return self
    def add_account(self, type):
        for x in range(0, len(type)):
            self.accounts.append(CreateAccount(type[x]))

amanda = User('Amanda', 'apseftis@me.com', ['checking', 'savings'])
amanda.add_account(['college_fund'])
print(len(amanda.accounts))
amanda.make_deposit(0, 100).display_user_balance(0).make_deposit(2, 400).display_user_balance(2)
