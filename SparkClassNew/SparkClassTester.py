########
#
# Spark Commander
#
# Program to send commands to Positive Grid Spark
#
# See https://github.com/paulhamsh/Spark-Parser

#### PRESETS ####

from AllPresets import *
from SparkClass import *



msg = SparkMessage()

for i in range (len(preset_list)):
    b = msg.create_preset(preset_list[i])

    for x in range(len(b)):
        if b[x].hex() != preset_listh[i][x]:
            print("Preset %s failed test in block %d" % (preset_list[i]["Name"], x))
            print (b[x].hex())
            print (preset_listh[i][x])
            print ("---------")

b = msg.change_effect("Twin","SLO100")
if b[0].hex() != "01fe000053fe27000000000000000000f0013a1501060204245477696e060126534c4f313030f7":
    print ("Pedal change failed test")
b = msg.change_hardware_preset(3)
if b[0].hex() != "01fe000053fe1a000000000000000000f0013a150138000003f7":
    print ("Hardware preset change failed test")
b = msg.turn_effect_onoff("Booster", "On")
if b[0].hex() != "01fe000053fe23000000000000000000f0013a150115020727426f6f737404657243f7":
    print ("Pedal on/off failed test")
b = msg.change_effect_parameter("Twin", 0, 0.344)
if b[0].hex() != "01fe000053fe25000000000000000000f0013a1501040204245477696e00154a3e302045f7":
    print ("Pedal parameter change failed test")
    print (b[0].hex())
    print ("01fe000053fe25000000000000000000f0013a1501044204245477696e00154a3e302045f7")
    

print ("Tests complete")

    
