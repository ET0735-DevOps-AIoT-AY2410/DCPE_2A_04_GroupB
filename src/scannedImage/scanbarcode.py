from picamera import PiCamera
from time import sleep
import os
import requests

def capture_image(file_path):
    camera = PiCamera()
    camera.resolution = (1440, 1080)
    camera.start_preview()
    sleep(2)  # Give the camera some time to adjust to lighting
    camera.capture(file_path)
    camera.stop_preview()
    camera.close()

def getInstruct():
    try:
        reponse = requests.get('http://127.0.0.1:5001/cameraInstruct').json()
        return reponse
    except:
        pass

def main():
    while(True):
        response = getInstruct()
        if response == 'scan':
            capture_image('scannedImage/barcode.jpg')
            print('scanned successfully')

if __name__ == "__main__":
    main()
