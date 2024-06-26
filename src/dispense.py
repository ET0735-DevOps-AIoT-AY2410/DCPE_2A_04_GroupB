import time

from hal import hal_lcd as LCD
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor

def dispenseBook():
    servo.init()
    dc_motor.init()

    lcd = LCD.lcd()
    lcd.lcd_clear()
    
    print("closed")
    servo.set_servo_position(0)
    time.sleep(1)  

    lcd.lcd_display_string("Valid Card", 1)     
    lcd.lcd_display_string("Dispensing...", 2)  
    
    print("open")
    servo.set_servo_position(90)
    time.sleep(0.5)            
    dc_motor.set_motor_speed(100)
    time.sleep(5)   
    dc_motor.set_motor_speed(0)
    time.sleep(0.5) 

    
    print("closed")
    servo.set_servo_position(0)
    time.sleep(1)

def main():
    dispenseBook()

if __name__ == '__main__':
    main()