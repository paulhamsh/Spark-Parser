########
#
# Spark Lib
#
# Program to package commands to send to Positive Grid Spark
#
# See https://github.com/paulhamsh/Spark-Parser

#### PRESETS ####


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
        format_byte = 4             # I don't know why - seems wrong but it is CRITICAL this is 4 except for the non-final chunks
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
            format1 = tmp_msg[22]
           
            if m == num_chunks - 1:   #  last chunk
                s1 = block_size - 16 - 6 - 4 - 1
                chunk_size = s1 - int ((s1+2) / 8)
                format1 = format1 & 0xfb  # very odd it sometimes doesn't like a 4 in the first format for the final chunk
            else:
                chunk_size = 0
            
            end_msg = tmp_msg[0:22] + bytes([format1]) + bytes ([num_chunks]) + bytes ([m]) + bytes([chunk_size]) + tmp_msg[26:]
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
    descr = preset["Description"]
    if len (descr) > 31:
        add_long_string (descr)
    else:
        add_string (descr)
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

