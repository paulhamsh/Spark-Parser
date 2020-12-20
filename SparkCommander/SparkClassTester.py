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
    b = msg.pack_preset(preset_list[i])

    for x in range(len(b)):
        if b[x].hex() != preset_listh[i][x]:
            print("Preset %s failed test\n", b[x]["Name"])

b = msg.pack_pedal_change("Twin","SLO100")
if b[0].hex() != "01fe000053fe27000000000000000000f0013a1501060204245477696e060126534c4f313030f7":
    print ("Pedal change failed test")
b = msg.pack_hardware_preset_change(3)
if b[0].hex() != "01fe000053fe1a000000000000000000f0013a150138000003f7":
    print ("Hardware preset change failed test")
b = msg.pack_turn_pedal_onoff("Booster", "On")
if b[0].hex() != "01fe000053fe23000000000000000000f0013a150115020727426f6f737404657243f7":
    print ("Pedal on/off failed test")
b = msg.pack_parameter_change("Twin", 0, 0.344)
if b[0].hex() != "01fe000053fe25000000000000000000f0013a1501044204245477696e00014a3eb020c5f7":
    print ("Pedal parameter change failed test")

print ("Tests complete")

    
