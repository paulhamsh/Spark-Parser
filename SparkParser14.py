import serial
import struct

global ser

'''

rb = 0

inp = ("01fe000041ff6a000000000000000000f00120000438f7f001046b0301200f001900005924003734323532313100372d433241412d00343133352d3846f7f00104190301000f011939322d370043464441303146103531363727312d20436c65616e2330f7f001044203"
    "01fe000041ff6a00000000000000000001200f02192e372731402d436c65616e280069636f6e2e706e4a674a4270000017f7f00104090301080f03192e62696100732e6e6f69736530676174654313003b114a3d756e4301f7f001046d0301580f0419114a3e29192f1201fe000041ff6a00000000000000000002114a00000400002a436f6d7040726573736f7243f7f00104260301680f05191200114a6e3e2a3b1001114a143f7f474b27426f606f737465724311f7f001041d0301300f061900114a3f080f1f7824547769366e431500114a"
    "01fe000041ff6a0000000000000000003f341d097901114a3ef7f00104460301280f071961740a021b114a3e417054032b114a3e7b13490453114a3f2079532cf7f00104370301000f081943686f72007573416e616c6f3667421400114a3e3541153201114a3ff7f00101fe000041ff6a000000000000000000042c0301000f0919115b1e0223114a3e5d4944034b114a3e000000290044656c61794d6ff7f00104760301600f0a196e6f43156600114a3e1f31206601114a3e6e24611602114a3e7b2457f7f00104590301300f0b1903114a3f"
    "01fe000041ff6a000000000000000000341b556a04114a3f090000002b62696100732e7265766572f7f00104070301300f0c19624317000b114a3e2d3027013b114a3e28193b023b114a3e60173203f7f00104240301180f0d19114a3f315b162004114a3e795b797a0501fe000041ff2b000000000000000000114a3e6e594a3806114a3e19f7f00104640301180f0e03191a7df7")
    

def read_byte():
    global rb
    r = bytes.fromhex(inp[rb*2:rb*2+2])
    rb+=1
    return r   

# Low level get and send fuctions

'''

b_pos = 0
c_pos = 0

def read_byte():
    a = b''
    while not a:
        a = ser.read(1)
    return a


def send_ack():
    ser.write(m_ack)

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
        if (c_subcmd != 0x04):
            send_ack()                                  # so must send an ack - but not for a parameter change
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
    print (text, "%0.2X" % a)

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
    print (text, s_str)

    
def find_byte(text="Byte   "):
    a = get_next_data();
    print (text, "%0.2X" % a)   
    return a

   
def find_integer(text="Integer"):
    a = [0]*2
    a[0] = get_next_data();
    a[1] = get_next_data();
    print (text, a)

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
    
    
    print (text,  "%1.2f" % f, a)
    return

def find_boolean(text="Boolean"):
    b = get_next_data()
    if b == 0x42:
        print(text, "True")
    elif b == 0x43:
        print(text, "False")
    else:
        print("Not a Boolean")

   
def process_message():       
    global m_ack
    global p
    global chunk_total, chunk_this

    print()
    print("=================== Start dump ===================")

    while True: 
        get_chunk_headers()

        if c_cmd == 0x01:
            if c_subcmd == 0x01:  # send whole preset
                print ("Send whole preset")
                if c_this == 0:       # first chunk of preset
                    find_byte("Unknown byte")
                    find_byte("Unknown byte")
                    find_string("UUID            ")
                    find_string("Preset name     ")
                    find_string("Version         ")
                    find_string("Description     ")
                    find_string("Icon            ")
                    find_float("Unknown value   ")
                    pedals = find_byte("Num pedals") - 0x10
                    print ("There are %d pedals in this preset" % pedals)
                    for r in range(0, pedals):
                        find_string("Pedal           ")
                        find_boolean("On/off          ")
                        vals = find_byte("Params          ") - 0x10
                        print ("There are %d parameters for this pedal" % vals)
                        for s in range(0, vals):
                            find_byte("  Param         ")
                            find_byte("  ???           ")
                            find_float("  Value         ")
                    find_byte("Unknown byte")
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
#        elif c_cmd == 4:
#            if c_subcmd == 0x38:
#                print ("Got ACK")
#        elif c_cmd == 3:
#            if c_subcmd == 1:
#                print ("Got a receive")
        else:         
            while b_pos < b_size:
                b = get_next_data()
                print ("Unknown command / parameter %0.2X" % b)
        print("===== Done  =======" )



# This captures the bluetooth traffic sent on a serial port
# I am using a ESP32 board to mimick the Spark amp and capture bluetooth traffic and relay it to the serial port
# Can be altered to parse a bytearray or similar

ser=serial.Serial("COM7", 115200, timeout=0)

try:
    while True:
        process_message()
finally:
    ser.close()


