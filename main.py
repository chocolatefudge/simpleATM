from auth import Authenticator
from action import ActionHandler
from data import AuthDB, BalanceDB
import hashlib
import json


class User:
    """
    User Class which contains a card number and hashed value of PIN. 
    """
    def __init__(self, cardNumber = -1):
        self.cardNumber = int(cardNumber)
        self.id = None # Hashed value of str(cardNumber) + str(pin)

class SimpleATM:
    """
    Main ATM Class that has connections to databases and handles user actions. 
    """
    def __init__(self, config):
        """
        Initializing procedures for SimpleATM. 
        First, it gets connections to AuthDB and BalanceDB. 
        After that, Authenticator and ActionHandler is initialized to handle user actions. 
        """
        self.authDB = AuthDB(config['auth_db_path'])
        self.balanceDB = BalanceDB(config['balance_db_path'])
        self.authenticator = Authenticator(self.authDB)
        self.actionHandler = ActionHandler(self.balanceDB)
        self.currentUser = None

    def handle(self, request):
        """
        Recieves a single user requests and executes necessary functions depending on request's type. 
        """
        parsedRequest = request.strip().split()
        requestType = parsedRequest[0]
        requestContent = None
        if len(parsedRequest) > 1:
            requestContent = int(parsedRequest[1])
        if requestType == "CARDINSERT":
            self.registerUser(requestContent)
        elif requestType == "AUTH":
            self.authenticateUser(requestContent)
        elif requestType in ["BALANCE", "DEPOSIT", "WITHDRAW"]:
            self.processAction(requestType, requestContent)
        elif requestType == "EXIT":
            self.removeUser()
        else:
            return 0

    def removeUser(self):
        """
        Removes a current user from SimpleATM, Authenticator, and ActionHandler.
        Executed when session with current user is ended. 
        """
        if self.currentUser:
            self.authenticator.removeUser()
            self.actionHandler.removeUser()
            self.currentUser = None
            print("Session has ended.")

    def registerUser(self, cardNumber):
        """
        Register a user to SimpleATM and Authenticator. 
        Registering means that user has a card that is stored in database. 
        User might be registered but hasn't been authenticated yet. 
        """
        if self.authenticator.checkCardNumber(cardNumber):
            self.currentUser = User(cardNumber)
            self.authenticator.addUser(self.currentUser)
            return True
        else:
            return False

    def authenticateUser(self, pin):
        """
        Recieves a PIN from a user, encodes it with SHA256 hash function.
        Then compares with hashed PIN value that is stored in AuthDB. 
        This process is matched with Bank API that verifies a user's PIN. 
        If user is authenticated, 
        """
        encodedPIN = hashlib.sha256(str(pin).encode()).hexdigest()
        if self.authenticator.authenticate(encodedPIN):
            self.currentUser.id = hashlib.sha256((str(self.currentUser.cardNumber)+str(pin)).encode()).hexdigest()
            self.actionHandler.addUser(self.currentUser)
            return True
        else:
            if self.authenticator.currentUser is None: # PIN is incorrect for >=5 times. 
                self.removeUser()
            return False

    def hasAuthenticatedUser(self):
        """
        Helper function for checking if user is authenticated. 
        """
        return self.actionHandler.currentUser is not None

    def processAction(self, actionType, actionContent):
        """
        If user is not authenticated, user cannot perform any of the actions. 
        If user is authenticated, calls necessary action handler for each of the aciton. 
        """
        if not self.hasAuthenticatedUser():
            return
        if actionType == "BALANCE":
            self.actionHandler.checkBalance(checkPurpose=True)
        elif actionType == "DEPOSIT":
            self.actionHandler.deposit(actionContent)
        else:
            self.actionHandler.withdraw(actionContent)

def main():
    """
    Opens a config.json file and initialize a SimpleATM.
    Opens a test.txt file and execute command line by line until ends. 
    """
    with open('config.json') as f:
        config = json.load(f)
    atm = SimpleATM(config)
    f = open(config["test_file_path"], 'r')
    lines = f.readlines()
    for line in lines:
        atm.handle(line)
    return


if __name__ == "__main__":
    main()