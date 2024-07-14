from hal import hal_rfid_reader as rfid_reader
from hal import hal_lcd as LCD
import time

def scan():          
    lcd = LCD.lcd()
    lcd.lcd_clear() 

    lcd.lcd_display_string("Scan your card", 1)  
    lcd.lcd_display_string("to pay fine", 2)
    time.sleep(1)

    reader = rfid_reader.init()
    id = reader.read_id_no_block()
    id = str(id)

    return id 

def main():
    print(scan())

if __name__ == '__main__':
    main()