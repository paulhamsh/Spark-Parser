import serial
import struct

def inc_pos(pos, n=1):
    for i in range(n):
        pos=pos+1
        if (pos+2) % 8 ==0:
            pos=pos+1
    return pos
   
def process_message(s):       
    print()
    print()
    print (s.hex())
    print()
    print (s)
    print()
    if s[0:4] == b'\x01\xfe\x00\x00':
        m_dir = s[4:6]
        m_size = int.from_bytes(s[6:7], "big")
        m_pad = s[7:16]
        m_fixed = s[16:18]
        m_seq1 = s[18:19]
        m_seq2 = s[19:20]
        m_cmd = s[20:21]
        m_param = s[21:22]

        m_ack = b'\x01\xfe\x00\x00A\xff\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\x01'+m_seq1+b'\x00\x04'+m_cmd+b'\xf7'
        p = 22

        for i in range (0, 22):
            print (" %0.2X" % s[i], end="")
            if (i + 1) % 8 == 0:
                print()
        print ()
        print ()
        while p < m_size:
            val = s[p]
            if (p+2) % 8 == 0:
                print()
                print (" %0.2X   " % val, end="")
                p=p+1
                if p < m_size:
                    val = s[p]
            if p < m_size:
                print (" %0.2X" % val, end="")
            p=p+1
    return m_ack

# This captures the bluetooth traffic sent on a serial port
# I am using a ESP32 board to mimick the Spark amp and capture bluetooth traffic and relay it to the serial port
# Can be altered to parse a bytearray or similar

ser=serial.Serial("COM7", 115200, timeout=0)
while True:
    s=ser.read(255)

    if s:
        b = s.split(b'\x01\xfe\x00\x00')
        for a_msg in b:
            if a_msg:
                ack=process_message(b'\x01\xfe\x00\x00'+a_msg)
                ser.write(ack)


