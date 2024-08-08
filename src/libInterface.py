from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc_motor
from threading import Thread
from flask import Flask, jsonify
import time
from datetime import datetime
import logging
import requests

import lib_loc
import getBooklist
import parseBooklist
import collection
import removeBorrowed
import returnBook
import extendTime
import scanRFID
import barcode
import libInterface

lcd = LCD.lcd()
lcd.lcd_clear()

BASE_URL = 'http://192.168.50.191:5000'

returnIndex = []
instruct = ''
fineList = []
borrowList = {}
reserveList = {}
userFine = {}
userList = []
dictionary = {}

exportKey = 0

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

def key_pressed(key):       #check keypad
    global inputKey
    global returnIndex
    inputKey = key
    libInterface.exportKey = inputKey
    returnIndex.append(inputKey)
    print(returnIndex)

def setup(location):        #check location
    output = "Location " + str(location) + "     "
    lcd.lcd_display_string(output, 1)
    lcd.lcd_display_string("Press '*'", 2)

def auth():                 #scan id and authenticate
    global reserveList
    global inputKey
    global instruct

    verified = False
    image_path = 'scannedImage/barcode.jpg'
    
    lcd.lcd_clear()
    lcd.lcd_display_string("Please scan your", 1)
    lcd.lcd_display_string("admin card      ", 2)
    attmps = 1

    while(attmps < 10):
        nameList = parseBooklist.getNameList(reserveList)
        tempList = parseBooklist.getNameList(borrowList)
        for i in tempList:
            nameList.append(i)
        tempList = parseBooklist.getNameList(userFine)
        for i in tempList:
            nameList.append(i)
        inputKey = 0
        instruct = 'scan'
        time.sleep(4)
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

            for i in userList:
                i = i.split('&')

            accountExist = parseBooklist.findPerson(userList, adminNo)
            if accountExist[0] == True:
                lcd.lcd_display_string("No services", 1)
                lcd.lcd_display_string("available", 2)
                time.sleep(1)
                lcd.lcd_display_string("Reserve book", 1)
                lcd.lcd_display_string("first    ", 2)
                time.sleep(1)
                return [False]
                
            elif accountExist[0] == False:
                output = 'to try again ('+ str(attmps) + ')'
                lcd.lcd_display_string("Please press '#'", 1)
                lcd.lcd_display_string(output, 2)
                attmps += 1
                while(inputKey != '#' and inputKey != '*'): 
                    time.sleep(1)
    
                if attmps == 10 or inputKey == '*':
                    lcd.lcd_clear()
                    return [False]

def pageOptions():
    global inputKey
    option = 0
    inputKey = 0
    
    sessionTime = datetime.now()

    while(option < 1 or option > 5 or type(option) != int):
        time.sleep(1)

        lcd.lcd_clear()
        lcd.lcd_display_string('[1]Collect', 1)
        lcd.lcd_display_string('[2]Return', 2)

        time.sleep(1)
        option = inputKey
        if (option >= 1 and option <= 5 and type(option) == int):
            break

        lcd.lcd_clear()
        lcd.lcd_display_string('[3]Extend', 1)
        lcd.lcd_display_string('[4]Pay fine', 2)
        time.sleep(1)
        option = inputKey
        if (option >= 1 and option <= 5 and type(option) == int):
            break

        lcd.lcd_clear()
        lcd.lcd_display_string('[5]Exit', 1)
        time.sleep(1)

        option = inputKey

        currentTime = datetime.now()
        delta = currentTime - sessionTime
        min = round(delta.total_seconds())/60
        if min >= 1:
            lcd.lcd_clear()
            lcd.lcd_display_string('Session timed', 1)
            lcd.lcd_display_string('out', 2)
            time.sleep(1)
            option = 5
            break

    return option

