from picamera import PiCamera
from time import sleep
from PIL import Image
from pyzbar.pyzbar import decode
import os

def capture_image(file_path):
    camera = PiCamera()
    camera.resolution = (1440, 1080)
    camera.start_preview()
    sleep(2)  # Give the camera some time to adjust to lighting
    camera.capture(file_path)
    camera.stop_preview()
    camera.close()

def read_barcode(file_path):
    image = Image.open(file_path)
    barcodes = decode(image)
    if len(barcodes) == 0:
        print('No barcode found')
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        print(f'Found {barcode_type} barcode: {barcode_data}')
    return barcode_data

def main():
    image_path = os.path.join(os.path.dirname(__file__), 'barcode.jpg')
    capture_image(image_path)
    read_barcode(image_path)


if __name__ == "__main__":
    main()
