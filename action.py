class ActionHandler:
    """
    ActionHandler handles user's 3 possible action which is checkBalance, deposit, and withdraw. 
    """
    def __init__(self, balanceDB):
        self.name = "a"
        self.currentUser = None
        self.db = balanceDB

    def addUser(self, user):
        self.currentUser = user

    def removeUser(self):
        self.currentUser = None

    def checkBalance(self, checkPurpose = False):
        """
        Checks current balance of the self.currentUser.
        """
        if checkPurpose:
            print("Check current balance")
        balance = self.db.checkBalance(self.currentUser.id)
        print("Current balance: %d" % balance)
        return balance

    def deposit(self, amount):
        """
        Deposit amount of money to the back account. 
        There is no upper bound of money that can be deposit.
        """
        print("Deposit %d" % amount)
        balance = self.checkBalance()
        self.db.updateBalance(self.currentUser.id, amount)
        print("Updated balance: %d" % (balance + amount))
        return True

    def withdraw(self, amount):
        """
        Tries to withdraw amount of money. 
        If there's not enough balance, withdraw request will be invalidated and balance will remain the same. 
        """
        print("Withdraw %d" % amount)
        balance = self.checkBalance()
        if balance >= amount:
            self.db.updateBalance(self.currentUser.id, -amount)
            print("Updated balance: %d" % (balance - amount))
            return True
        else:
            print("Not enough balance")
            return False