def collectOption(person, id, userLoc):
    global reserveList
    global borrowList
    global toReturnList

    lcd.lcd_clear()
    lcd.lcd_display_string('Collect', 1)
    time.sleep(0.5)
    if id in reserveList and len(reserveList[id]) > 0:
        if id in borrowList:
            noOfBorrowed = len(borrowList[id])
        else:
            noOfBorrowed = 0
        toReturnList = collection.collectBook(person, userLoc, reserveList, noOfBorrowed)
        reserveList = removeBorrowed.remove(reserveList, toReturnList)
        
        reponse = requests.post(f'{BASE_URL}/return', headers={'info': 'book'}, json=toReturnList)
        print(reponse.json(), '\n')

        print('borrowed', toReturnList)

        if len(toReturnList) > 0:
            lcd.lcd_clear()
            lcd.lcd_display_string("Books collected", 1)
            lcd.lcd_display_string('successfully', 2)
            time.sleep(0.5)
    
    else:
        lcd.lcd_display_string('No book reserved', 1)

def returnOption(person, id):
    global borrowList
    global toReturnList
    global inputKey
    global returnIndex

    lcd.lcd_clear()
    lcd.lcd_display_string('Return', 1)
    time.sleep(0.5)
    if id in borrowList and len(borrowList[id]) > 0:
        returnIndex = []
        while(inputKey != '*'): 
            returnBook.displayBorrowed(borrowList, person, dictionary)
        print(returnIndex)
        toReturnList = returnBook.returnBook(returnIndex, borrowList, person)
        borrowList = removeBorrowed.remove(borrowList, toReturnList)

        reponse = requests.post(f'{BASE_URL}/return', headers={'info': 'book'}, json=toReturnList)
        print(reponse.json(), '\n')

        print('returned', toReturnList)
        print('borrowed', borrowList)
        
        if len(returnIndex) > 1:
            lcd.lcd_clear()
            lcd.lcd_display_string("Books returned", 1)
            lcd.lcd_display_string('successfully', 2)
            time.sleep(0.5)
        else:
            lcd.lcd_clear()
            lcd.lcd_display_string("Exited", 1)

    else:
        lcd.lcd_display_string('No book borrowed', 1)

def extendOption(person, id):
    global borrowList
    global toReturnList
    global inputKey
    global returnIndex
    
    lcd.lcd_clear()
    lcd.lcd_display_string('Extend', 1)
    time.sleep(0.5)
    if id in borrowList and len(borrowList[id]) > 0:
        returnIndex = []
        while(inputKey != '*'): 
            extendTime.display(borrowList, person, dictionary)
        print(returnIndex)
        borrowList = extendTime.extend(returnIndex, borrowList, person)
        toReturnList = borrowList
        
        reponse = requests.post(f'{BASE_URL}/return', headers={'info': 'book'}, json=toReturnList)
        print(reponse.json(), '\n')

        print('borrowed', borrowList)

        if len(returnIndex) > 1:
            lcd.lcd_clear()
            lcd.lcd_display_string("Books returned", 1)
            lcd.lcd_display_string('successfully', 2)
            time.sleep(0.5)
        else:
            lcd.lcd_clear()
            lcd.lcd_display_string("Exited", 1)
    
    else:
        lcd.lcd_display_string('No book borrowed', 1)

