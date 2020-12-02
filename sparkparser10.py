import serial
import struct

global ser, fd


# Low level get and send fuctions

def read_byte():
    a=b''
    while not a:
        a=ser.read(1)
    return a


def send_ack():
    ser.write(m_ack)

# Next level functions

def get_header():
    global m_dir, m_size, m_pad, m_fixed, m_seq1, m_seq2, m_cmd, m_param
    global p
    
    m_header = [0]*22
    for i in range (0,22):
        m_header[i]=read_byte()
    m_dir = m_header[4:6]
    m_size = ord(m_header[6])
    m_pad = m_header[7:16]
    m_fixed = m_header[16:18]
    m_seq1 = ord(m_header[18])
    m_seq2 = ord(m_header[19])
    m_cmd = ord(m_header[20])
    m_param = ord(m_header[21])
    
    p = 23

   
def get_next_data():
    global p
    global chunk_total, chunk_this

    if (p == m_size) and (m_cmd == 0x01) and (m_param == 0x01) and (chunk_this+1 < chunk_total):
        a = read_byte()
        send_ack()
        get_header()
        print ("[Chunk format byte %0.2X]" % ord(read_byte()))
        chunk_total = ord(read_byte())
        chunk_this = ord(read_byte())
        print ("[Chunk  %d of %d]" % (chunk_this+1, chunk_total))
        print ("[Chunk unknown %0.2X]" % ord(read_byte()))
        p += 4
    
    a = read_byte()
    if ((p+1) % 8 == 0) and (p < m_size): # it could be that 0xf7 is in the format byte!
        p = p + 1
        a = read_byte()
    p = p + 1
    return ord(a)

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
    print()

    while True: 
        get_header()
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
                    find_byte()
                    find_byte()
                    find_byte()
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
                while p < m_size:
                    b = get_next_data()
                    print ("skipping  %0.2X - after preset ended" % b)
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
        else:         
            while p < m_size:
                b = get_next_data()
                print ("Unknown command / parameter %0.2X" % b)
        b = get_next_data()
        while b != 0xF7: # in the edge case of a header being read just above!
            print ("Skipping %0.2X - looking for 0xf7" % b)
            b = get_next_data()
        print("===== Done %0.2X %d %d =======" % (b, p, m_size))
        send_ack()


# This captures the bluetooth traffic sent on a serial port
# I am using a ESP32 board to mimick the Spark amp and capture bluetooth traffic and relay it to the serial port
# Can be altered to parse a bytearray or similar

ser=serial.Serial("COM7", 115200, timeout=0)

try:
    while True:
        process_message()
finally:
    ser.close()


