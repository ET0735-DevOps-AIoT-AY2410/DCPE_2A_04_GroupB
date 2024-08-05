import time
from datetime import datetime, timedelta
from threading import Thread
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from parseDateTime import getMin
import parseBooklist

#Use 1min instead of 1day for demonstration purposes

lcd = LCD.lcd()

def key_pressed(key):
    global returnIndex
    global password
    password = key

    print(password)
    returnIndex.append(password)

def extend(returnIndex, borrowList, person):
    for i in returnIndex:
        if type(i) != int:
            returnIndex.remove('*')
    info = person[0] + '&' + person[1]
    borrowList[info]
    
    for index in returnIndex:
        if index <= len(borrowList[info]) and index > 0:
            borrowDate = datetime.strptime(borrowList[info][int(index)-1][1], '%Y-%m-%d %H:%M:%S')
            newDate = borrowDate + timedelta(minutes=7)
            newDate = datetime.strftime(newDate, '%Y-%m-%d %H:%M:%S')

            borrowList[info][int(index)-1][1] = newDate
            borrowList[info][int(index)-1][1] += 'E'

    return borrowList

def display(borrowList, person, dictionary):
    displayList = parseBooklist.getReserve(borrowList, person)
    for i in range(len(displayList)):
        if displayList[i][1][-1:] != 'E':
            lcd.lcd_clear()
            lcd.lcd_display_string(f"[{i+1}]{dictionary[displayList[i][0]]}", 1)
            lcd.lcd_display_string(f"return by {int(getMin(displayList[i][1])) + 7}", 2)
            time.sleep(0.5)
        elif displayList[i][1][-1:] == 'E':
            lcd.lcd_clear()
            lcd.lcd_display_string(dictionary[displayList[i][0]], 1)
            lcd.lcd_display_string("already extended", 2)
            time.sleep(0.5)
    
    return

def main():
    global password
    global returnIndex
    egBorrowlist = {'Test1&1234567': [['Book 1', '2024-06-09 15:07:23'], 
                                   ['Book 2', '2024-06-09 15:08:12'], 
                                   ['Book 3', '2024-06-09 15:20:12E']],
                  'Test2&7654321': [['Book 1', '2024-06-09 15:34:32']]}
    person = ['Test1', '1234567']
    
    password = ''
    keypad.init(key_pressed)

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    returnIndex = []
    while(password != '*'):
        display(egBorrowlist, person)
    print(returnIndex)
    
    print(extend(returnIndex, egBorrowlist, person))
    
if __name__ == "__main__":
    main()
