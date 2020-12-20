########
#
# Spark Class
#
# Class to package commands to send to Positive Grid Spark
#
# See https://github.com/paulhamsh/Spark-Parser


import struct


class SparkMessage:


    block_header = b'\x01\xfe\x00\x00\x53\xfe'
    size         = 33                                           # could be anything, will be replaced
    block_filler = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    chunk_header = b'\xf0\x01\x3a\x15'
    this_chunk = 0
    max_size = 0xad

    def __init__(self):
        self.snd_data = b''
        self.this_cmd = 0
        self.this_sub_cmd = 0
        self.multi = False
        self.pos = 0
        self.header = b''
        self.block_pos = 0
        self.final_data = 0
        self.multi_chunk = False
        self.tmp_data=b''
        self.end_msg=b''


    ######## Helper functions to package a command for the Spark (handles the 'format bytes'

    def pack_header(self, cmd, sub_cmd, multi):
#        global snd_data, tmp_data, format_byte, this_chunk, this_cmd, this_sub_cmd
#        global pos, header, block_pos, final_data, multi_chunk

        self.header = self.block_header + bytes([self.size]) + self.block_filler + self.chunk_header + bytes([cmd]) + bytes([sub_cmd])
        self.snd_data = self.header

        self.pos = 1
        self.block_pos = 0x10 + 0x06 + 1
    
        self.this_cmd = cmd
        self.this_sub_cmd = sub_cmd
        self.multi_chunk = multi

        self.format_byte = 0
        self.tmp_data = b''
    
        if self.multi_chunk:
            self.format_byte = 4             # I don't know why - seems wrong but it is CRITICAL this is 4 except for the non-final chunks
            self.tmp_data += b'\x03' + bytes([self.this_chunk]) + b'\x00'            # mutli-chunk header - assumes 3 chunks
            self.pos += 3
            self.block_pos += 3       

    def end_chunk(self):
#        global snd_data, tmp_data, format_byte, pos, block_pos

        self.tmp_data += b'\xf7'
        self.pos += 1
        self.block_pos += 1

        if len(self.tmp_data) == 1:
            self.snd_data += self.tmp_data        # last byte is 0xf7 so we don't need a format byte
        elif len(self.tmp_data) > 1:
            self.snd_data += bytes([self.format_byte])
            self.snd_data += self.tmp_data
       

    def start_packing (self, cmd, sub_cmd, multi = False):
#        global final_data, this_chunk

        self.final_data = []
        self.this_chunk = 0
        self.pack_header (cmd, sub_cmd, multi)
    
        
    def add_pack (self, msg, setformat = True):
#        global snd_data, tmp_data, pos, format_byte, block_pos, this_chunk, multi_chunk, final_data


        if setformat == True:
            self.format_byte |= (1 << (self.pos-1))
        
        for i in range (0, len(msg)):
            self.tmp_data += bytes([msg[i]])
            self.pos += 1
            self.block_pos += 1

            if self.pos == 8:
                self.snd_data += bytes([self.format_byte])
                self.snd_data += self.tmp_data
                self.format_byte = 0
                self.pos = 1
                self.block_pos += 1
                self.tmp_data = b''

            if (self.block_pos == self.max_size - 1) and self.multi_chunk:
                self.end_chunk()
                self.this_chunk += 1
                size = len(self.snd_data)
                end_msg = self.snd_data[0:6] + bytes([size]) + self.snd_data[7:]
                self.final_data.append(end_msg)
            
                self.pack_header(self.this_cmd, self.this_sub_cmd, True)
         


    def end_pack(self): 
