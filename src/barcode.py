from time import sleep
from PIL import Image
from pyzbar.pyzbar import decode
import os

def read_barcode(file_path):
    image = Image.open(file_path)
    barcodes = decode(image)
    if len(barcodes) == 0:
        print('No barcode found')
        return '0000000000'
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        print(f'Found {barcode_type} barcode: {barcode_data}')
    return barcode_data

def main():
    image_path = os.path.join(os.path.dirname(__file__), 'barcode.jpg')
    read_barcode(image_path)


if __name__ == "__main__":
    main()
