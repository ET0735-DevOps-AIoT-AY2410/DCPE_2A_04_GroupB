from hal import hal_input_switch as input_switch
from hal import hal_lcd as LCD
from threading import Thread
import time

lcd = LCD.lcd()

def main():
    input_switch.init()
    lcd.lcd_clear()
    
    loc_thread = Thread(target=loc_loop)
    loc_thread.start()

def loc_loop():
    while(True):
        output = "Location " + str(get_loc())
        lcd.lcd_display_string(str(output), 1) 
    

def get_loc():
    global location

    input_switch.init()
    
    switch = input_switch.read_slide_switch()
    if switch == 0:
        location = 2
    elif switch == 1:
        location = 1
    
    return location

if __name__ =='__main__':
    main()