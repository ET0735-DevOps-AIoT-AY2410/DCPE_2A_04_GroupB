FROM arm32v7/python:3
ENV SPI_PATH /app/src/SPI-Py
ENV LD_LIBRARY_PATH /opt/vc/lib

ENV READTHEDOCS=True
ENV TZ=Asia/Singapore

WORKDIR /app

COPY requirements.txt .

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhost.org -r requirements.txt 

RUN pip3 install --no-cache-dir rpi.gpio\
 smbus

RUN apt-get update
RUN apt-get install -y libzbar0
RUN pip3 install picamera

COPY ./src ./src

WORKDIR $SPI_PATH
RUN python3 setup.py install

WORKDIR /app

CMD ["python", "-u", "src/libInterface.py"]