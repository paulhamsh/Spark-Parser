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
        m_seq = s[18:20]
        m_cmd = s[20:22]

        print ("Size           ", m_size)
        print ("Sequence       ", m_seq.hex())
        print ("Command        ", m_cmd.hex())
        p = 23
        while p < m_size:
            arg_type =int.from_bytes(s[p:p+1], "big")
            p=inc_pos(p)
            if arg_type == 0x00:
                arg_val = int.from_bytes(s[p:p+2],"big")
                print ("  00: Int         ",arg_val)
                p=inc_pos(p,2)
            elif (arg_type >=0x01) and (arg_type <= 0x1F):
                print("  {:0X}: Unknown     ".format(arg_type))
            elif (arg_type >= 0x20) and (arg_type <= 0x3F):
                s_len = arg_type - 0x20
                s_ctr=0
                s_str=""
                while s_ctr < s_len:
                    s_str+=str(s[p:p+1], 'utf-8')
                    s_ctr+=1
                    p=inc_pos(p)
                print ("  xx: String      ", s_str)
            elif arg_type == 0x4a:
                v=s[p+3:p+4]+s[p+2:p+3]+s[p+1:p+2]+s[p:p+1]
                [val]=struct.unpack('f',v)
                print ("  4a: Float       ", val)
                p=inc_pos(p,4)
            elif arg_type == 0x59:
                s_ctr=0
                s_str=""
                s_len = 36
                p=inc_pos(p)
                while s_ctr < s_len:
                    s_str+=str(s[p:p+1], 'utf-8')
                    s_ctr+=1
                    p=inc_pos(p)
                print ("  59: UUID        ", s_str)                    
            elif arg_type == 0x42:
                print ("  42: Boolean      true")
            elif arg_type == 0x43:
                print ("  43: Boolean      false")
            elif arg_type == 0xf7:
                print ("   End of message")        
            else:
                print ("  {:0X}: Unknown     ".format(arg_type))
                

ser=serial.Serial("COM7", 115200, timeout=0)
while True:
    s=ser.read(5000)
    if s:
        b = s.split(b'\x01\xfe\x00\x00')
        for a_msg in b:
            if a_msg: 
                process_message(b'\x01\xfe\x00\x00'+a_msg);

