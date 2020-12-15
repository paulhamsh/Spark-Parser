########
#
# Spark Commander
#
# Program to send commands to Positive Grid Spark
#
# See https://github.com/paulhamsh/Spark-Parser

#### PRESETS ####

preset = { "Filler": [0x00, 0x7f],
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

preset2 = { "Filler": [0x00, 0x7f], 
            "UUID": "CDE99591-C05D-4AE0-9E34-EC4A81F3F84F",
            "Name": "Sweet Memory",
            "Version": "0.7",
            "Description": "1-Clean",
            "Icon": "icon.png",
            "BPM": 60.0,
            "Pedals": [ { 
                "Name": "bias.noisegate",
                "OnOff": "Off",
                "Parameters": [0.049625, 0.570989, 0.000000] }, { 
                "Name": "BlueComp",
                "OnOff": "Off",
                "Parameters": [0.215257, 0.661338, 0.177034, 0.555061] }, { 
                "Name": "DistortionTS9",
                "OnOff": "Off",
                "Parameters": [0.057889, 0.739769, 0.593970] }, { 
                "Name": "94MatchDCV2",
                "OnOff": "On",
                "Parameters": [0.528918, 0.500905, 0.246163, 0.208069, 0.782293] }, { 
                "Name": "Flanger",
                "OnOff": "Off",
                "Parameters": [0.206406, 0.661090, 0.653219] }, { 
                "Name": "DelayRe201",
                "OnOff": "On",
                "Parameters": [0.048888, 0.155602, 0.242589, 0.184818, 0.500000] }, { 
                "Name": "bias.reverb",
                "OnOff": "On",
                "Parameters": [0.559224, 0.504705, 0.208440, 0.150422, 0.602287, 0.594118, 0.000000] }], 
            "End Filler": 0x6b}

preset3 = { "Filler": [0x00, 0x7f], 
            "UUID": "6AF9D829-CEA7-4189-AC80-B3364A563EB4",
            "Name": "Dark Soul",
            "Version": "0.7",
            "Description": "1-Clean",
            "Icon": "icon.png",
            "BPM": 60.0,
            "Pedals": [ { 
                "Name": "bias.noisegate",
                "OnOff": "On",
                "Parameters": [0.058408, 0.128289, 0.000000] }, { 
                "Name": "BBEOpticalComp",
                "OnOff": "Off",
                "Parameters": [0.712698, 0.184857, 0.000000] }, { 
                "Name": "Overdrive",
                "OnOff": "On",
                "Parameters": [0.586199, 0.167363, 0.128346] }, { 
                "Name": "SLO100",
                "OnOff": "On",
                "Parameters": [0.590901, 0.512059, 0.583818, 0.143590, 0.505713] }, { 
                "Name": "Flanger",
                "OnOff": "Off",
                "Parameters": [0.206406, 0.661090, 0.653219] }, { 
                "Name": "DelayMono",
                "OnOff": "Off",
                "Parameters": [0.215109, 0.192441, 0.239331, 0.199510, 0.500000] }, { 
                "Name": "bias.reverb",
                "OnOff": "On",
                "Parameters": [0.170029, 0.809775, 0.147739, 0.148698, 0.582143, 0.650000, 0.199510] }], 
            "End Filler": 0x58}

preset4 = { "Filler": [0x00, 0x7f], 
            "UUID": "2E2928B5-D87E-4346-B58F-145B88C581BE",
            "Name": "Blues Ark",
            "Version": "0.7",
            "Description": "1-Clean",
            "Icon": "icon.png",
            "BPM": 60.0,
            "Pedals": [ { 
                "Name": "bias.noisegate",
                "OnOff": "On",
                "Parameters": [0.127409, 0.156590, 0.000000] }, { 
                "Name": "LA2AComp",
                "OnOff": "On",
                "Parameters": [0.000000, 0.832474, 0.151574] }, { 
                "Name": "DistortionTS9",
                "OnOff": "On",
                "Parameters": [0.570513, 0.547716, 0.704468] }, { 
                "Name": "Twin",
                "OnOff": "On",
                "Parameters": [0.677588, 0.185857, 0.591710, 0.676652, 0.239594] }, { 
                "Name": "ChorusAnalog",
                "OnOff": "Off",
                "Parameters": [0.188557, 0.154576, 0.508627, 0.227677] }, { 
                "Name": "DelayMono",
                "OnOff": "On",
                "Parameters": [0.173239, 0.238698, 0.521186, 0.606772, 0.500000] }, { 
                "Name": "bias.reverb",
                "OnOff": "On",
                "Parameters": [0.162267, 0.196427, 0.230569, 0.050138, 0.243627, 0.232705, 0.149510] }], 
            "End Filler": 0x23}

preset5 = { "Filler": [0x00, 0x7f], 
            "UUID": "94109418-E7D9-4B99-83F7-DDB11CA5847D",
            "Name": "Spooky Melody",
            "Version": "0.7",
            "Description": "Description for Alternative Preset 1",
            "Icon": "icon.png",
            "BPM": 60.0,
            "Pedals": [ { 
                "Name": "bias.noisegate",
                "OnOff": "On",
                "Parameters": [0.500000, 0.500000] }, { 
                "Name": "Compressor",
                "OnOff": "On",
                "Parameters": [0.175844, 0.177083] }, { 
                "Name": "DistortionTS9",
                "OnOff": "Off",
                "Parameters": [0.136083, 0.642384, 0.593971] }, { 
                "Name": "Twin",
                "OnOff": "On",
                "Parameters": [0.613426, 0.244191, 0.226583, 0.505084, 0.579992] }, { 
                "Name": "UniVibe",
                "OnOff": "On",
                "Parameters": [0.634645, 0.000000, 0.246419] }, { 
                "Name": "DelayEchoFilt",
                "OnOff": "On",
                "Parameters": [0.231858, 0.555041, 0.529055, 0.154405, 0.000000] }, { 
                "Name": "bias.reverb",
                "OnOff": "On",
                "Parameters": [0.961090, 0.231594, 0.175907, 0.224767, 0.227677, 0.178083, 0.500000] }], 
            "End Filler": 0x19}

#import bluetooth

import socket
import time
import struct

block_header = b'\x01\xfe\x00\x00\x53\xfe'
size         = 33                                           # could be anything, will be replaced
block_filler = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
chunk_header = b'\xf0\x01\x3a\x15'
this_chunk = 0
max_size = 0xad


######## Helper functions to package a command for the Spark (handles the 'format bytes'

def pack_header(cmd, sub_cmd, multi):
    global snd_data, tmp_data, format_byte, this_chunk, this_cmd, this_sub_cmd
    global pos, header, block_pos, final_data, multi_chunk

    header = block_header + bytes([size]) + block_filler + chunk_header + bytes([cmd]) + bytes([sub_cmd])
    snd_data = header

    pos = 1
    block_pos = 0x10 + 0x06 + 1
    
    this_cmd = cmd
    this_sub_cmd = sub_cmd
    multi_chunk = multi

    format_byte = 0
    tmp_data = b''
    
    if multi_chunk:
        format_byte = 4             # I don't know why - seems wrong but it is CRITICAL this is 4 for the non-final chunks
        tmp_data += b'\x03' + bytes([this_chunk]) + b'\x00'            # mutli-chunk header - assumes 3 chunks
        pos += 3
        block_pos += 3       

def end_chunk():
    global snd_data, tmp_data, format_byte, pos, block_pos

#    add_pack (b'\xf7', False)
    tmp_data += b'\xf7'
    pos += 1
    block_pos += 1

    if pos == 8:
        snd_data += bytes([format_byte])
        snd_data += tmp_data
        format_byte = 0
        pos = 1
        block_pos += 1
        tmp_data = b''

    if len(tmp_data) == 1:
        snd_data += tmp_data        # last byte is 0xf7 so we don't need a format byte
    elif len(tmp_data) > 1:
        snd_data += bytes([format_byte])
        snd_data += tmp_data
       

def start_packing (cmd, sub_cmd, multi = False):
    global final_data, this_chunk

    final_data = []
    this_chunk = 0
    pack_header (cmd, sub_cmd, multi)
    
        
def add_pack (msg, setformat = True):
    global snd_data, tmp_data, pos, format_byte, block_pos, this_chunk, multi_chunk, final_data


    if setformat == True:
        format_byte |= (1 << (pos-1))
        
    for i in range (0, len(msg)):
        tmp_data += bytes([msg[i]])
        pos += 1
        block_pos += 1

        if pos == 8:
            snd_data += bytes([format_byte])
            snd_data += tmp_data
            format_byte = 0
            pos = 1
            block_pos += 1
            tmp_data = b''

        if (block_pos == max_size - 1) and multi_chunk:
            end_chunk ()
            this_chunk += 1
            size = len(snd_data)
            end_msg = snd_data[0:6] + bytes([size]) + snd_data[7:]
            final_data.append(end_msg)
            
            pack_header(this_cmd, this_sub_cmd, True)
         


def end_pack(): 
    global snd_data, tmp_data, pos, format_byte, final_data, multi_chunk

    end_chunk()
    
    # update the block size field        
    block_size = len(snd_data)
    end_msg = snd_data[0:6] + bytes([block_size]) + snd_data[7:]
    final_data.append(end_msg)
    
    # update chunk size and counts for all chunks
    if multi_chunk:
        num_chunks = len (final_data)
        for m in range(0, num_chunks):
            tmp_msg = final_data[m]
            
            if m == num_chunks - 1:   #  last chunk
                s1 = block_size - 16 - 6 - 4 - 1
                chunk_size = s1 - int ((s1+2) / 8)
            else:
                chunk_size = 0
            
            end_msg = tmp_msg[0:23] + bytes ([num_chunks]) + bytes ([m]) + bytes([chunk_size]) + tmp_msg[26:]
            final_data[m] = end_msg

    return final_data

######## Helper functions for packing data types

def add_prefixed_string(pack_str):
    add_pack ([len(pack_str)], False)
    add_pack (bytes([len(pack_str)+0x20]) + bytes(pack_str, 'utf-8'))

def add_string(pack_str):
    add_pack (bytes([len(pack_str)+0x20]) + bytes(pack_str, 'utf-8'))

def add_long_string(pack_str):
    add_pack (b'\x59')
    add_pack (bytes([len(pack_str)]) + bytes(pack_str, 'utf-8'), False)    

def add_float(flt):
    bytes_val = struct.pack(">f", flt)
    add_pack (b'\x4a' + bytes_val)

def add_onoff (onoff):
    if onoff == "On":
        b = b'\x43'
    else:
        b = b'\x42'
    add_pack(b)
    
######## Functions to package a command for the Spark


def pack_parameter_change (pedal, param, val):
    cmd = 0x01
    sub_cmd = 0x04
    
    start_packing (cmd, sub_cmd)
    add_prefixed_string (pedal)
    add_pack ([param])
    add_float(val)
    return end_pack ()


def pack_pedal_change (pedal1, pedal2):
    cmd = 0x01
    sub_cmd = 0x06

    start_packing (cmd, sub_cmd)
    add_prefixed_string (pedal1)
    add_prefixed_string (pedal2)
    return end_pack ()

def pack_hardware_preset_change (preset_num):    # preset_num is 0 to 3
    cmd = 0x01
    sub_cmd = 0x38

    start_packing (cmd, sub_cmd)
    add_pack ([0], False)
    add_pack ([preset_num], False)          ##### CHANGED
    return end_pack ()

def pack_turn_pedal_onoff (pedal, onoff):
    cmd = 0x01
    sub_cmd = 0x15

    start_packing (cmd, sub_cmd)
    add_prefixed_string (pedal)
    add_onoff (onoff)
    return end_pack ()    


def pack_preset (preset):
    global this_chunk, tmp_data, snd_data
    
    cmd = 0x01
    sub_cmd = 0x01
    this_chunk = 0

    start_packing (cmd, sub_cmd, True)

    add_pack (b'\x00\x7f', False)       
    add_long_string (preset["UUID"])
    add_string (preset["Name"])
    add_string (preset["Version"])
    add_string (preset["Description"])
    add_string (preset["Icon"])
    add_float (preset["BPM"])
    add_pack (bytes([0x10 + 7]))        # always 7 pedals
    for i in range (0, 7):
        add_string (preset["Pedals"][i]["Name"])
        add_onoff (preset["Pedals"][i]["OnOff"])
        num_p = len(preset["Pedals"][i]["Parameters"])
        add_pack (bytes([num_p + 0x10]))
        for p in range (0, num_p):
              add_pack (bytes([p]), False) 
              add_pack (b'\x11')
              add_float (preset["Pedals"][i]["Parameters"][p])
    add_pack (bytes([preset["End Filler"]]))                   
    return end_pack ()

######## Test program    


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
    '''
    print("Change to hardware preset 0")
    b = pack_hardware_preset_change(0)
    cs.send(b[0])
    r = cs.recv(100)
    time.sleep(3)

    print ("Sweep up gain")    
    for v in range (0, 100):
        val = v*0.01
        b = pack_parameter_change ("Twin", 0, val)
        cs.send(b[0])
        time.sleep(0.02)

    print ("Change amp from Twin to SLO 100")
    b = pack_pedal_change ("Twin", "SLO100")
    cs.send(b[0])
    r = cs.recv(100)
    time.sleep(3)

    print ("Change amp from SLO 100 to Twin")
    b = pack_pedal_change ( "SLO100", "Twin")
    cs.send(b[0])
    print(cs.recv(100))    
    time.sleep(3)

    print ("Turn on the Booster pedal")
    b = pack_turn_pedal_onoff  ( "Booster", "On")
    cs.send(b[0])
    r = cs.recv(100)
    time.sleep(3)

    print ("Booster gain to 9")
    b = pack_parameter_change ("Booster", 0, 0.9)
    cs.send(b[0])
    time.sleep(3)
           
    print ("Booster gain to 1")
    b = pack_parameter_change ("Booster", 0, 0.1)
    cs.send(b[0])
    time.sleep(3)
    
    print ("Turn off Booster")       
    b = pack_turn_pedal_onoff ( "Booster", "Off")
    cs.send(b[0])
    r = cs.recv(100)
    time.sleep(3)

    print ("Turn on the Booster pedal")
    b = pack_turn_pedal_onoff  ( "Booster", "On")
    cs.send(b[0])
    r = cs.recv(100)
    time.sleep(3)
    '''

                          
    print("Change to hardware preset 1")
    b = pack_hardware_preset_change(1)
    cs.send(b[0])
    r = cs.recv(100)
    time.sleep(3)
    
    
    print("Change to **my** Silver Ship")
    b = pack_preset(preset)
    for i in b:
        cs.send(i)
        r = cs.recv(100)
    b = pack_hardware_preset_change (0x7f)
    cs.send(b[0])
    r = cs.recv(100)
    time.sleep(10)

    
    print("Change to **my** Blues Ark")
    b = pack_preset(preset5)
    for i in b:
        cs.send(i)
        print ("11223344556677881122334455667788112233445566ffccmmll")
        print (i.hex())
        r = cs.recv(100)
    b = pack_hardware_preset_change (0x7f)
    cs.send(b[0])
    r = cs.recv(100)


  
except OSError as e:
    print(e)
    
finally:
    if cs is not None:
        cs.close()
    
