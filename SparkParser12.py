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

def read_byte():
    a=b''
    while not a:
        a=ser.read(1)
    return a


def send_ack():
    ser.write(m_ack)

# Next level functions

def get_block_header():
    global m_dir, m_size, m_pad
    global b_pos
    
    b_header = [0]*16
    for i in range (0,16):
        b_header[i]=read_byte()
    m_dir = b_header[4:6]
    m_size = ord(b_header[6])
    m_pad = b_header[7:16]

    b_pos = 17

def get_chunk_header():
    global m_fixed, m_seq1, m_seq2, m_cmd, m_param
    global b_pos, c_pos, c_size

    c_header = [0]*6
    for i in range (0,6):
        c_header[i]=read_byte()
    m_fixed = c_header[0:2]
    m_seq1 = ord(c_header[2])
    m_seq2 = ord(c_header[3])
    m_cmd = ord(c_header[4])
    m_param = ord(c_header[5])

    c_size = m_size - 16
    
    c_pos = 1
    b_pos += 6
   
def get_next_data():
    global b_pos, m_cmd, m_param, m_size
    global c_pos, chunk_total, chunk_this, c_size

    if (b_pos == m_size) and (m_cmd == 0x01) and (m_param == 0x01) and (m_size == 0xad): # and (chunk_this+1 < chunk_total):
        a = read_byte()             # should be 0xf7
        if m_dir == [b'S',b'\xfe']:
            send_ack()              # only if reading a 'sent' command
        get_block_header()
        get_chunk_header()
        print ("[Chunk format byte %0.2X]" % ord(read_byte()))
        chunk_total = ord(read_byte())
        chunk_this = ord(read_byte())
        print ("[Chunk  %d of %d]" % (chunk_this+1, chunk_total))
        print ("[Chunk unknown %0.2X]" % ord(read_byte()))
        b_pos += 4
        c_pos += 4
    
    a = read_byte()
#    if ((b_pos +1 ) % 8 == 0) and (b_pos < m_size): # it could be that 0xf7 is in the format byte!
    if (c_pos  % 8 == 1) and (c_pos < c_size):
        b_pos += 1
        c_pos += 1
        a = read_byte()
    b_pos += 1
    c_pos += 1
    return ord(a)

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
        get_block_header()
        get_chunk_header()
        print ("Size           ", m_size)
        print ("Sequence       ", m_seq1)
        print ("Sequence 2     ", m_seq2)
        print ("Command        ", m_cmd)
        print ("Parameter      ", m_param)

        m_ack = bytes.fromhex("01fe000041ff17000000000000000000f001" + "%0.2X" % m_seq1 + "0004" + "%0.2X" % m_cmd + "f7")

        if m_cmd == 0x01:
            if m_param == 0x01:  # send whole preset
                print ("Send whole preset")
                chunk_total = find_byte("Total chunks ")
                chunk_this = find_byte("This chunk   ")
                if chunk_this == 0:       # first chunk of preset
                    print ("Chunk %d of %d" % (chunk_this+1, chunk_total))
                    find_byte("Chunk related?")
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
            elif m_param == 0x15:  # enable / disable pedal
                print ("Enable / disable pedal")
                skip_byte()
                find_string("Pedal  ")
                find_boolean()
            elif m_param == 0x04: # change parameter
                print ("Change pedal parameter")
                skip_byte()
                find_string("Pedal  ")
                find_byte("Param  ")
                find_float()
            elif m_param == 0x06:  # change pedal
                print ("Change pedal")
                skip_byte()
                find_string("Old pedal      ")
                skip_byte()
                find_string("New pedal      ")
            elif m_param == 0x38:  # change between hardware presets
                print ("Change between presets")
                find_integer()
#        elif m_cmd == 4:
#            if m_param == 0x38:
#                print ("Got ACK")
#        elif m_cmd == 3:
#            if m_param == 1:
#                print ("Got a receive")
        else:         
            while b_pos < m_size:
                b = get_next_data()
                print ("Unknown command / parameter %0.2X" % b)
        b = get_next_data()
        print("===== Done %0.2X %d %d =======" % (b, b_pos, m_size))
        if m_dir == [b'S',b'\xfe']:
            send_ack()              # only if reading a 'sent' command


# This captures the bluetooth traffic sent on a serial port
# I am using a ESP32 board to mimick the Spark amp and capture bluetooth traffic and relay it to the serial port
# Can be altered to parse a bytearray or similar

ser=serial.Serial("COM7", 115200, timeout=0)

try:
    while True:
        process_message()
finally:
    ser.close()


