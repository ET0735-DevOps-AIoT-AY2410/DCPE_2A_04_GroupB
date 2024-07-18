from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc_motor
from threading import Thread
from flask import Flask, jsonify
import time

import lib_loc
import getBooklist
import parseBooklist
import collection
import removeBorrowed
import returnBook
import extendTime
import scanRFID
import barcode

lcd = LCD.lcd()
lcd.lcd_clear()
dc_motor.init()
returnIndex = []

books = {'1': 'Book 1',
         '2': 'Book 2',
         '3': 'Book 3',
         '4': 'Book 4',
         '5': 'Book 5',
         '6': 'Book 6',
         '7': 'Book 7',
         '8': 'Book 8',
         '9': 'Book 9',
        '10': 'Book 10'}

app = Flask(__name__)

def key_pressed(key):       #check keypad
    global password
    global returnIndex
    password = key

    print(password)
    returnIndex.append(password)
    print(returnIndex)

def setup(location):        #check location
    output = "Location " + str(location)
    lcd.lcd_display_string(output, 1)
    lcd.lcd_display_string("Press '*'", 2)

def auth():                 #scan id and authenticate
    global bookList
    global password

    verified = False
    image_path = 'barcode.jpg'
    
    lcd.lcd_clear()
    lcd.lcd_display_string("Please scan your", 1)
    lcd.lcd_display_string("admin card      ", 2)
    attmps = 1

    while(attmps < 10):
        nameList = parseBooklist.getNameList(bookList)
        tempList = parseBooklist.getNameList(borrowList)
        for i in tempList:
            nameList.append(i)
        password = 0
        #barcode.capture_image(image_path)
        adminNo = barcode.read_barcode(image_path)
        adminNo = adminNo[-7:]
        print(adminNo)
        response = parseBooklist.findPerson(nameList, adminNo)
        verified = response[0]

        if verified == True:
            person = response[1]
            lcd.lcd_clear()
            lcd.lcd_display_string(person[0], 1)
            lcd.lcd_display_string(person[1], 2)
            
            return True, person

        elif verified == False:
            lcd.lcd_clear()
            output = 'to try again ('+ str(attmps) + ')'
            lcd.lcd_display_string("Please press '#'", 1)
            lcd.lcd_display_string(output, 2)
            attmps += 1
            while(password != '#'): 
                time.sleep(1)
   
            if attmps == 10:
                lcd.lcd_clear()
                return [False]

def pageOptions():
    global password
    option = 0

    while(option < 1 or option > 4):
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

def collectOption(person, id, userLoc):
    global bookList
    global borrowList
    global toReturnList

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

def returnOption(person, id):
    global borrowList
    global toReturnList
    global password
    global returnIndex

    lcd.lcd_clear()
    lcd.lcd_display_string('Return', 1)
    time.sleep(0.5)
    if id in borrowList and len(borrowList[id]) > 0:
        returnIndex = []
        while(password != '*'): 
            print(returnIndex)
            returnBook.displayBorrowed(borrowList, person, books)
            lcd.lcd_clear()
            lcd.lcd_display_string("Press '*' to", 1)
            lcd.lcd_display_string('continue', 2)
            time.sleep(0.5)
        toReturnList = returnBook.returnBook(returnIndex, borrowList, person)
        borrowList = removeBorrowed.remove(borrowList, toReturnList)

        print('returned', toReturnList)
        print('borrowed', borrowList)
    
    else:
        lcd.lcd_display_string('No book borrowed', 1)

def extendOption(person, id):
    global borrowList
    global toReturnList
    global password
    global returnIndex
    
    lcd.lcd_clear()
    lcd.lcd_display_string('Extend', 1)
    time.sleep(0.5)
    if id in borrowList and len(borrowList[id]) > 0:
        returnIndex = []
        while(password != '*'): 
            extendTime.display(borrowList, person, books)
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

def fineOption(id):
    global fineList
    global finePaid

    lcd.lcd_clear()
    lcd.lcd_display_string('Pay Fine', 1)
    time.sleep(0.5)
    
    if id in fineList and fineList[id] > 0:
        lcd.lcd_clear()
        lcd.lcd_display_string('Fine incurred:', 1)
        lcd.lcd_display_string(f"${fineList[id]:.2f}",2)
        
        attmps = 1
        while(attmps < 10):
            card = scanRFID.scan()

            if card == 'None':
                lcd.lcd_clear()
                output = 'to try again ('+ str(attmps) + ')'
                lcd.lcd_display_string("Please press '#'", 1)
                lcd.lcd_display_string(output, 2)
                attmps += 1
                while(password != '#'):  
                    time.sleep(1)

            else:
                time.sleep(1)
                lcd.lcd_clear()
                lcd.lcd_display_string("Thank you", 1)
                time.sleep(1)

                finePaid = id
                break
    
    else:
        lcd.lcd_display_string('No fine incurred', 1)

def loc_loop():
    global password
    global returnIndex
    global finePaid
    global toReturnList

    password = 0
    returnIndex = []
    
    finePaid = ''
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
                if id not in fineList:
                    collectOption(person, id, userLoc)
                else:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Please pay fine", 1)
                    lcd.lcd_display_string("first", 2)
                    time.sleep(1)

                password = 0
                session = 0
                option = 0
                returnIndex = []

            elif option == 2:
                returnOption(person, id)

                password = 0
                session = 0
                option = 0
                returnIndex = []

            elif option == 3:
                if id not in fineList:
                    extendOption(person, id)
                else:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Please pay fine", 1)
                    lcd.lcd_display_string("first", 2)
                    time.sleep(1)
                
                password = 0
                session = 0
                option = 0
                returnIndex = []

            elif option == 4:
                fineOption(id)
                
                password = 0
                session = 0
                option = 0
                returnIndex = []
            
            lcd.lcd_clear()
        

def getList():
    global bookList
    global borrowList
    global fineList
    checkChangeReserve = {}
    checkChangeBorrow = {}
    checkChangeFine = {}
    while(True):
        data = getBooklist.getReserve()
        bookList = data[0]
        borrowList = data[1]
        fineList = getBooklist.getFine()

        if bookList != checkChangeReserve:
            print('reserve: ', bookList)
            checkChangeReserve = bookList
        if borrowList != checkChangeBorrow:
            print('borrow: ',borrowList)
            checkChangeBorrow = borrowList
        if fineList != checkChangeFine:
            print('fines: ',fineList)
            checkChangeFine = fineList

def main():
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
    tempReturn = toReturnList
    toReturnList = {}
    return jsonify(tempReturn)

@app.route('/finepaid', methods=['GET'])
def fine():
    global finePaid
    tempfinepaid = finePaid
    finePaid = ''
    return jsonify(tempfinepaid)

def run():
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main()