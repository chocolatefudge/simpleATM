import os, json
from data import DatabaseBuilder

class Builder:
    """
    Builder class builds necessary databases to test our SimpleATM. 
    This process is not necessary in real world if database is stored in bank's main system
    and each ATM can have access to main database. 
    """
    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)
        self.setUpPath()
        self.setUpDatabase()
        
    def setUpPath(self):
        """
        Make necessary directory if it doesn't exists. 
        Remove database files if exists. 
        """
        os.makedirs(self.config['data_dir'], exist_ok=True)
        if os.path.isfile(self.config['auth_db_path']):
            os.remove(self.config['auth_db_path'])
        if os.path.isfile(self.config['balance_db_path']):
            os.remove(self.config['balance_db_path'])

    def setUpDatabase(self):
        """
        Build a new tatabase from userdata.txt
        """
        DatabaseBuilder(self.config)


if __name__== "__main__":
    Builder()