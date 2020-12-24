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
    # size could be anything and is replaced later
    size         = 33                                           
    block_filler = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    chunk_header = b'\xf0\x01\x3a\x15'
    max_block_size = 0xad

    def __init__(self):
        # block_data stores the full block of data
        self.block_data = b''
        # temp_data stores the bytes as they are being packaged, to allow the format byte to be created
        self.temp_data=b''
        # header for each block
        self.header = b''
        # position in the data, and in the block
        self.pos = 0
        self.block_pos = 0

        self.this_cmd = 0
        self.this_sub_cmd = 0

        self.multi_chunk = False
        # array for the output of each block
        self.final_data = []

    ######## Helper functions to package a command for the Spark (handles the 'format bytes'

    # Creates the block and chunk headers, clears the data ready to accept bytes
    # If a multi-chunk message, creates the three-byte sub-header and sets the format byte correctly
    
    def create_header(self, cmd, sub_cmd, multi):
        self.header = ( self.block_header + bytes([self.size]) +
                        self.block_filler + self.chunk_header +
                        bytes([cmd]) + bytes([sub_cmd]) )
        
        self.block_data = self.header

        # starting at position 1 in the data
        self.pos = 1
        # block starting postition is past all the headers
        self.block_pos = 0x10 + 0x06 + 1

        # store these so we can create each header for multi-chunk messages
        self.this_cmd = cmd
        self.this_sub_cmd = sub_cmd
        self.multi_chunk = multi

        self.format_byte = 0
        self.temp_data = b''
    
        if self.multi_chunk:
            # I don't know why - seems wrong but it is critial this is 4 except for the non-final chunks
            self.format_byte = 4
            # Mutli-chunk sub-header - assumes 3 chunks but replaced later
            self.temp_data += b'\x03' + bytes([self.this_chunk]) + b'\x00'
            self.pos += 3
            self.block_pos += 3       

    # Close this chunk - add the 0xf7 and flush any remaining data from temp_data into block_data
    def end_chunk(self):
        self.temp_data += b'\xf7'
        self.pos += 1
        self.block_pos += 1

        if len(self.temp_data) == 1:
            # last byte is 0xf7 so we don't need a format byte
            self.block_data += self.temp_data        
        elif len(self.temp_data) > 1:
            self.block_data += bytes([self.format_byte])
            self.block_data += self.temp_data
       
    # Start the process - clear the data and create the headers
    def start_message (self, cmd, sub_cmd, multi = False):
        self.final_data = []
        self.this_chunk = 0
        self.create_header (cmd, sub_cmd, multi)
    
    # Add bytes to a temporary message
    # If at the eighth byte flush this into the block_data message
    # If hit the size limit and a multi-chunk message then store block_data in final_data and start a new block
    def add_bytes (self, msg, setformat = True):
        if setformat == True:
            self.format_byte |= (1 << (self.pos-1))
        
        for i in range (0, len(msg)):
            self.temp_data += bytes([msg[i]])
            self.pos += 1
            self.block_pos += 1

            if self.pos == 8:
                self.block_data += bytes([self.format_byte])
                self.block_data += self.temp_data
                self.format_byte = 0
                self.pos = 1
                self.block_pos += 1
                self.temp_data = b''

            if (self.block_pos == self.max_block_size - 1) and self.multi_chunk:
                self.end_chunk()
                self.this_chunk += 1
                size = len(self.block_data)
                end_msg = self.block_data[0:6] + bytes([size]) + self.block_data[7:]
                self.final_data.append(end_msg)
            
                self.create_header(self.this_cmd, self.this_sub_cmd, True)
         


    def end_message(self): 
        self.end_chunk()
    
        # update the block size field        
        self.block_size = len(self.block_data)
        self.end_msg = self.block_data[0:6] + bytes([self.block_size]) + self.block_data[7:]
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
                    # very odd it sometimes doesn't like a 4 in the first format for the final chunk
                    format1 = format1 & 0xfb  
                else:
                    chunk_size = 0
            
                self.end_msg = ( tmp_msg[0:22] + bytes([format1]) +
                                 bytes ([num_chunks]) + bytes ([m]) +
                                 bytes([chunk_size]) + tmp_msg[26:] )
                self.final_data[m] = self.end_msg

        return self.final_data

    ######## Helper functions for packing data types

    def add_prefixed_string(self, pack_str):
        self.add_bytes ([len(pack_str)], False)
        self.add_bytes (bytes([len(pack_str)+0x20]) + bytes(pack_str, 'utf-8'))

    def add_string(self, pack_str):
        self.add_bytes (bytes([len(pack_str)+0x20]) + bytes(pack_str, 'utf-8'))

    def add_long_string(self, pack_str):
        self.add_bytes (b'\x59')
        self.add_bytes (bytes([len(pack_str)]) + bytes(pack_str, 'utf-8'), False)    