def fineOption(id):
    global userFine
    global finePaid
    global fineList

    lcd.lcd_clear()
    lcd.lcd_display_string('Pay Fine', 1)
    time.sleep(0.5)

    overdueFlag = 0
    overdueList = []
    
    if id in userFine and userFine[id] > 0:
        lcd.lcd_clear()
        lcd.lcd_display_string('Fine incurred:', 1)
        lcd.lcd_display_string(f"${userFine[id]:.2f}",2)
        time.sleep(0.5)

        for overdueBook in fineList:
            if id == overdueBook[2]:
                overdueFlag += 1
                overdueList.append(overdueBook)
        
        attmps = 1
        while(attmps < 10 and overdueFlag == 0):
            card = scanRFID.scan()

            if card == 'None':
                lcd.lcd_clear()
                output = 'to try again ('+ str(attmps) + ')'
                lcd.lcd_display_string("Please press '#'", 1)
                lcd.lcd_display_string(output, 2)
                attmps += 1
                while(inputKey != '#'):  
                    time.sleep(1)

            else:
                time.sleep(1)
                lcd.lcd_clear()
                lcd.lcd_display_string("Thank you", 1)
                time.sleep(1)

                finePaid = id
                
                reponse = requests.post(f'{BASE_URL}/return', headers={'info': 'fine'}, json=finePaid)
                print(reponse.json(), '\n')

                return

        lcd.lcd_clear()
        lcd.lcd_display_string("Pls return the", 1)
        lcd.lcd_display_string("following 1st:", 2)
        time.sleep(0.5)

        for overdueBook in overdueList:
            lcd.lcd_clear()
            lcd.lcd_display_string(dictionary[overdueBook[0]], 1)
            time.sleep(0.75)
    
    else:
        lcd.lcd_display_string('No fine incurred', 1)

def loc_loop():
    global inputKey
    global returnIndex
    global finePaid
    global toReturnList

    inputKey = 0
    returnIndex = []
    
    finePaid = ''
    toReturnList = {}

    session = 0
    option = 0

    while(True):
        userLoc = lib_loc.get_loc()
        setup(userLoc)

        if inputKey == '*':
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
                if id not in userFine:
                    collectOption(person, id, userLoc)
                else:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Please pay fine", 1)
                    lcd.lcd_display_string("first", 2)
                    time.sleep(1)
                    
                inputKey = 0
                option = 0
                returnIndex = []

            elif option == 2:
                returnOption(person, id)
                
                inputKey = 0
                option = 0
                returnIndex = []

            elif option == 3:
                if id not in userFine:
                    extendOption(person, id)
                else:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Please pay fine", 1)
                    lcd.lcd_display_string("first", 2)
                    time.sleep(1)
                    
                inputKey = 0
                option = 0
                returnIndex = []

            elif option == 4:
                fineOption(id)

                inputKey = 0
                option = 0
                returnIndex = []
                
            elif option == 5:
                
                inputKey = 0
                session = 0
                option = 0
                returnIndex = []
            
            lcd.lcd_clear()
        

def getList():
    global reserveList
    global borrowList
    global fineList
    global userFine
    global userList
    global dictionary

    checkReserve = {}
    checkBorrow = {}
    checkUserFine = {}
    checkUserList = []
    checkFine = {}
    checkDict = {}

    while(True):
        data = getBooklist.getReserve(BASE_URL)
        reserveList = data[0]
        borrowList = data[1]
        fineData = getBooklist.getFine(BASE_URL)
        userFine = fineData[0]
        fineList = fineData[1]
        dictionary = getBooklist.getDict(BASE_URL)

        if reserveList != checkReserve:
            print('reserve: ', reserveList)
            checkReserve = reserveList
        if borrowList != checkBorrow:
            print('borrow: ', borrowList)
            checkBorrow = borrowList
        if userFine != checkUserFine:
            print('user fines: ', userFine)
            checkUserFine = userFine
        if fineList != checkFine:
            print('fines: ', fineList)
            checkFine = fineList
        if userList != checkUserList:
            print('user accounts: ', userList)
            checkUserList = userList      
        if dictionary != checkDict:
            print('dictionary books: ', dictionary)
            checkDict = dictionary

def main():
    dc_motor.init()
    keypad.init(key_pressed)

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    loc_thread = Thread(target=loc_loop)
    loc_thread.start()

    book_thread = Thread(target=getList)
    book_thread.start()

    webthread = Thread(target=run)
    webthread.start()

@app.route('/cameraInstruct', methods=['GET'])
def cam():
    global instruct
    tempInstruct = instruct
    instruct = ''
    return jsonify(tempInstruct)

def run():
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main()