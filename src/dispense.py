import time

from hal import hal_lcd as LCD
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor
from hal import hal_led as led

def dispenseBook():
    servo.init()
    led.init()
    led.set_output(1, 1)

    lcd = LCD.lcd()
    lcd.lcd_clear()
    
    print("closed")
    servo.set_servo_position(0)
    time.sleep(1)  
    
    lcd.lcd_display_string("Dispensing...", 1)  
    
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
    
    led.set_output(1, 0)

def main():
    dc_motor.init()
    dispenseBook()

if __name__ == '__main__':
    main()