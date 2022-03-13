# SimpleATM
Online Assessment project for Bear Robotics. 

## Introduction 
SimpleATM is a simplified version of ATM (Automatic Teller Machine) that supports card insertion, PIN checking, check balance, deposit, and withdrawal. This is not integrated with real-world ATM or bank systems but can be integrated in the future. Note that some of the real-world problems or edge cases are not illustrated fully on SimpleATM. 

## Structure
Project directory is as follows: 

	\actions.py
    \auth.py
    \bulid.py
    \data.py
    \main.py
    \README.md
    \test.txt
    \userdata.txt

## Gettign Started
### How to install
1. Clone the repo. 
   ```sh
   git clone https://github.com/chocolatefudge/simpleATM.git
   ```
2. Make sure you have Python >= 3.6 in your environment. 

### How to run
1. Build database.
   ```sh
   python3 build.py
   ```
2. Execute SimpleATM with given test code. 
   ```sh
   python3 main.py
   ```

## Making custom test and user data
### Making user data
1. Open userdata.txt
2. Add a row of cardNumber, PIN, balance divided by space. 
    ex) 1234 5678 10000
3. Remove one or more rows from userdata.txt

### Making custom test routine
1. Open test.txt
2. Add or remove actions. Possible actions are as follows: 
   ```sh
   CARDINSERT (card_number)
   AUTH (PIN)
   BALANCE
   DEPOSIT (amount)
   WITHDRAW (amount)
   EXIT
   ```
   (note that first and second arguments should be divided by space.)


## Miscellaneous
 - Card number is 4-digit number instead of 16 digits for simplicity. 
 - Any test routines that doesn't reflect the real world behaviors of the ATM might cause errors. Below are some of the examples:
   - Cannot insert more than 1 card at the same time. 
   - Cannot perform PIN check before a card is inserted. 
   - Cannot check balance / deposit / withdraw before card is inserted and PIN is authenticated. 
 - You can contact me on dong32@gmail.com. 