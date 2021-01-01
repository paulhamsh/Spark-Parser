########
#
# Spark Run Some Command Tests
#
# Program to send commands to Positive Grid Spark
#
# See https://github.com/paulhamsh/Spark-Parser


from AllPresets import *
from SparkClass import *

import socket
import time
import struct


SERVER_PORT = 2
MY_SPARK = "08:EB:ED:4E:47:07"  # Change to address of YOUR Spark


def send_receive(b):
    cs.send(b)
    a=cs.recv(100)

    
def send_preset(pres):
    for i in pres:
        cs.send(i)
        a=cs.recv(100)
    cs.send(change_user_preset[0])
    a=cs.recv(100)
    
def just_send(b):
    cs.send(b)
    


try:
    cs = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    cs.connect((MY_SPARK, SERVER_PORT))
    print ("Connected successfully")

    msg = SparkMessage()
    
    
    # Run some basic tests

    change_user_preset = msg.change_hardware_preset(0x7f)
    
    print("Change to hardware preset 0")
    b = msg.change_hardware_preset(0)
    send_receive(b[0])
    time.sleep(3)


    
    print ("Sweep up gain")    
    for v in range (0, 100):
        val = v*0.01
        b = msg.change_effect_parameter ("Twin", 0, val)
        just_send(b[0])
        time.sleep(0.02)

    print ("Change amp from Twin to SLO 100")
    b = msg.change_effect ("Twin", "SLO100")
    send_receive(b[0])
    time.sleep(3)

    print ("Change amp from SLO 100 to Twin")
    b = msg.change_effect ( "SLO100", "Twin")
    send_receive(b[0])
    time.sleep(3)

    print ("Turn on the Booster pedal")
    b = msg.turn_effect_onoff  ( "Booster", "On")
    send_receive(b[0])
    time.sleep(3)

    print ("Booster gain to 9")
    b = msg.change_effect_parameter ("Booster", 0, 0.9)
    just_send(b[0])
    time.sleep(3)
           
    print ("Booster gain to 1")
    b = msg.change_effect_parameter ("Booster", 0, 0.1)
    just_send(b[0])
    time.sleep(3)
    
    print ("Turn off Booster")       
    b = msg.turn_effect_onoff ( "Booster", "Off")
    send_receive(b[0])
    time.sleep(3)

    print ("Turn on the Booster pedal")
    b = msg.turn_effect_onoff  ( "Booster", "On")
    send_receive(b[0])
    time.sleep(3)

    for i in range (len(preset_list)):
        print ("\t", preset_list[i]["Name"])
        b = msg.create_preset(preset_list[i])
        send_preset(b)
        time.sleep(5)

    print("Preset ", preset_list[1]["Name"])
    b = msg.create_preset(preset_list[8])
    send_preset(b)
    time.sleep(5)

    
    print ("Finished")

    
except OSError as e:
    print(e)
finally:
    if cs is not None:
        cs.close()
