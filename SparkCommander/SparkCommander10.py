########
#
# Spark Commander
#
# Program to send commands to Positive Grid Spark
#
# See https://github.com/paulhamsh/Spark-Parser

#### PRESETS ####

from AllPresets import *
from SparkLib import *

#import bluetooth

import socket
import time
import struct


def send_presets(pres):
    for i in pres:
        cs.send(bytes.fromhex(i))
        a=cs.recv(100)
        
SERVER_PORT = 2
MY_SPARK = "08:EB:ED:4E:47:07"  # Change to address of YOUR Spark

try:
    
    cs = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    cs.connect((MY_SPARK, SERVER_PORT))
    print ("Connected successfully")

    print("Change to hardware preset 1")
    b = pack_hardware_preset_change(1)
    cs.send(b[0])
    r = cs.recv(100)
    time.sleep(3)
    

    for p in preset_list:
        print("Change to %s" % p["Name"])
        b = pack_preset(p)
        for i in b:
            cs.send(i)
            r = cs.recv(100)
        b = pack_hardware_preset_change (0x7f)
        cs.send(b[0])
        r = cs.recv(100)
        time.sleep(3)

    
    print ("Finished")

  
except OSError as e:
    print(e)
    
finally:
    if cs is not None:
        cs.close()
    
