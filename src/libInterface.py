from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc_motor
from threading import Thread
import lib_loc as library
import time
import getBooklist
import parseBooklist
import collection

lcd = LCD.lcd()
lcd.lcd_clear()
dc_motor.init()

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
        option = password

    return option

def loc_loop():
    global password
    global borrowList
    session = 0
    option = 0
    
    while(True):
        userLoc = library.get_loc()
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

            if option == 0:
                option = pageOptions()
            
            elif option == 1:
                lcd.lcd_clear()
                lcd.lcd_display_string('Collect', 1)

                if person[0] + '&' + person[1] in borrowList:
                    noOfBorrowed = len(borrowList[person[0] + '&' + person[1]])
                else:
                    noOfBorrowed = 0
                borrowList = collection.collectBook(person, userLoc, bookList, noOfBorrowed)
                print(borrowList)
                session = 0

            elif option == 2:
                lcd.lcd_clear()
                lcd.lcd_display_string('Return', 1)
            elif option == 3:
                lcd.lcd_clear()
                lcd.lcd_display_string('Extend', 1)
            elif option == 4:
                lcd.lcd_clear()
                lcd.lcd_display_string('Pay Fine', 1)
        
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
    
if __name__ == '__main__':
    main()