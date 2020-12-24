
import pygame
import pygame.midi
import time
from   SparkClass import *

#for Raspberry Pi
import bluetooth
#end for Raspberry Pi

#for Windows
#import socket
#end for Windows


SERVER_PORT = 2
MY_SPARK = "08:EB:ED:4E:47:07"  # Change to address of YOUR Spark

preset = { 
    "Filler": [0x00, 0x7f], 
    "UUID": "07079063-94A9-41B1-AB1D-02CBC5D00790",
    "Name": "Silver Ship",
    "Version": "0.7",
    "Description": "1-Clean",
    "Icon": "icon.png",
    "BPM": 60.0,
    "Pedals": [ { 
        "Name": "bias.noisegate",
        "OnOff": "Off",
        "Parameters": [0.137825, 0.224641, 0.000000] }, { 
        "Name": "LA2AComp",
        "OnOff": "On",
        "Parameters": [0.000000, 0.852394, 0.186536] }, { 
        "Name": "Booster",
        "OnOff": "Off",
        "Parameters": [0.720631] }, { 
        "Name": "RolandJC120",
        "OnOff": "On",
        "Parameters": [0.630271, 0.140908, 0.158357, 0.669359, 0.805777] }, { 
        "Name": "Cloner",
        "OnOff": "On",
        "Parameters": [0.199593, 0.000000] }, { 
        "Name": "VintageDelay",
        "OnOff": "Off",
        "Parameters": [0.188881, 0.212384, 0.209420, 0.500000] }, { 
        "Name": "bias.reverb",
        "OnOff": "On",
        "Parameters": [0.142857, 0.204175, 0.144743, 0.193668, 0.582143, 0.650000, 0.199510] }], 
    "End Filler": 0x34}

amps = ["RolandJC120", "Twin", "ADClean", "Bassman", "AC Boost"]

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

    
pygame.init()
pygame.midi.init()

#for Raspberry Pi
cs = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
cs.connect((MY_SPARK, SERVER_PORT))
#end for Raspberry Pi

#for Windows
#cs = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
#cs.connect((MY_SPARK, SERVER_PORT))
#end for Windows
        
print ("Connected successfully")

print("Sending Silver Ship preset")
msg = SparkMessage()
change_user_preset = msg.change_hardware_preset(0x7f)

b = msg.create_preset(preset)
send_preset(b)

amp = 0

    
# list all midi devices
i=-1
for x in range( 0, pygame.midi.get_count() ):
    inf = pygame.midi.get_device_info(x)
    # Looking specifically for the Novation Launchkey device here
    if inf[1]== b'Launchkey MK2 25 MIDI 1':
        i = x
 
# open a specific midi device
if i>0:
    inp = pygame.midi.Input(i)
else:
    print ("Could not find Launchkey midi device")
    quit()
    
# run the event loop
while True:
    if inp.poll():
        # no way to find number of messages in queue
        # so we just specify a high max value
        midi_in =inp.read(1000)
        for midi_data in midi_in:
            mi = midi_data[0]
            #print ("%d %d %d %d" % (mi[0], mi[1], mi[2], mi[3]))

            if mi[0] == 176:
                par = mi[1] - 21
                if par >= 0 and par < 5:
                    val = mi[2] / 127
                    print (par, val)
                    b = msg.change_effect_parameter(amps[amp], par, val)
                    just_send(b[0])
            elif mi[0] == 153:
                if mi[1] >= 40 and mi[1] <=43:
                    new_amp = mi[1] - 40
                if mi[1] == 48:
                    new_amp = 4
                if new_amp >= 0 and new_amp < 5:
                    print (amps[amp], amps[new_amp])
                    b = msg.change_effect(amps[amp], amps[new_amp])
                    send_receive(b[0])
                    amp = new_amp

                    
    # wait 10ms - this is arbitrary, but wait(0) still resulted
    # in 100% cpu utilization
    pygame.time.wait(10)

