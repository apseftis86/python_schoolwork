from my_modules.bank_account import BankAccount, CreateAccount


class User:
    def __init__(self, name, email, *types):
        self.name = name
        self.email = email
        self.accounts = []
        for type in types:
            self.add_account(type)

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
        self.accounts.append(CreateAccount(type))

amanda = User('Amanda', 'apseftis@me.com', 'checking', 'savings', 'college_fund')
print(amanda.accounts[2].account_type)
