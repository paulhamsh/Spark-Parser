########
#
# Spark Commander
#
# Program to send commands to Positive Grid Spark
#
# See https://github.com/paulhamsh/Spark-Parser


import bluetooth
#import socket
import time
import struct

######## Helper functions to package a command for the Spark (handles the 'format bytes'
    
def start_packing(msg):
    global snd_data, tmp_data, pos, format_byte
    global pos
    
    snd_data = msg
    pos = 1
    format_byte = 0
    tmp_data = b''
    

def add_pack (msg, setformat = True):
    global snd_data, tmp_data, pos, format_byte

    if setformat == True:
        format_byte |= (1 << (pos-1))
        
    for i in range (0, len(msg)):
        tmp_data += bytes([msg[i]])
        pos += 1

        if (pos == 8):
            snd_data += bytes([format_byte])
            snd_data += tmp_data
            format_byte = 0
            pos = 1
            tmp_data = b''

def end_pack(): 
    global snd_data, tmp_data, pos, format_byte

    if len(tmp_data) == 1:
        snd_data += tmp_data        # last byte if 0xf7 so we don't need a format byte
    elif len(tmp_data) > 1:
        snd_data += bytes([format_byte])
        snd_data += tmp_data
        
    size = len(snd_data)

    # update the size field
    final_data = snd_data[0:6] + bytes([size]) + snd_data[7:]
    return final_data

######## Functions to package a command for the Spark

block_header = b'\x01\xfe\x00\x00\x53\xfe'
size         = 33                                           # could be anything, will be replaced
block_filler = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
chunk_header = b'\xf0\x01\x3a\x15'

def pack_parameter_change (pedal, param, val):
    cmd = 0x01
    sub_cmd = 0x04
    
    start_packing (block_header + bytes([size]) + block_filler + chunk_header + bytes([cmd]) + bytes([sub_cmd]))

    add_pack ([len(pedal)], False)
    pedal_bytes = bytes([len(pedal)+0x20]) + bytes(pedal, 'utf-8')
    add_pack (pedal_bytes)
    
    add_pack ([param])

    bytes_val = struct.pack(">f", val)
    add_pack (b'\x4a' + bytes_val)

    add_pack (b'\xf7', False)
    return end_pack ()


def pack_pedal_change (pedal1, pedal2):
    cmd = 0x01
    sub_cmd = 0x06

    start_packing (block_header + bytes([size]) + block_filler + chunk_header + bytes([cmd]) + bytes([sub_cmd]))

    add_pack ([len(pedal1)], False)
    pedal1_bytes = bytes([len(pedal1)+0x20]) + bytes(pedal1, 'utf-8')
    add_pack (pedal1_bytes)

    add_pack ([len(pedal2)], False)
    pedal2_bytes = bytes([len(pedal2)+0x20]) + bytes(pedal2, 'utf-8')
    add_pack (pedal2_bytes)
    
    add_pack (b'\xf7', False)
    return end_pack ()

def pack_hardware_preset_change (preset_num):    # preset_num is 0 to 3
    cmd = 0x01
    sub_cmd = 0x38

    start_packing (block_header + bytes([size]) + block_filler + chunk_header + bytes([cmd]) + bytes([sub_cmd]))

    add_pack ([0], False)
    add_pack ([preset_num])

    add_pack (b'\xf7', False)
    return end_pack ()

def pack_turn_pedal_onoff (pedal, onoff):
    cmd = 0x01
    sub_cmd = 0x15

    start_packing (block_header + bytes([size]) + block_filler + chunk_header + bytes([cmd]) + bytes([sub_cmd]))

    add_pack ([len(pedal)], False)
    pedal_bytes = bytes([len(pedal)+0x20]) + bytes(pedal, 'utf-8')
    add_pack (pedal_bytes)

    if onoff == True:
        add_pack (b'\x42')
    else:
        add_pack (b'\x43')
        
    add_pack (b'\xf7', False)
    return end_pack ()    
    
######## Test program    

print ("Checking for bluetooth devices...")

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("Found {} devices.".format(len(nearby_devices)))

for addr, name in nearby_devices:
    print("  {} - {}".format(addr, name))
    if name == "Spark 40 Audio":
        server_addr = addr

print ("Connecting to {}...".format(server_addr))

SERVER_PORT = 2

try:
    cs = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    cs.connect((server_addr, SERVER_PORT))
    print ("Connected successfully")

    print("Change to hardware preset 0")
    b = pack_hardware_preset_change(0)
    cs.send(b)
    time.sleep(3)

    print ("Sweep up gain")    
    for v in range (0, 100):
        val = v*0.01
        b = pack_parameter_change ("Twin", 0, val)
        cs.send(b)
        time.sleep(0.02)

    print ("Change amp from Twin to SLO 100")
    b = pack_pedal_change ("Twin", "SLO100")
    cs.send(b)
    time.sleep(3)

    print ("Change amp from SLO 100 to Twin")
    b = pack_pedal_change ( "SLO100", "Twin")
    cs.send(b)
    time.sleep(3)

    print ("Turn on the Booster pedal")
    b = pack_turn_pedal_onoff  ( "Booster", False)
    cs.send(b)
    time.sleep(3)

    print ("Booster gain to 9")
    b = pack_parameter_change ("Booster", 0, 0.9)
    cs.send(b)
    time.sleep(3)
           
    print ("Booster gain to 1")
    b = pack_parameter_change ("Booster", 0, 0.1)
    cs.send(b)
    time.sleep(3)
    
    print ("Turn off Booster")       
    b = pack_turn_pedal_onoff ( "Booster", True)
    cs.send(b)
    time.sleep(3)

    print ("Turn on the Booster pedal")
    b = pack_turn_pedal_onoff  ( "Booster", False)
    cs.send(b)
    time.sleep(3)
            
    
except OSError as e:
    print(e)
finally:
    if cs is not None:
        cs.close()

