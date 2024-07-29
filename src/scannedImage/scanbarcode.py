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

def main():
    while(True):
        response = requests.get('http://127.0.0.1:5001/cameraInstruct')
        if response == 'scannedImage/barcode.jpg':
            capture_image('barcode.jpg')

if __name__ == "__main__":
    main()
