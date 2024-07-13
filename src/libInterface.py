from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc_motor

import time
from threading import Thread
from flask import Flask

import lib_loc
import getBooklist
import parseBooklist
import collection
import removeBorrowed
import returnBook
import extendTime

lcd = LCD.lcd()
lcd.lcd_clear()
dc_motor.init()

app = Flask(__name__)

def key_pressed(key):
    global password
    password = key

    print(password)

def setup(location):
    output = "Location " + str(location)
    lcd.lcd_display_string(output, 1)
    lcd.lcd_display_string("Press '*'", 2)

def auth():
    global bookList
    global password

    verified = False
    restart = True
    
    lcd.lcd_clear()
    lcd.lcd_display_string("Please scan your", 1)
    lcd.lcd_display_string("admin card      ", 2)
    attmps = 1

    while(restart == True and attmps < 10):
        nameList = parseBooklist.getNameList(bookList)
        password = 0
        adminNo = '1234567' #replace with camera
        response = parseBooklist.findPerson(nameList, adminNo)
        verified = response[0]

        if verified == True:
            person = response[1]
            lcd.lcd_clear()
            lcd.lcd_display_string(person[0], 1)
            lcd.lcd_display_string(person[1], 2)
            restart = False
            
            return True, person

        elif verified == False:
            lcd.lcd_clear()
            output = 'to try again ('+ str(attmps) + ')'
            lcd.lcd_display_string("Please press '#'", 1)
            lcd.lcd_display_string(output, 2)
            attmps += 1
            while(password != '#'):  
                restart = True
   
            if attmps == 10:
                lcd.lcd_clear()
                return [False]

def pageOptions():
    global password
    global toReturnList
    toReturnList = {}
    option = 0

    while(option == 0):
        time.sleep(1)

        lcd.lcd_clear()
        lcd.lcd_display_string('Collect press 1', 1)
        lcd.lcd_display_string('Return press 2', 2)

        time.sleep(1)

        lcd.lcd_clear()
        lcd.lcd_display_string('Extend press 3', 1)
        lcd.lcd_display_string('Pay fine press 4', 2)
        time.sleep(1)

        option = password

    return option

def loc_loop():
    global password
    global bookList
    global borrowList
    global returnList
    global returnIndex
    global fineList
    global toReturnList
    returnList = {}
    toReturnList = {}
    session = 0
    option = 0
    
    while(True):
        userLoc = lib_loc.get_loc()
        setup(userLoc)

        if password == '*':
            session = 1
            print(userLoc)
            authenticate = auth()

            if authenticate[0] == False:
                session = 0

        while(session == 1):
            person = authenticate[1]
            print(person)
            id = person[0] + '&' + person[1]

            if option == 0:
                option = pageOptions()
            
            elif option == 1:
                lcd.lcd_clear()
                lcd.lcd_display_string('Collect', 1)
                time.sleep(0.5)
                if id in bookList and len(bookList[id]) > 0:
                    if id in borrowList:
                        noOfBorrowed = len(borrowList[id])
                    else:
                        noOfBorrowed = 0
                    toReturnList = collection.collectBook(person, userLoc, bookList, noOfBorrowed)
                    bookList = removeBorrowed.remove(bookList, toReturnList)
                    print('borrowed', toReturnList)
                
                else:
                    lcd.lcd_display_string('No book reserved', 1)
                
                session = 0
                option = 0
                returnIndex = []

            elif option == 2:
                lcd.lcd_clear()
                lcd.lcd_display_string('Return', 1)
                time.sleep(0.5)
                if id in borrowList and len(borrowList[id]) > 0:
                    returnIndex = []
                    while(password != '*'): 
                        print(returnIndex)
                        returnBook.displayBorrowed(borrowList, person)
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Press '*' to", 1)
                        lcd.lcd_display_string('continue', 2)
                        time.sleep(0.5)
                    toReturnList = returnBook.returnBook(returnIndex, borrowList, person)
                    borrowList = removeBorrowed.remove(borrowList, toReturnList)

                    print('returned', returnList)
                    print('borrowed', borrowList)
                
                else:
                    lcd.lcd_display_string('No book borrowed', 1)
                
                password = 0
                session = 0
                option = 0
                returnIndex = []

            elif option == 3:
                lcd.lcd_clear()
                lcd.lcd_display_string('Extend', 1)
                time.sleep(0.5)
                if id in borrowList and len(borrowList[id]) > 0:
                    returnIndex = []
                    while(password != '*'): 
                        extendTime.display(borrowList, person)
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Press '*' to", 1)
                        lcd.lcd_display_string('continue', 2)
                        time.sleep(0.5)
                    print(returnIndex)
                    borrowList = extendTime.extend(returnIndex, borrowList, person)
                    toReturnList = borrowList
                    
                    print('borrowed', borrowList)
                
                else:
                    lcd.lcd_display_string('No book borrowed', 1)
                
                password = 0
                session = 0
                option = 0
                returnIndex = []


            elif option == 4:
                lcd.lcd_clear()
                lcd.lcd_display_string('Pay Fine', 1)
                
                session = 0
                option = 0
                returnIndex = []
        
            lcd.lcd_clear()        

def getList():
    global bookList
    global borrowList
    checkChangeReserve = {}
    checkChangeBorrow = {}
    while(True):
        data = getBooklist.getReserve()
        bookList = data[0]
        borrowList = data[1]
        if bookList != checkChangeReserve:
            print('reserve: ', bookList)
            checkChangeReserve = bookList
        if borrowList != checkChangeBorrow:
            print('borrow: ',borrowList)
            checkChangeBorrow = borrowList

def main():
    global password
    password = ''
    keypad.init(key_pressed)

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    loc_thread = Thread(target=loc_loop)
    loc_thread.start()

    book_thread = Thread(target=getList)
    book_thread.start()

    webthread = Thread(target=run)
    webthread.start()

@app.route('/', methods=['GET'])
def about():
    global toReturnList
    return toReturnList

def run():
    app.run(host='0.0.0.0', port=5001)
    
if __name__ == '__main__':
    main()