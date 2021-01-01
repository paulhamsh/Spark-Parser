import serial
import struct
import socket

from SparkReaderClass import *
from SparkCommsClass import *



reader = SparkReadMessage()
comms = SparkComms("bluetooth")
comms.connect()

while True:
    dat = comms.get_data()
    reader.set_message(dat)
    s = reader.read_message()
    print ("================")
    #print (reader.python)
    print (reader.text)
    #print (reader.raw)



