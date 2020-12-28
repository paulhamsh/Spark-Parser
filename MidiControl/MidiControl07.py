import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame.midi
import time
from   SparkClass import *
from   sys import platform

print()
if platform == "win32":
    #for Windows
    import socket
    midi_device_name = b'Launchkey MIDI'
    print ("Midi Control on Windows")
else:
    #for Raspberry Pi
    import bluetooth
    midi_device_name = b'Launchkey MK2 25 MIDI 1'
    print ("Midi Control on Raspberry Pi or Linux")

 
# Change to address of YOUR Spark or leave as "" to search for a Spark
my_spark = "08:EB:ED:4E:47:07"  
# my_spark = ""

#
# Spark presets and options
#

spark_noisegates =  ["bias.noisegate"]
spark_compressors = ["LA2AComp","BlueComp","Compressor","BassComp","BBEOpticalComp"]
spark_drives =      ["Booster","DistortionTS9","Overdrive","Fuzz","ProCoRat","BassBigMuff",
                     "GuitarMuff","MaestroBassmaster","SABdriver"]
spark_amps=         ["RolandJC120","Twin","ADClean","94MatchDCV2","Bassman","AC Boost","Checkmate",
                     "TwoStoneSP50","Deluxe65","Plexi","OverDrivenJM45","OverDrivenLuxVerb",
                     "Bogner","OrangeAD30","AmericanHighGain","SLO100","YJM100","Rectifier",
                     "EVH","SwitchAxeLead","Invader","BE101","Acoustic","AcousticAmpV2","FatAcousticV2",
                     "FlatAcoustic","GK800","Sunny3000","W600","Hammer500"]
spark_modulations = ["Tremolo","ChorusAnalog","Flanger","Phaser","Vibrato01","UniVibe",
                     "Cloner","MiniVibe","Tremolator","TremoloSquare"]
spark_delays =      ["DelayMono","DelayEchoFilt","VintageDelay","DelayReverse",
                     "DelayMultiHead","DelayRe201"]
spark_reverbs =     ["bias.reverb"]

spark_effects =     {"Noisegate":   spark_noisegates, 
                     "Compressor":  spark_compressors,
                     "Drive":       spark_drives,
                     "Amp":         spark_amps, 
                     "Mod":         spark_modulations, 
                     "Delay":       spark_delays, 
                     "Reverb":      spark_reverbs}

preset1 = { 
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

spark_presets = [preset1]

effects_current = {"Noisegate": "bias.noisegate", 
                   "Compressor": "LA2AComp",
                   "Drive": "Booster",
                   "Amp": "RolandJC120", 
                   "Mod": "Cloner", 
                   "Delay": "Vintage Delay", 
                   "Reverb": "bias.reverb"}

# check midi command table

def validate_map(map):
    err = 0
    for a_cmd in map:

        cmd = map[a_cmd][0]


        # test all the commands are ok
        if cmd not in ["HardwarePreset","ChangeParam","ChangeEffect","EffectOnOff"]:
            print (">>> %s is not a valid command to Spark" % cmd)
            err += 1
        
        # check the effect types (not needed for HardwarePreset)
        if cmd not in ["HardwarePreset"]:
            eff_type = map[a_cmd][1]
            eff_name = map[a_cmd][2]
            if eff_type not in effects_current:
                print (">>> %s is not a valid effect" % eff_type)
                err += 1
            else:
                if cmd in ["ChangeEffect"]:
                    if eff_name not in spark_effects[eff_type]:
                        print (">>> %s is not a valid effect name" % eff_name)
                        err += 1
    return err  

    
# Spark communications functions

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

#
# Connect to the Spark
#

print ()
print ("BLUETOOTH TO SPARK")
print ("==================")
print ("Trying to connect to Spark")

if my_spark == "":
    print ("Checking for bluetooth devices...")
    bt_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(bt_devices)))

    for addr, name in bt_devices:
        print("  {} - {}".format(addr, name))
        if name == "Spark 40 Audio":
            server_addr = addr
else:
    server_addr = my_spark

server_port = 2    
    
print ("Connecting to {}...".format(server_addr))

