import serial
import struct

from SparkReaderClass import *
from SparkCommsClass import *


# This captures the bluetooth traffic sent on a serial port
# I am using a ESP32 board to mimick the Spark amp and capture bluetooth traffic and relay it to the serial port
# Can be altered to parse a bytearray or similar

#ser=serial.Serial("COM7", BAUD, timeout=0)

reader = SparkReadMessage()
comms = SparkComms("serial")
comms.connect()


while True:
    dat = comms.get_data()
    reader.set_message(dat)
    reader.read_message()
    print ("================")
    print (reader.python)
    print (reader.text)
    print (reader.raw)


