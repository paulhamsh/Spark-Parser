import serial
import struct

global ser

##############    PUT YOUR PRESET HERE

dt1 = "01FE000053FEAD000000000000000000F001167B010124040000007F5924003936314637463400302D373743332D00344539382D41360039342D44463943004134303639393502352A4475616C2020547261696E2330042E373D446573630072697074696F6E0020666F7220526F00636B20507265731065742031286963406F6E2E706E674A3242700000172E62006961732E6E6F6940736567617465430D1200114A3E18670C0701114A00F7"
dt2 = "01FE000053FEAD000000000000000000F00116230101440401000000002E004242454F7074690063616C436F6D701B431300114A3F351A211501114A3F061B4E2D02114A00000400002D44697374006F7274696F6E546C5339431300114A6A3C0A4F3601114A663E3D441402114A103F381F7529526500637469666965721B431500114A3F345B653501114A3E595B224702114A3E6659230403114A3E7F1A1A0904114A3F4B051C0E26436CF7"
dt3 = "01FE000053FEAD000000000000000000F00116290101040402006F6E65725B421200114A3E291A767D01114A00000400002944656C6160794D6F6E6F42154600114A3E68021E4601114A3E10027B0602114A3F0D04574603114A3F0E51120604114A00000000012B626961732E7260657665726242177600114A3E3B5B724601114A3F2C17325602114A3E2117347603114A3E112F233604114A3E1A64093605114A3E5D65411606114A3E19F7"
dt4 = "01FE000053FE1E000000000000000000F0011679010138040303191A46F7"

preset = dt1 + dt2 + dt3 + dt4

##############


b_pos = 0
c_pos = 0


preset_pos =0

def read_byte():
    global preset_pos
    
    a = preset[preset_pos: preset_pos+2]
    preset_pos += 2
    b = bytes.fromhex(a)
    return b


# Next level functions

def get_block_header():
    global b_dir, b_size, b_pad, c_seq
    global b_pos
    
    b_header = [0]*16
    for i in range (0,16):
        b_header[i] = read_byte()
    b_dir = b_header[4:6]
    b_size = ord(b_header[6])
    b_pad = b_header[7:16]

    b_pos = 17

        
#Read bytes from the block - if the block is empty, read in a new block header and carry on
    
def block_read_byte():
    global b_pos, b_size, m_ack

    if b_pos == 0:          # a new block, so need to read block header
        get_block_header()

    b = read_byte()
    b_pos += 1

    if (b_pos > b_size):                                # just read last byte of the block
        b_pos = 0                                       # flag as new block

    return ord(b)


def get_multichunk_header():
    global c_pos, c_total, c_this
    
    block_read_byte()                                   # this will be the format byte, don't need it

    c_multi_header = [0] * 3
    for i in range (0,3):
        c_multi_header[i] = block_read_byte()
    c_total = c_multi_header[0]
    c_this  = c_multi_header[1]
    
    c_pos += 4                                          # 3 plus the format byte


def get_chunk_headers():
    global c_fixed, c_seq1, c_seq2, c_cmd, c_subcmd, m_ack
    global c_pos, c_size, c_total, c_this

    c_header = [0]*6
    for i in range (0,6):
        c_header[i] = block_read_byte()
    c_fixed = c_header[0:2]
    c_seq1 = c_header[2]
    c_seq2 = c_header[3]
    c_cmd = c_header[4]
    c_subcmd = c_header[5]

    if   (c_cmd == 0x04) and (c_subcmd == 0x38):         # ack packet, no chunk data
        c_size = 0
    elif (c_cmd == 0x03) and (c_subcmd == 0x01):         # read preset - chunks of 32
        c_size = 32
    else:                                               # should be a normal set command with a single chunk
        c_size = b_size - 22
        
    c_pos = 1
    
    if  ((c_cmd == 0x01) and (c_subcmd == 0x01)) or ((c_cmd == 0x03) and (c_subcmd == 0x01)):      # this is a multi-chunk message
        get_multichunk_header()

    m_ack = bytes.fromhex("01fe000041ff17000000000000000000f001" + "%0.2X" % c_seq1 + "0004" + "%0.2X" % c_cmd + "f7")


def get_next_data():
    global b_pos, c_cmd, c_subcmd, b_size
    global c_pos, c_size

    if (c_pos == 0):                                    # empty chunk
        get_chunk_headers()

        
    r = block_read_byte()
    if (c_pos % 8 == 1) and (c_pos < c_size):           # a format byte and not the end ie f7 (which it could be)
        r = block_read_byte()
        c_pos += 1

    c_pos += 1
    
    if (c_pos == c_size):                               # one byte left in chunk - should be xf7
        d = block_read_byte()                           # so get it and discard it
        c_pos = 0                                       # set the chunk to be empty
    return r