try:
    if platform == "win32":
        #for Windows
        cs = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        cs.connect((server_addr, server_port))
    else:
        #for Raspberry Pi
        cs = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        cs.connect((server_addr, server_port))
except OSError as e:
    print("Cannot connect to Spark via bluetooth")
    quit()
                    
print ("Connected successfully")
print("Sending Silver Ship preset")
msg = SparkMessage()
change_user_preset = msg.change_hardware_preset(0x7f)
b = msg.create_preset(preset1)
send_preset(b)

#
# Find the Midi device
#

print ()
print ("SETTING UP MIDI")
print ("===============")
print ("Starting midi")
pygame.midi.init()    

# list all midi devices
i=-1
for x in range( 0, pygame.midi.get_count() ):
    inf = pygame.midi.get_device_info(x)
    # Looking specifically for the Novation Launchkey device here
    if inf[1]== midi_device_name and inf[2] == 1:
        i = x
 
# open a specific midi device
if i>0:
    inp = pygame.midi.Input(i)
    print ("Found Launchkey")
else:
    print ("Could not find Launchkey midi device")
    quit()
    
# Start the main routine
    


midi_map = {"NoteOn-40":   ["HardwarePreset", 0],
            "NoteOn-41":   ["HardwarePreset", 1],
            "NoteOn-42":   ["HardwarePreset", 2],
            "CC-21":       ["ChangeParam", "Amp", 0],
            "CC-22":       ["ChangeParam", "Amp", 1],
            "CC-23":       ["ChangeParam", "Drive", 2],
            "NoteOn-43":   ["ChangeEffect", "Amp", "Twin"],
            "NoteOn-36":   ["EffectOnOff", "Drive", "On"],
            "NoteOn-37":   ["EffectOnOff", "Drive", "Off"]
            }
 
commands = { 0x80: "NoteOff",
             0x90: "NoteOn",
             0xB0: "CC",
             0xC0: "PgmChg" }
             

# check the commands for basic validity

print ()
print ("Checking the midi command table")

errors = validate_map(midi_map)
if errors > 0:
    print ("Need to fix the midi command table quitting")
    quit()

# run the event loop

print()
print ("RUNNING THE COMMANDER")
print ("=====================")

while True:
    if inp.poll():

        midi_in =inp.read(1000)
        for midi_data in midi_in:
            mi = midi_data[0]
            m_cmd = (mi[0] & 0xf0)
            m_val = mi[1]
            m_param = 0
            
            if m_cmd in commands:
                m_str = commands[m_cmd] + "-%d" % m_val
            else:
                m_str = ""
                
            m_param_val= mi[2] / 127

            if m_str in midi_map.keys():
                s_cmd = midi_map [m_str]
            else:
                s_cmd = ["None"]
                print ("Unknown midi command %s" % m_str)

            this_cmd = s_cmd[0]
            if this_cmd == "HardwarePreset":
                hw_preset = s_cmd[1]
                print("Change to hw preset %d" % hw_preset)
                b=msg.change_hardware_preset(hw_preset)
                send_receive(b[0])                
            elif this_cmd == "ChangeParam":
                effect_type = s_cmd[1]
                current_effect = effects_current[effect_type]
                param_num = s_cmd[2]
                print ("Change %s (%s) param number %d to %f" % (effect_type, current_effect, param_num, m_param_val))
                b=msg.change_effect_parameter(current_effect, param_num, m_param_val)
                just_send(b[0])
            elif this_cmd == "ChangeEffect":
                effect_type = s_cmd[1]
                new_effect = s_cmd[2]
                current_effect = effects_current[effect_type]
                effects_current[effect_type] = new_effect
                print ("Change %s from %s to %s" % (effect_type, current_effect, new_effect))
                b=msg.change_effect(current_effect, new_effect)
                send_receive(b[0])
            elif this_cmd == "EffectOnOff":
                effect_type = s_cmd[1]
                new_value = s_cmd[2]
                current_effect = effects_current[effect_type]
                print ("Change %s (%s) to %s" % (effect_type, current_effect, new_value))
                b=msg.turn_effect_onoff(current_effect, new_value)
                send_receive(b[0])
                    
    pygame.time.wait(10)


if cs is not None:
    cs.close()
