from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from threading import Thread
import lib_loc as library
import time

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

def loc_loop():
    while(True):
        userLoc = library.get_loc()
        setup(userLoc)

def main():
    global userLoc
    global password
    password = ''
    keypad.init(key_pressed)

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    loc_thread = Thread(target=loc_loop)
    loc_thread.start()

if __name__ == '__main__':
    main()