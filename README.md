# Spark-Parser
Python code to parse the data packets sent to a Spark Amp

This uses a M5Stack Core 2 ESP32 board connected to my PC via USB.
The Core 2 appears as a Spark Amp to the Spark app on an Android tablet (over bluetooth serial)
Does not work with iOS which I presume uses BLE.

All traffic to the 'amp' is captured and sent over USB as a serial stream.

The python program reads the serial input and parses it

This is a work-in-progress to interpret the commands sent to the Spark and build a picture of how packets are constructed

I also had a version with the Core 2 as the receiver from the app, connected over wi-fi to a Pi 400 to send to the amp - but couldn't get it responsive enough (buffers on bluetooth or tcp/ip, I'm not sure). It nearly worked and captured a lot of the connection sequence, but wasn't reliable.

Now considering using two Core 2s connected either via the USB to a PC or together over a serial connection of some sort.


Latest version (1.0) seems to work completely and can handle edge cases for most presets


Based on the work of Justin Nelson https://github.com/jrnelson90/tinderboxpedal and Yuriy Tsibizov https://github.com/ytsibizov/midibox


|

Size 173Sequence 63Sequence 2 30Command 1Parameter 1Send whole preset
Total chunks 03This chunk 00Chunk 1 of 3
Byte 00Byte 00Byte 7F
UUID 6AF9D829-CEA7-4189-AC80-B3364A563EB4


Preset name Dark Soul
Version 0.7
Description 1-Clean
Icon icon.png
Unknown value 60.00 [66, 112, 0, 0]Num pedals 17There are 7 pedals in this presetPedal bias.noisegateOn/off FalseParams 13There are 3 parameters for this pedalParam 00??? 11Value 0.06 [61, 111, 61, 8]Param 01??? 11Value 0.13 [62, 3, 94, 35]Param 02??? 11Value 0.00 [0, 0, 0, 0]
 | \x01\xfe\x00\x00S\xfe\xad\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\x017\x1e\x01\x01


$ \x03\x00


 \x00\x00\x7f


 Y$\x00 6AF9D82\x00 9-CEA7-\x00 4189-AC\x00 80-B336\x00 4A563EB\x02 4 )Dark \x10 Soul #0.\x02 7 &#39;1-Cle\x04 an (iconP .png JBp\x0c \x00\x00 \x17 .bia\x00 s.noise0 gate C \x13 \x00+ \x11 J=o=\x08 \x01\x03 \x11 J\&gt;\x03^# \x02C \x11 J\x00\x00\x00\x00 .\x00 BBEOpti\x00 calCo \xf7 | 01 FE 00 00 53 FE AD 0000 00 00 00 00 00 00 00F0 01 37 1E 01 01



24 03 00


00 00 7F


59 2400 36 41 46 39 44 38 3200 39 2D 43 45 41 37 2D00 34 31 38 39 2D 41 4300 38 30 2D 42 33 33 3600 34 41 35 36 33 45 4202 34 29 44 61 72 6B 2010 53 6F 75 6C 23 30 2E02 37 27 31 2D 43 6C 6504 61 6E 28 69 63 6F 6E50 2E 70 6E 67 4A 42 700C 00 0017 2E 62 69 6100 73 2E 6E 6F 69 73 6530 67 61 74 65 43 13 002B 114A 3D 6F 3D 08 0103 114A 3E 03 5E 23 0243 114A 00 00 00 00 2E00 42 42 45 4F 70 74 6900 63 61 6C 43 6F F7 |
| --- | --- | --- |
|



[Chunk format byte 64][Chunk 2 of 3][Chunk unknown 00]Pedal BBEOpticalCompOn/off TrueParams 13There are 3 parameters for this pedalParam 00??? 11Value 0.71 [63, 54, 115, 101]Param 01??? 11Value 0.18 [62, 61, 75, 45]Param 02??? 11Value 0.00 [0, 0, 0, 0]
Pedal Overdrive
On/off FalseParams 13There are 3 parameters for this pedalParam 00??? 11Value 0.59 [63, 22, 17, 40]Param 01??? 11Value 0.17 [62, 43, 97, 21]Param 02??? 11Value 0.13 [62, 3, 109, 28]
Pedal SLO100On/off FalseParams 15There are 5 parameters for this pedalParam 00??? 11Value 0.59 [63, 23, 69, 81]Param 01??? 11Value 0.51 [63, 3, 22, 71]Param 02??? 11Value 0.58 [63, 21, 117, 19]Param 03??? 11Value 0.14 [62, 19, 9, 48]Param 04??? 11Value 0.51 [63, 1, 118, 111]Pedal Flanger
On/off TrueParams 13There are 3 parameters for this pedalParam 00??? 11Value 0.21 [62, 83, 92, 48]Param 01??? 11Value 0.66 [63, 41, 61, 56]
Param 02??? 11
 | \x01\xfe\x00\x00S\xfe\xad\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\x017\x0f\x01\x01