# ============================================================

def skip_byte(text="Skipping "):
    a=get_next_data()
    return a

def find_string(text="String "):
    a = get_next_data()
    if a == 0x59:
        s_len = get_next_data()
    else:
        s_len = a - 0x20
    s_str = ""
    for i in range (0, s_len):
        b = get_next_data()
        s_str += chr(b)
    return s_str
    
def find_byte(text="Byte   "):
    a = get_next_data();
    return a

   
def find_integer(text="Integer"):
    a = [0]*2
    a[0] = get_next_data();
    a[1] = get_next_data();
    return a

def find_float(text="Float"):
    a = [0]*4
    # This next byte should be 0x4a
    x = get_next_data();
    a[0] = get_next_data();
    a[1] = get_next_data();
    a[2] = get_next_data();
    a[3] = get_next_data();
    s = ""
    for i in range(0,4):
        s+="%0.2X" % a[3-i]
    b=bytes.fromhex(s)
    [f] = struct.unpack('f', b)
    return f

def find_boolean(text="Boolean"):
    b = get_next_data()
    return b
   
def process_message():       
    global m_ack
    global p
    global chunk_total, chunk_this

    print()
    print("=================== Start dump ===================")


    get_chunk_headers()

    if c_cmd == 0x01:
        if c_subcmd == 0x01:  # send whole preset
            print ("Send whole preset")
            preset = "preset = { "
            if c_this == 0:       # first chunk of preset
                b1 = find_byte("Unknown byte")
                b2 = find_byte("Unknown byte")
                preset += "\n\t\"Filler\": [0x%0.2x, 0x%0.2x], " % (b1,b2) 
                s = find_string("UUID            ")
                preset += "\n\t\"UUID\": \""+ s + "\","

                s = find_string("Preset name     ")
                preset +="\n\t\"Name\": \""+ s+  "\","
                s = find_string("Version         ")
                preset +="\n\t\"Version\": \""+ s+  "\","
                s = find_string("Description     ")
                preset +="\n\t\"Description\": \""+ s+  "\","
                s = find_string("Icon            ")
                preset +="\n\t\"Icon\": \""+ s+  "\","
                f = find_float("Unknown value   ")
                preset +="\n\t\"BPM\": %0.1f," % f
                num_pedals = find_byte("Num pedals") - 0x10
                preset +="\n\t\"Pedals\": [ "
                for r in range(0, num_pedals):
                    preset += "{ "
                    s = find_string("Pedal           ")
                    preset +="\n\t\t\"Name\": \""+ s+  "\","
                    b = find_boolean("On/off          ")
                    if b == 0x42:
                        s = "Off"
                    else:
                        s = "On"
                    preset +="\n\t\t\"OnOff\": \""+ s+  "\","
                    vals = find_byte("Params          ") - 0x10
                    preset +="\n\t\t\"Parameters\": ["
                    for s in range(0, vals):
                        find_byte("  Param         ")
                        find_byte("  ???           ")
                        f = find_float("  Value         ")
                        preset +="%0.6f" % f
                        if s < vals - 1:
                            preset += ", "
                        else:
                            preset += "] }"
                    if r < num_pedals - 1:
                        preset += ", "
                    else:
                        preset += "], "
                b = find_byte("Unknown byte")
                preset += "\n\t\"End Filler\": 0x%0.2x}" % b
                print (preset)
        elif c_subcmd == 0x15:  # enable / disable pedal
            print ("Enable / disable pedal")
            skip_byte()
            find_string("Pedal  ")
            find_boolean()
        elif c_subcmd == 0x04: # change parameter
            print ("Change pedal parameter")
            skip_byte()
            find_string("Pedal  ")
            find_byte("Param  ")
            find_float()
        elif c_subcmd == 0x06:  # change pedal
            print ("Change pedal")
            skip_byte()
            find_string("Old pedal      ")
            skip_byte()
            find_string("New pedal      ")
        elif c_subcmd == 0x38:  # change between hardware presets
            print ("Change between presets")
            find_integer()
    else:         
        while b_pos < b_size:
            b = get_next_data()
            print ("Unknown command / parameter %0.2X" % b)
    print("===== Done  =======" )



# This captures the bluetooth traffic sent on a serial port
# I am using a ESP32 board to mimick the Spark amp and capture bluetooth traffic and relay it to the serial port
# Can be altered to parse a bytearray or similar

process_message()



