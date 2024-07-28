import time

# Abstract hardware interactions
class LCDInterface:
    def clear(self):
        pass
    
    def display_string(self, message, line):
        pass

class ServoInterface:
    def set_position(self, position):
        pass

class DCMotorInterface:
    def set_speed(self, speed):
        pass

# Implement the dispenseBook function with dependency injection
def dispenseBook(lcd: LCDInterface, servo: ServoInterface, dc_motor: DCMotorInterface):
    lcd.clear()
    
    print("closed")
    servo.set_position(0)
    time.sleep(1)  

    lcd.display_string("Valid Card", 1)     
    lcd.display_string("Dispensing...", 2)  
    
    print("open")
    servo.set_position(90)
    time.sleep(0.5)            
    dc_motor.set_speed(100)
    time.sleep(5)   
    dc_motor.set_speed(0)
    time.sleep(0.5) 

    print("closed")
    servo.set_position(0)
    time.sleep(1)

# Mock classes for testing
class MockLCD(LCDInterface):
    def __init__(self):
        self.commands = []

    def clear(self):
        self.commands.append("LCD cleared")

    def display_string(self, message, line):
        self.commands.append(f"LCD Line {line}: {message}")

class MockServo(ServoInterface):
    def __init__(self):
        self.positions = []

    def set_position(self, position):
        self.positions.append(f"Servo set to position {position}")

class MockDCMotor(DCMotorInterface):
    def __init__(self):
        self.speeds = []

    def set_speed(self, speed):
        self.speeds.append(f"DC Motor set to speed {speed}")

def main():
    lcd = MockLCD()
    servo = MockServo()
    dc_motor = MockDCMotor()

    dispenseBook(lcd, servo, dc_motor)

if __name__ == '__main__':
    main()
