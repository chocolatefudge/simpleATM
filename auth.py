
class Authenticator:
    """
    Authenticator part that handles authentication part of the SimpleATM
    """
    def __init__(self, authDB):
        self.name = "a"
        self.db = authDB
        self.currentUser = None
        self.currentWrongCnt = 0

    def addUser(self, user):
        """
        Adds user to current user. 
        """
        self.currentUser = user

    def removeUser(self):
        """
        Remove current user and initialize PIN wrong count. 
        """
        self.currentUser = None
        self.currentWrongCnt = 0

    def checkCardNumber(self, cardNumber):
        """
        Checks given card number and check if card number is in AuthDB. 
        """
        if self.db.checkCardNumber(int(cardNumber)):
            print("Card number is found.")
            return True
        else:
            print("Unknown card number.")
            return False

    def authenticate(self, pin):
        """
        Checks if given PIN is correct PIN for current user's card number. 
        If not, currentWrongCnt is incremented.
        If user types in wrong PIN for more than 5 times, user gets removed from system. 
        """
        if not self.db.checkPIN(self.currentUser.cardNumber, pin):
            self.currentWrongCnt += 1
            print("Password incorrect for %d/5 times" % self.currentWrongCnt)
            if self.currentWrongCnt >= 5:
                self.removeUser()
            return False
        else:
            print("Correct password")
            return True