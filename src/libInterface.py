from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from threading import Thread
import lib_loc as library
import time
import getBooklist
import parseBooklist

lcd = LCD.lcd()
lcd.lcd_clear()

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
    nameList = parseBooklist.getNameList(bookList)
    attmps = 1

    while(restart == True and attmps < 10):
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

def loc_loop():
    global password
    session = 0
    
    while(session == 0):
        userLoc = library.get_loc()
        setup(userLoc)

        if password == '*':
            session = 1
            print(userLoc)
            authenticate = auth()
            if authenticate[0] == False:
                session = 0

            elif authenticate[0] == True:
                print(authenticate[1])

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
    global userLoc
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