#        global snd_data, tmp_data, pos, format_byte, final_data, multi_chunk

        self.end_chunk()
    
        # update the block size field        
        self.block_size = len(self.snd_data)
        self.end_msg = self.snd_data[0:6] + bytes([self.block_size]) + self.snd_data[7:]
        self.final_data.append(self.end_msg)
    
        # update chunk size and counts for all chunks
        if self.multi_chunk:
            num_chunks = len (self.final_data)
            for m in range(0, num_chunks):
                tmp_msg = self.final_data[m]
                format1 = tmp_msg[22]
           
                if m == num_chunks - 1:   #  last chunk
                    s1 = self.block_size - 16 - 6 - 4 - 1
                    chunk_size = s1 - int ((s1+2) / 8)
                    format1 = format1 & 0xfb  # very odd it sometimes doesn't like a 4 in the first format for the final chunk
                else:
                    chunk_size = 0
            
                self.end_msg = tmp_msg[0:22] + bytes([format1]) + bytes ([num_chunks]) + bytes ([m]) + bytes([chunk_size]) + tmp_msg[26:]
                self.final_data[m] = self.end_msg

        return self.final_data

    ######## Helper functions for packing data types

    def add_prefixed_string(self, pack_str):
        self.add_pack ([len(pack_str)], False)
        self.add_pack (bytes([len(pack_str)+0x20]) + bytes(pack_str, 'utf-8'))

    def add_string(self, pack_str):
        self.add_pack (bytes([len(pack_str)+0x20]) + bytes(pack_str, 'utf-8'))

    def add_long_string(self, pack_str):
        self.add_pack (b'\x59')
        self.add_pack (bytes([len(pack_str)]) + bytes(pack_str, 'utf-8'), False)    

    def add_float(self,flt):
        bytes_val = struct.pack(">f", flt)
        self.add_pack (b'\x4a' + bytes_val)

    def add_onoff (self,onoff):
        if onoff == "On":
            b = b'\x43'
        else:
            b = b'\x42'
        self.add_pack(b)
    
    ######## Functions to package a command for the Spark


    def pack_parameter_change (self, pedal, param, val):
        cmd = 0x01
        sub_cmd = 0x04
    
        self.start_packing (cmd, sub_cmd)
        self.add_prefixed_string (pedal)
        self.add_pack ([param])
        self.add_float(val)
        return self.end_pack ()


    def pack_pedal_change (self, pedal1, pedal2):
        cmd = 0x01
        sub_cmd = 0x06

        self.start_packing (cmd, sub_cmd)
        self.add_prefixed_string (pedal1)
        self.add_prefixed_string (pedal2)
        return self.end_pack ()

    def pack_hardware_preset_change (self, preset_num):    # preset_num is 0 to 3
        cmd = 0x01
        sub_cmd = 0x38

        self.start_packing (cmd, sub_cmd)
        self.add_pack ([0], False)
        self.add_pack ([preset_num], False)         
        return self.end_pack ()

    def pack_turn_pedal_onoff (self, pedal, onoff):
        cmd = 0x01
        sub_cmd = 0x15

        self.start_packing (cmd, sub_cmd)
        self.add_prefixed_string (pedal)
        self.add_onoff (onoff)
        return self.end_pack ()    


    def pack_preset (self, preset):
        global this_chunk, tmp_data, snd_data
    
        cmd = 0x01
        sub_cmd = 0x01
        this_chunk = 0

        self.start_packing (cmd, sub_cmd, True)

        self.add_pack (b'\x00\x7f', False)       
        self.add_long_string (preset["UUID"])
        self.add_string (preset["Name"])
        self.add_string (preset["Version"])
        descr = preset["Description"]
        if len (descr) > 31:
            self.add_long_string (descr)
        else:
            self.add_string (descr)
        self.add_string (preset["Icon"])
        self.add_float (preset["BPM"])
        self.add_pack (bytes([0x10 + 7]))        # always 7 pedals
        for i in range (0, 7):
            self.add_string (preset["Pedals"][i]["Name"])
            self.add_onoff (preset["Pedals"][i]["OnOff"])
            num_p = len(preset["Pedals"][i]["Parameters"])
            self.add_pack (bytes([num_p + 0x10]))
            for p in range (0, num_p):
                self.add_pack (bytes([p]), False) 
                self.add_pack (b'\x11')
                self.add_float (preset["Pedals"][i]["Parameters"][p])
        self.add_pack (bytes([preset["End Filler"]]))                   
        return self.end_pack ()

