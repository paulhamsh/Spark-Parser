# Reverse engineering the bluetooth message format used for app <-> amp communications
By ytsibizov
Additional information from paulhamsh

Messages are exhcanged in the data frame format.
When the app sends a message then the Spark responds with an acknowledgemnent

Large transfers (such as a new preset) are sent in packets of length 0xad (173 decimal)

# Data frame format

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
|     15 |      1 | Parameter                                             |
|     16 |        | Message body                                          |
|     ?? |      1 | End of message f7                                     |

## Data frame elements

Header

| Offset | 00 | 01 | 02 | 03 |
|--------|----|----|----|----|
| Data   | 01 | fe | 00 | 00 |

Direction 

| Offset | 04 | 05 | Description         |
|--------|----|----|---------------------|
| Data   | 41 | ff | Received from Spark |
| Data   | 53 | fe | Sent to Spark       |

Size of message

| Offset | 06     | Description                |
|--------|--------|----------------------------|
| Data   | length | Number of bytes in message |

Zeros

| Offset | 07 | 08 | 09 | 0A | 0B | 0C | 0D | 0E | 0F |
|--------|----|----|----|----|----|----|----|----|----|
| Data   | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 |

Fixed

| Offset | 10 | 11 |
|--------|----|----|
| Data   | f0 | 01 |

Sequence number

| Offset |  12              |  13                  |
|--------|------------------|----------------------|
| Data   |  sequence number |  sequence number (?) |

It is known (from the existing working code) that this number is never checked by the amp.

Command and parameter

| Offset |  14       |  15       |
|--------|-----------|-----------|
| Data   | command   | parameter |

This is then followed by the message body (see below)

Trailer

| Offset | xx |
|--------|----|
| Data   | f7 |



## Body structure

The body of the message made of sequences of 8 bytes - 1 format byte and then 7 bytes of data. 
Arguments are sequential in the data sequence and the format byte shows where new a new argument starts.
Each bit maps to a byte in the next sequence, and if the bit is set in the format byte then that byte in the sequence is the start of a new data element.
Strings have their length as their first byte (stored as 0x20 + length).

An example is shown below, with each new data sequence on a new line. The bit expansion is the format byte with the bits reversed, to show where the new sequence starts:

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

Which translates to:
     String: Royal Crown
     String: 0.7
     String: 1-Clean
     String: icon.png
     ???: 4a 42
     ???: 70 00 00
     ???: 17
     String: .bias.noisegate

It appears that strings are the only variable length data sequence and the only sequence that starts with a length

### Argument types

| Value      | Length   | Type                             |
|------------|----------|----------------------------------|
| 00    ??   |        2 | Integer number, big endian       |
| 20 - 3f    | variable | String of length argument - 0x20 |
| 42         |        1 | Boolean "True"                   |
| 43         |        1 | Boolean "False"                  |
| 4a         |        4 | Float                            | 


## Command types

| Value | Operation  |
|-------|------------|
|  00   | Info       |
|  01   | Set        |
|  02   | Get        | 
|  03   | Response ??|
|  04   | Ack        |
|  f0   | Sequence ??| 


## INFO Operation

The only known operation is 

02 23  - Get hardware ID


## SET operation

Following SET operations are known:

| Parameter | Description            | Arguments
|-----------|------------------------|-----------------------------------------------------------
| 01        | Send preset            | *UUID*, preset name, version, description, *float*, *byte*, noisegate name, boolean, ?,?, float, 
| 02        | Change value  ??       | ??
| 04        | Change knob            | String: pedal name, Byte: knob reference, Float: new value
| 06        | Change pedal           | String: old pedal name, String: new pedal name
| 15        | Enable/disable a pedal | String: pedal name, Boolean: on/off
| 38        | Change to preset       | Int: preset number (0 - 3)

### 01 Send preset

A new present is a multi-packet message.

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  Byte    |      1 |  Number of packets ?                                  |
|  Byte    |      1 |                                                       |
|  Byte    |      1 |                                                       |
|  Byte    |      1 |                                                       |
|  Byte    |      1 |                                                       |
|  UUID    |     36 | UUID for preset                                       |
|  String  |      x | Preset name                                           |
|  String  |      x | Version                                               |
|  String  |      x | Preset description                                    |
|  String  |      x | Icon name ??                                          |
|  Float   |      4 |                                                       |
|  Byte    |      1 |                                                       |

Followed by information for each pedal / amp:

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  String  |      x | Pedal name                                            |
|  Boolean |      1 | On/off                                                |
|  Byte    |      1 | Number of values (+0x10)                              |

Each pedal header is followed by data for each know / switch:

| Type     | Length | Content                                               |
|----------|--------|-------------------------------------------------------|
|  Byte    |      1 | Value reference (starts at 0)                         |
|  Byte    |      1 | 11???                                                 |
|  Float   |      4 | Value to set                                          |
|          |        |                                                       |
|  Byte    |      1 | Value reference (starts at 0)                         |
|  Byte    |      1 | 11???                                                 |
|  Float   |      4 | Value to set                                          |
 
### 04 Change knob

Arguments are a string for the pedal name, a byte for which know is being altered (starting at 0) and a float for the new value.

### 15 Enable/disable a pedal

   There is no consensus on what "True" value means, for different positions (maybe even pedals?) it is different.

   | Position       | Active     | Disabled   |
   |----------------|------------|------------|
   | 0 (noise gate) | 42 (True)  | 43 (False) |
   | 1 (compressor) | 42 (True)  | 43 (False) |
   | 2 (distortion) | 43 (False) | 42 (True)  |
   | 3 (amp)        | -          | -          |
   | 4 (chorus)     | 43 (False) | 42 (True)  |
   | 5 (delay)      | 43 (False) | 42 (True)  |

### 38 Change preset

Only argument is an integer for which preset to select (0-3)

## GET Operations

Following GET operations are known:

| Parameter |                       |
|-----------|-----------------------|
|  01       | Get preset configuration
|  02       |
|  11       | Get device name

### 01 Get preset configuration

Multiple arguments, only first one is actually used

 - Integer number - Preset number starting 0, or 0x0100 for "current"
 - 34x "0x00" (that is 11x "Integer number, value 0" + 0x00)

## "ACK" packets

After a successful operation, amp sends back an "ack" packet.
This has the command 0x04, the same sequence number as the original packet and a parameter the same as the parameter sent to the Spark

## Pedal names

## Compressors

|---------------------|
| LA2AComp            |
| BlueComp            |
| Compressor          |
| BassComp            |
| BBEOpticalComp      |

## Drive

|---------------------|
| Booster             |
| DistortionTS9       |
| Overdrive           |
| Fuzz                |
| ProCoRat            |
| BassBigMuff         |
| GuitarMuff          |
| MaestroBassmaster   |

SABdriver