#    def add_float(self,flt):
#        bytes_val = struct.pack(">f", flt)
#        self.add_bytes (b'\x4a' + bytes_val)

    # floats are special - bit 7 is actually stored in the format byte and not in the data
    def add_float (self, flt):
        bytes_val = struct.pack(">f", flt)
        self.add_bytes(b'\x4a', True)
#        bv=b''
        for b in bytes_val:
            fmt_bit = ((b & 0x80) == 0x80)
            self.add_bytes(bytes([b & 0x7f]), fmt_bit)
#            bv += bytes([b & 0x7f])
#        if bytes_val != bv:
#             print ("ADDED FLOAT WITH DIFF", bytes_val, bv) 
           
    def add_onoff (self,onoff):
        if onoff == "On":
            b = b'\x43'
        else:
            b = b'\x42'
        self.add_bytes(b)
    
    ######## Functions to package a command for the Spark


    def change_effect_parameter (self, pedal, param, val):
        cmd = 0x01
        sub_cmd = 0x04
    
        self.start_message (cmd, sub_cmd)
        self.add_prefixed_string (pedal)
        self.add_bytes ([param])
        self.add_float(val)
        return self.end_message ()


    def change_effect (self, pedal1, pedal2):
        cmd = 0x01
        sub_cmd = 0x06

        self.start_message (cmd, sub_cmd)
        self.add_prefixed_string (pedal1)
        self.add_prefixed_string (pedal2)
        return self.end_message ()

    def change_hardware_preset (self, preset_num):
        # preset_num is 0 to 3
        cmd = 0x01
        sub_cmd = 0x38

        self.start_message (cmd, sub_cmd)
        self.add_bytes ([0], False)
        self.add_bytes ([preset_num], False)         
        return self.end_message ()

    def turn_effect_onoff (self, pedal, onoff):
        cmd = 0x01
        sub_cmd = 0x15

        self.start_message (cmd, sub_cmd)
        self.add_prefixed_string (pedal)
        self.add_onoff (onoff)
        return self.end_message ()    


    def create_preset (self, preset):
        cmd = 0x01
        sub_cmd = 0x01
        this_chunk = 0

        self.start_message (cmd, sub_cmd, True)
        self.add_bytes (b'\x00\x7f', False)       
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
        self.add_bytes (bytes([0x10 + 7]))        # always 7 pedals
        for i in range (0, 7):
            self.add_string (preset["Pedals"][i]["Name"])
            self.add_onoff (preset["Pedals"][i]["OnOff"])
            num_p = len(preset["Pedals"][i]["Parameters"])
            self.add_bytes (bytes([num_p + 0x10]))
            for p in range (0, num_p):
                self.add_bytes (bytes([p]), False) 
                self.add_bytes (b'\x11')
                self.add_float (preset["Pedals"][i]["Parameters"][p])
        self.add_bytes (bytes([preset["End Filler"]]))                   
        return self.end_message ()