d \x03\x01 \x00 mp B \x13
\x06 \x00 \x11 J?6se6 \x01 \x11 J\&gt;=K-\x06 \x02 \x11 J\x00\x00\x00\x00
\x01 )OverdrX ive C \x13
 \x00 \x11Q J?\x16\x11( \x01 \x11E J\&gt;+a\x15 \x02 \x11% J\&gt;\x03m\x1c &amp;S` LO100 C \x15
F \x00 \x11 J?\x17EQF \x01 \x11 J?\x03\x16GF \x02 \x11 J?\x15u\x13\x16 \x03 \x11 J\&gt;\x13\t0f \x04 \x11 J?\x01vo\x01 &#39;Flange6 r B \x13
 \x00 \x11 J\&gt;7S\\0 \x01 \x11 J?\x12 )=8 \x02 \x11 \xf7 | 01 FE 00 00 53 FE AD 0000 00 00 00 00 00 00 00F0 01 37 0F 01 01


64 03 01 006D 70 42 1306 00 114A 3F 36 73 6536 01 114A 3E 3D 4B 2D06 02 114A 00 00 00 0001 29 4F 76 65 72 64 7258 69 76 65 43 13
00 1151 4A 3F 16 11 28 01 1145 4A 3E 2B 61 15 02 1125 4A 3E 03 6D 1C 26 5360 4C 4F 31 30 30 43 1546 00 114A 3F 17 45 5146 01 114A 3F 03 16 4746 02 114A 3F 15 75 1316 03 114A 3E 13 09 3066 04 114A 3F 01 76 6F01 27 46 6C 61 6E 67 6536 72 42 13 00 114A 3E37 53 5C 30 01 114A 3F12 29 3D 38 02 11F7 |
|



[Chunk format byte 48][Chunk 3 of 3][Chunk unknown 74]Value 0.65 [63, 39, 57, 97]

Pedal DelayMono
On/off TrueParams 15There are 5 parameters for this pedalParam 00??? 11Value 0.22 [62, 92, 69, 114]Param 01??? 11Value 0.19 [62, 69, 15, 82]Param 02??? 11Value 0.24 [62, 117, 19, 68]Param 03??? 11Value 0.20 [62, 76, 76, 77]Param 04??? 11Value 0.50 [63, 0, 0, 0]

Pedal bias.reverb
On/off FalseParams 17There are 7 parameters for this pedalParam 00??? 11Value 0.17 [62, 46, 28, 32]Param 01??? 11Value 0.81 [63, 79, 77, 105]Param 02??? 11Value 0.15 [62, 23, 73, 6]Param 03??? 11Value 0.15 [62, 24, 68, 106]Param 04??? 11Value 0.58 [63, 21, 7, 80]Param 05??? 11Value 0.65 [63, 38, 102, 103]Param 06??? 11Value 0.20 [62, 76, 76, 77]Skipping 58 - after preset ended===== Done F7 160 159 ======= | \x01\xfe\x00\x00S\xfe\x9f\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\x017a\x01\x01
H \x03\x02
 T J?&#39;9\x02 a
 )Delay0 Mono
 B \x15 \x00# \x11 J\&gt;\\Er \x01# \x11 J\&gt;E\x0fR \x02\x0b \x11 J\&gt;u\x13D \x03; \x11 J\&gt;LLM \x04K \x11 J?\x00\x00\x00
 +\x00 bias.re0 verb C \x17
 \x00+ \x11 J\&gt;.\x1c \x01# \x11 J?Omi \x02+ \x11 J\&gt;\x17I\x06 \x03\x13 \x11 J\&gt;\x18Dj \x04\x03 \x11 J?\x15\x07P \x05\x03 \x11 J?&amp;fg \x063 \x11 J\&gt;LLM X\xf7 | 01 FE 00 00 53 FE 9F 0000 00 00 00 00 00 00 00F0 01 37 61 01 01


48 03 02
744A 3F 27 3902 61
29 44 65 6C 61 7930 4D 6F 6E 6F 42 15 0023 114A 3E 5C 45 72 0123 114A 3E 45 0F 52 020B 114A 3E 75 13 44 033B 114A 3E 4C 4C 4D 044B 114A 3F 00 00 00 2B00 62 69 61 73 2E 72 6530 76 65 72 62 43 17 002B 114A 3E 2E 1C 20 0123 114A 3F 4F 4D 69 022B 114A 3E 17 49 06 0313 114A 3E 18 44 6A 0403 114A 3F 15 07 50 0503 114A 3F 26 66 67 0633 114A 3E 4C 4C 4D 58F7 |
| Size 26Sequence 1Sequence 2 127Command 1Parameter 56

Change between presets
Integer [0, 127]===== Done F7 27 26 ======= | \x01\xfe\x00\x00S\xfe\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\x018\x7f\x018
\x00\x00\x7f\xf7 | 01 FE 00 00 53 FE 1A 0000 00 00 00 00 00 00 00F0 01 38 7F 01 38


00 00 7F F7 |
