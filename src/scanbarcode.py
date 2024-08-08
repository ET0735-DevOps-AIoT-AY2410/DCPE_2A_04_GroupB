from picamera import PiCamera
from time import sleep
import os

def capture_image(file_path):
    camera = PiCamera()
    camera.resolution = (1440, 1080)
    camera.start_preview()
    sleep(2)  # Give the camera some time to adjust to lighting
    camera.capture(file_path)
    camera.stop_preview()
    camera.close()

def main():
    image_path = os.path.join(os.path.dirname(__file__), 'barcode.jpg')
    capture_image(image_path)

if __name__ == "__main__":
    main()
