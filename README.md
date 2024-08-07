# Library Book Reservation and Collection System

This contains all the documents denoting Software Requirements Specifications(SRS), and sprint planning

It also contains the code for the Library Book Reservation and Collection System

Before running app:
- IP of server updated in:
    - static .js files
    - libInterface.py
- IP of RPi updated in:
    - webpage.py

To run container:
```
docker run -it --privileged=true \
-p 5001:5001 \
--mount type=bind,source="$(sudo find /home/pi -name scannedImage)",target=/app/scannedImage \
dionchoy/testlib
```