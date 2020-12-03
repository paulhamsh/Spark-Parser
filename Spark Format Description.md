# Reverse engineering the bluetooth message format used for app to amp communications

By ytsibizov.
Additional information from paulhamsh.

Messages are exhcanged in the data frame format.
When the app sends a message then the Spark responds with an acknowledgemnent.

Large transfers (such as a new preset) are sent in packets of length 0xad (173 decimal).

# Data message format

All numbers in hexadecimal

| Offset | Length | Data                                                  |
|--------|--------|-------------------------------------------------------|
|     00 |      4 | Header 01fe0000                                       |
|     04 |      2 | Direction                                             |
|     06 |      1 | Size of message (including the 6 byte header)         |
|     07 |      9 | Zeros                                                 |
|     10 |      2 | Fixed f001                                            |
|     12 |      1 | Sequence number                                       |
|     13 |      1 | Sequnce number follow on?????                         |
|     14 |      1 | Command                                               |
|     15 |      1 | Sub-command                                           |
|     16 |        | Message body                                          |
|     ?? |      1 | End of message f7                                     |

## Data frame elements

### Header

| Offset | 00 | 01 | 02 | 03 |
|--------|----|----|----|----|
| Data   | 01 | fe | 00 | 00 |

### Direction 

| Offset | 04 | 05 | Description         |
|--------|----|----|---------------------|
| Data   | 41 | ff | Received from Spark |
| Data   | 53 | fe | Sent to Spark       |

### Size of message

| Offset | 06     | Description                |
|--------|--------|----------------------------|
| Data   | length | Number of bytes in message |

### Zeros

| Offset | 07 | 08 | 09 | 0A | 0B | 0C | 0D | 0E | 0F |
|--------|----|----|----|----|----|----|----|----|----|
| Data   | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 |

### Fixed

| Offset | 10 | 11 |
|--------|----|----|
| Data   | f0 | 01 |

### Sequence number

This remains the same for a multi-packet message.   
It is also used in the acknowledgement message.   

| Offset |  12              |  
|--------|------------------|
| Data   |  sequence number |

### Sequence number follow-on

| Offset |  13                           |  
|--------|-------------------------------|
| Data   |  sequence number follow-on ?? |

It is known (from the existing working code) that this number is never checked by the amp.

### Command and sub-command

The command is also used in the acknowledgement message.  

| Offset |  14       |  15         |
|--------|-----------|-------------|
| Data   | command   | sub-command |

This is then followed by the message body (see below)  

### Trailer

| Offset | xx |
|--------|----|
| Data   | f7 |



## Message body

The body of the message made of sequences of 8 bytes - 1 format byte and then 7 bytes of data. 
Arguments are sequential in the data sequence and the format byte shows where new a new argument starts.
Each bit maps to a byte in the next sequence, and if the bit is set in the format byte then that byte in the sequence is the start of a new data element.
Strings have their length as their first byte (stored as 0x20 + length).

An example is shown below, with each new data sequence on a new line. The bit expansion is the format byte with the bits reversed, to show where the new sequence starts.

Exploring the data it doesn't look like the format bits are always correct.  
It seems that each command / sub-command has a specific set of parameters and these bits are not required.  

```
     F1   D1 D2 D3 D4   D5 D6 D7               Reversed bit expansion of F1
     02   xx                                   0100 000x
             2b 52 6f   79 61 62 x
     40   20 43 72 6f   77 6e                  0000 001x
                              23 
     08   30 2e 37                             0001 000x
                   27   31 2d 43 
     10   6c 65 61 6e                          0000 100x
                        28 69 63
     40   6f 63 2e 70   6e 67                  0000 001x
                              4a 
     32   42                                   0100 110x 
             70 00 00   
                        17 
                           2e 62        
     00   69 61 73 2e   6e 6f 69               0000 000x
     40   73 65 67 61   74 65                  0000 001x
                                 xx
```

Which translates to:  

```
     String: Royal Crown   
     String: 0.7  
     String: 1-Clean  
     String: icon.png  
     Float:  42 70 00 00  
     Byte:   17  
     String: .bias.noisegate  
```

It appears that strings are the only variable length data sequence and the only sequence that starts with a length

### Data types

| Type                             |   Length |  Example                                                                              |
|----------------------------------|----------|---------------------------------------------------------------------------------------|
| Byte                             |        1 | 00 - ff                                                                               | 
| Integer number, big endian ??    |        2 | 0000 - ffff                                                                           |
| Short string                     |     1-31 | Length + 0x20, bytes of string (sometimes prefixed by length, then length + 0x20 etc) |
| Long string                      |     32 + | 0x59 + length + bytes of string                                                       |
| Boolean "True"                   |        1 | 0x42                                                                                  |
| Boolean "False"                  |        1 | 0x43                                                                                  |
| Float                            |    4 + 1 | Prefix 0x49 + 4 bytes of floating point                                               |


## Commands

| Value | Command     |
|-------|-------------|
|  01   | Set         |
|  02   | Get         | 
|  04   | Ack         |


## SET command

Following SET operations are known:

