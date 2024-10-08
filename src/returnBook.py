from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from threading import Thread
import time
import parseBooklist

import libInterface

lcd = LCD.lcd()
lcd.lcd_clear()
returnIndex = []

def key_pressed(key):
    global returnIndex
    global password
    password = key

    print(password)
    returnIndex.append(password)

def displayBorrowed(borrowList, person, dictionary):
    displayList = parseBooklist.getReserve(borrowList, person)
    if len(displayList)%2 == 0:
        for i in range(len(displayList)):
            if i%2 == 1:
                lcd.lcd_clear()
                lcd.lcd_display_string(f"[{i}]{dictionary[displayList[i-1][0]]}", 1)
                lcd.lcd_display_string(f"[{(i+1)%10}]{dictionary[displayList[i][0]]}", 2)
                time.sleep(0.5)
                
            print(libInterface.exportKey)
            if libInterface.exportKey == "*":
                return

    elif len(displayList)%2 == 1:
        for i in range(len(displayList)):
            if i%2 == 1 and i<(len(displayList)-1):
                lcd.lcd_clear()
                lcd.lcd_display_string(f"[{i}]{dictionary[displayList[i-1][0]]}", 1)
                lcd.lcd_display_string(f"[{(i+1)%10}]{dictionary[displayList[i][0]]}", 2)
                time.sleep(0.5)
            elif i == (len(displayList)-1):
                lcd.lcd_clear()
                lcd.lcd_display_string(f"[{i+1}]{dictionary[displayList[i][0]]}", 1)
                time.sleep(0.5)
                
            if libInterface.exportKey == "*":
                return

    lcd.lcd_clear()
    lcd.lcd_display_string("Press '*' to", 1)
    lcd.lcd_display_string('continue', 2)
    time.sleep(0.5)

def returnBook(returnIndex, borrowList, person):
    for i in returnIndex:
        if type(i) != int:
            returnIndex.remove(i)
    returnIndex = set(returnIndex)
    info = person[0] + '&' + person[1]
    borrowList[info]
    reserveList = {}
    
    reserveList.setdefault(info, [])
    for index in returnIndex:
        if index <= len(borrowList[info]) and index > -1:
            reserveList[info].append([borrowList[info][int(index)-1][0]])

    return reserveList

def main():
    global password
    global returnIndex
    password = ''
    keypad.init(key_pressed)

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    egBorrowList = {'Test1&1234567': [['Book 1', '2024-06-15 21:30:29'], 
                                      ['Book 3', '2024-06-15 21:30:29' ], 
                                      ['Book 2', '2024-06-15 21:30:29'], 
                                      ['Book 9', '2024-06-15 21:30:29'],
                                      ['Book 6', '2024-06-15 21:30:29']],
                'Test2&7654321': [['Book 5', '2024-06-15 21:28:26']]}
    
    person = ['Test1', '1234567']
    
    returnIndex = []
    while(password != '*'):
        displayBorrowed(egBorrowList, person)
    print(returnIndex)

    print(returnBook(returnIndex, egBorrowList, person))
    
if __name__ == '__main__':
    main()