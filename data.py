from os import path
import sqlite3
import hashlib

class DatabaseBuilder:
    """
    Creates a AuthDB and BalanceDB for testing purpose. 
    User data is given in userdata.txt
    """
    def __init__(self, config):
        self.userDataPath = config['user_data_path']
        self.authDBPath = config['auth_db_path']
        self.balanceDBPath = config['balance_db_path']
        self.setupDB()
        self.insertData()

    def connect(self, path):
        conn = sqlite3.connect(path, isolation_level=None)
        c = conn.cursor()
        return conn, c

    def close(self, conn):
        conn.commit()
        conn.close()
        return

    def setupDB(self):
        """
        Creates AuthDB and BalanceDB and set up each fields. 
        """
        self.setupAuthDB()
        self.setupBalanceDB()
        return

    def setupAuthDB(self):
        """
        Creates DB for authentification purpose. 
        Each table consists of cardNo: Card Number | pin: PIN for that card number. 
        """
        conn, c = self.connect(self.authDBPath)
        c.execute(
            "CREATE TABLE auth_data (cardNo integer PRIMARY KEY, pin TEXT)")
        self.close(conn)
        return

    def setupBalanceDB(self):
        """
        Creates DB storing user's balance in theire bank account. 
        """
        conn, c = self.connect(self.balanceDBPath)
        c.execute(
            "CREATE TABLE balance_data (id text PRIMARY KEY, balance INTEGER)")
        self.close(conn)
        return

    def insertData(self):
        """
        Given each triplets of data in a form [cardNumber, PIN, balance] in userdata.txt, 
        Writes each data into AuthDB and BalanceDB. 
        cardNumber | hash(PIN) goes into AuthDB
        hash(cardNumber+PIN) <- works as unique user ID | balance goes into BalanceDB
        """
        authDBconn, authDBcursor = self.connect(self.authDBPath)
        balanceDBconn, balanceDBcursor = self.connect(self.balanceDBPath)
        f = open(self.userDataPath, 'r')
        for line in f.readlines():
            cardNumber, PIN, balance = [int(i) for i in line.strip().split()]
            encodedPIN = hashlib.sha256(str(PIN).encode()).hexdigest()
            id = hashlib.sha256((str(cardNumber)+str(PIN)).encode()).hexdigest()
            authDBcursor.execute("INSERT INTO auth_data VALUES(?, ?)", [cardNumber, encodedPIN])
            balanceDBcursor.execute("INSERT INTO balance_data VALUES(?, ?)", [id, balance])
        self.close(authDBconn)
        self.close(balanceDBconn)
        return


class AuthDB:
    """
    Database for authentification purpose of user's card number and PIN. 
    """
    def __init__(self, path):
        self.path = path

    def connect(self):
        conn = sqlite3.connect(self.path, isolation_level=None)
        c = conn.cursor()
        return conn, c

    def close(self, conn):
        conn.commit()
        conn.close()
        return

    def checkCardNumber(self, cardNumber):
        """
        Given a card number, check if AuthDB has that card in DB.
        """
        conn, c = self.connect()
        c.execute("SELECT * FROM auth_data WHERE cardNo='%d'"% cardNumber)
        entry = c.fetchone()
        if entry is None:
            return False
        self.close(conn)
        return True

    def checkPIN(self, cardNumber, pin):
        """
        Given a cardNumber and a encoded pin, check if pin is correct for that card number. 
        """
        conn, c = self.connect()
        c.execute("SELECT pin FROM auth_data WHERE cardNo='%d'" % cardNumber)
        pinDB = c.fetchone()
        self.close(conn)
        return pin == pinDB[0]


class BalanceDB:
    """
    Database for storing balance of each user and updates it if necessary. 
    """
    def __init__(self, path):
        self.path = path

    def connect(self):
        conn = sqlite3.connect(self.path, isolation_level=None)
        c = conn.cursor()
        return conn, c

    def close(self, conn):
        conn.commit()
        conn.close()
        return
    
    def checkBalance(self, userID):
        """
        Checks user with userID's balance and return balance value. 
        """
        conn, c = self.connect()
        c.execute("SELECT balance FROM balance_data WHERE id='%s'" % userID)
        res = c.fetchone()
        self.close(conn)
        return res[0]
    
    def updateBalance(self, userID, amount):
        """
        Updates userID's balance by amount. 
        An amount can be positive, zero, or negative integers. 
        Invalid calls to updateBalance will not be made from ActionHandler module. 
        """
        conn, c = self.connect()
        currBalance = self.checkBalance(userID)
        c.execute("UPDATE balance_data SET balance=? WHERE id=?", (currBalance + amount, userID))
        self.close(conn)
        return 