| Sub-command | Description            | Arguments
|-------------|------------------------|-----------------------------------------------------------
| 01          | Send preset            | *UUID*, preset name, version, description, *float*, *byte*, noisegate name, boolean, ?,?, float, 
| 02          | Change value  ??       | ??
| 04          | Change parameter       | String: pedal name, Byte: parameter reference, Float: new value
| 06          | Change pedal           | String: old pedal name, String: new pedal name
| 15          | Enable/disable a pedal | String: pedal name, Boolean: on/off
| 23          |                        |
| 24          |                        |
| 38          | Change to preset       | Int: preset number (0 - 3)

### 01 Send preset sub-command

A new preset is a multi-packet message.   
Each packet starts with two bytes for the total number of packets and which packet this is.  
Each packet also has the same sequence number in the header.   

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  Byte    |      1 | Number of packets in total (1- )                      |
|  Byte    |      1 | Reference for this packet (0- )                       |
|  Byte    |      1 | ??                                                    |

Followed by:

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  Byte    |      1 | ??                                                    |
|  Byte    |      1 | ??                                                    |
|  UUID    |     36 | UUID for preset                                       |
|  String  |      x | Preset name                                           |
|  String  |      x | Version                                               |
|  String  |      x | Preset description                                    |
|  String  |      x | Icon name ??                                          |
|  Float   |      4 | ??    Perhaps BPM (seems to be 60.0)                  |
|  Byte    |      1 | ??    Perhaps number of pedals in preset              |

Followed by information for each pedal / amp:

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  String  |      x | Pedal name                                            |
|  Boolean |      1 | On/off                                                |
|  Byte    |      1 | Number of parameters following (+0x10)                |

Each pedal header is followed by values for each pedal parameter:

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  Byte    |      1 | Parameter reference (starts at 0)                     |
|  Byte    |      1 | 11 ??                                                 |
|  Float   |      4 | Parameter value                                       |
|          |        |                                                       |
|  Byte    |      1 | Parameter reference (starts at 0)                     |
|  Byte    |      1 | 11 ??                                                 |
|  Float   |      4 | Parameter value                                       |
|          |        |                                                       |
|   ...    |    ... | ...                                                   |
 
### 04 Change parameter (the value of a switch / dial on a pedal) sub-command

Arguments are a string for the pedal name, a byte for which parameter is being altered (starting at 0) and a float for the new value.

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  Byte    |      1 | (String length ??)                                    |
|  String  |      x | Pedal name                                            |
|  Byte    |      1 | Parameter reference                                   |
|  Float   |      4 | Parameter value (0.xx represents x.x in UI)           |

### 06 Swap pedals sub-command

Arguments are a string for the current pedal name, and string for new pedal name.

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  Byte    |      1 | (String length ??)                                    |
|  String  |      x | Old pedal name                                        |
|  Byte    |      1 | (String length ??)                                    |
|  Float   |      4 | New pedal name                                        |

### 15 Enable/disable a pedal sub-command

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  Byte    |      1 | (String length??)                                     |
|  String  |      x | Pedal name                                            |
|  Boolean |      1 | Pedal on / off                                        |

There is no consensus on what "True" value means, for different positions (maybe even pedals?) it is different.

| Position       | Active     | Disabled   |
|----------------|------------|------------|
| 0 (noise gate) | 42 (True)  | 43 (False) |
| 1 (compressor) | 42 (True)  | 43 (False) |
| 2 (distortion) | 43 (False) | 42 (True)  |
| 3 (amp)        | -          | -          |
| 4 (chorus)     | 43 (False) | 42 (True)  |
| 5 (delay)      | 43 (False) | 42 (True)  |

### 38 Change preset sub-command

Only argument is an integer for which preset to select (0-3)

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  Integer |      2 | Preset reference (0-3)                                |

## GET Commands

Following GET operations are known:

| Sub-command |                          |
|-------------|--------------------------|
|  01         | Get preset configuration |
|  02         | ???                      |
|  11         | Get device name          |
|  23         | Get serial number        |

### 01 Get preset configuration

Multiple arguments, only first one is actually used

 - Integer number - Preset number starting 0, or 0x0100 for "current"
 - 34x "0x00" (that is 11x "Integer number, value 0" + 0x00)
 ???

## ACK packet

After a successful operation, amp sends back an "ack" packet.
This has the command 0x04, the same sequence number as the original packet and a sub-command the same as the sub-command sent to the Spark

## Pedal names

## Compressors

| Name                |
|---------------------|
| LA2AComp            |
| BlueComp            |
| Compressor          |
| BassComp            |
| BBEOpticalComp      |

## Drive

| Name                |
|---------------------|
| Booster             |
| DistortionTS9       |
| Overdrive           |
| Fuzz                |
| ProCoRat            |
| BassBigMuff         |
| GuitarMuff          |
| MaestroBassmaster   |
| SABdriver           |

# Connect messages

These are the messages sent when the app connects to the Spark amp

| Direction   | Command  | Sub-command  |  Operation               | Description
|-------------|----------|--------------|--------------------------|------------------------------------
| To Spark    | 02       | 11           | Get amp name             |             
| From Spark  | 03       | 11           |                          | Byte: 08 String: Spark 40
| To Spark    | 02       | 24           |                          | Bytes: 14,0,1,2,3
| To Spark    | 02       | 23           | Get serial number        | 
| From Spark  | 03       | 23           |                          | D, String: Serial number with 'w' at end
| To Spark    | 02       | 01           | Get preset configuration | Lots of 00
| From Spark  | 03       | 01           |                          | 


