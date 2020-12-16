# Spark Commander 7

Python functions to send commands to the Spark over bluetooth

Based on the outputs of the Spark Parser which analyses the data sent to the Spark  

This works on a Windows 10 PC running Python 3.9 - using native sockets for bluetooth (which is only in Python 3.9)  
Otherwise you need ``` pip install pybluez ``` and ```import bluetooth```.

It also needs the bluetooth address of your Spark. BluettoothCL from NirSoft will find it (on Windows).

There is a version for the Raspberry Pi 400 which will also locate the Spark from its name rather than bluetooth address.  This uses PyBluez which you need to  ```pip install pybluez```   

Tested on little-endian machines only so far ```print(sys.byteorder)``` .  

Will now send a full preset to the Spark - some bugs but works for quite a few presets (just not Spooky Melody yet)

# Spark Preset Converter

Will take a preset in the format below and output the hex string and a python byte string.

```
preset = { "Filler": [0x00, 0x7f],
            "UUID": "07079063-94A9-41B1-AB1D-02CBC5D00790",
            "Name": "Silver Ship",
            "Version": "0.7",
            "Description": "1-Clean",
            "Icon": "icon.png",
            "BPM": 60.0,
            "Pedals": [ {
                "Name": "bias.noisegate",
                "OnOff": "Off",
                "Parameters": [0.137825, 0.224641, 0.000000] }, {
                "Name": "LA2AComp",
                "OnOff": "On",
                "Parameters": [0.000000, 0.852394, 0.186536] }, {
                "Name": "Booster",
                "OnOff": "Off",
                "Parameters": [0.720631] }, {
                "Name": "RolandJC120",
                "OnOff": "On",
                "Parameters": [0.630271, 0.140908, 0.158357, 0.669359, 0.805777] }, {
                "Name": "Cloner",
                "OnOff": "On",
                "Parameters": [0.199593, 0.000000] }, {
                "Name": "VintageDelay",
                "OnOff": "Off",
                "Parameters": [0.188881, 0.212384, 0.209420, 0.500000] }, {
                "Name": "bias.reverb",
                "OnOff": "On",
                "Parameters": [0.142857, 0.204175, 0.144743, 0.193668, 0.582143, 0.650000, 0.199510] }],
            "End Filler": 0x34}


01fe000053fead000000000000000000f0013a15010124030000007f59240030
37303739303600332d393441392d00343142312d41420031442d303243420043
35443030373902302b53696c7665407220536869702308302e3727312d43106c
65616e286963406f6e2e706e674a3042700000172e62006961732e6e6f694073
6567617465420d1300114a3e0d210cff01114a3e66080c4a02114a0000000200
284c41324143186f6d704313f7

01fe000053fead000000000000000000f0013a1501013403010000114a003000
000001114a3f305a367e02114a3e083f034b27426f6f30737465724211004311
4a3f387b462b00526f6c616e644a304331323043150003114a3f215971010311
4a3e104a300203114a3e2228560303114a3f2b5b1d0443114a3f4e4767264043
6c6f6e6572430d1200114a3e4c620c1b01114a00000002002c56696e74610067
6544656c61791b421400114af7

01fe000053fe81000000000000000000f0013a150101040302593e416a050601
114a3e597b310602114a3e5672320603114a3f000000012b626961732e726065
7665726243170600114a3e12491b0601114a3e5113400602114a3e1437820603
114a3e4650e70604114a3f1507530605114a3f2666660606114a3e4c4c590134
f7


b"\x01\xfe\x00\x00S\xfe\xad\x00\x00\x00\x00\x00\x00\x00\x00\x00
\xf0\x01:\x15\x01\x01$\x03\x00\x00\x00\x7fY$\x000707906\x003-94A9-
\x0041B1-AB\x001D-02CB\x00C5D0079\x020+Silve@r Ship#\x080.7'1-C
\x10lean(ic@on.pngJ0Bp\x00\x00\x17.b\x00ias.noi@segateB\r\x13\x00
\x11J>\r!\x0c\xff\x01\x11J>f\x08\x0cJ\x02\x11J\x00\x00\x00\x02
\x00(LA2AC\x18ompC\x13\xf7"

b'\x01\xfe\x00\x00S\xfe\xad\x00\x00\x00\x00\x00\x00\x00\x00\x00
\xf0\x01:\x15\x01\x014\x03\x01\x00\x00\x11J\x000\x00\x00\x00\x01
\x11J?0Z6~\x02\x11J>\x08?\x03K\'Boo0sterB\x11\x00C\x11J?8{F+
\x00RolandJ0C120C\x15\x00\x03\x11J?!Yq\x01\x03\x11J>\x10J0\x02
\x03\x11J>"(V\x03\x03\x11J?+[\x1d\x04C\x11J?NGg&@ClonerC\r\x12
\x00\x11J>Lb\x0c\x1b\x01\x11J\x00\x00\x00\x02\x00,Vinta\x00geDelay
\x1bB\x14\x00\x11J\xf7'

b'\x01\xfe\x00\x00S\xfe\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00
\xf0\x01:\x15\x01\x01\x04\x03\x02Y>Aj\x05\x06\x01\x11J>Y{1\x06
\x02\x11J>Vr2\x06\x03\x11J?\x00\x00\x00\x01+bias.r`everbC\x17
\x06\x00\x11J>\x12I\x1b\x06\x01\x11J>Q\x13@\x06\x02\x11J>\x147
\x82\x06\x03\x11J>FP\xe7\x06\x04\x11J?\x15\x07S\x06\x05\x11J?&ff
\x06\x06\x11J>LLY\x014\xf7'
```


# Spark Parser

Python code to parse the data packets sent to a Spark Amp

This uses a M5Stack Core 2 ESP32 board connected to my PC via USB.
The Core 2 appears as a Spark Amp to the Spark app on an Android tablet (over bluetooth serial)
Does not work with iOS which I presume uses BLE.

All traffic to the 'amp' is captured and sent over USB as a serial stream.

The python program reads the serial input and parses it

This is a work-in-progress to interpret the commands sent to the Spark and build a picture of how packets are constructed

I also had a version with the Core 2 as the receiver from the app, connected over wi-fi to a Pi 400 to send to the amp - but couldn't get it responsive enough (buffers on bluetooth or tcp/ip, I'm not sure). It nearly worked and captured a lot of the connection sequence, but wasn't reliable.

Now considering using two Core 2s connected either via the USB to a PC or together over a serial connection of some sort  

Latest version (1.2) seems to work completely and can handle edge cases for most presets

# Spark Hex Preset Extractor

Will read a hex string of the preset and output it like a python array/dictionary like below:

```
preset = { 
	"Filler": [0x00, 0x7f], 
	"UUID": "961F7F40-77C3-4E98-A694-DF9CA4069955",
	"Name": "Dual Train",
	"Version": "0.7",
	"Description": "Description for Rock Preset 1",
	"Icon": "icon.png",
	"BPM": 60.0,
	"Pedals": [ { 
		"Name": "bias.noisegate",
		"OnOff": "On",
		"Parameters": [0.148831, 0.000000] }, { 
		"Name": "BBEOpticalComp",
		"OnOff": "On",
		"Parameters": [0.707536, 0.524630, 0.000000] }, { 
		"Name": "DistortionTS9",
		"OnOff": "On",
		"Parameters": [0.008442, 0.184830, 0.719230] }, { 
		"Name": "Rectifier",
		"OnOff": "On",
		"Parameters": [0.704669, 0.212045, 0.224743, 0.249123, 0.793397] }, { 
		"Name": "Cloner",
		"OnOff": "Off",
		"Parameters": [0.165491, 0.000000] }, { 
		"Name": "DelayMono",
		"OnOff": "Off",
		"Parameters": [0.226571, 0.140634, 0.550847, 0.555925, 0.000000] }, { 
		"Name": "bias.reverb",
		"OnOff": "Off",
		"Parameters": [0.182966, 0.672229, 0.157315, 0.141781, 0.150772, 0.216207, 0.149510] }], 
	"End Filler": 0x46}
```

# Spark Scanner Hex

Like Spark Parser but output in hex

Based on the work of Justin Nelson https://github.com/jrnelson90/tinderboxpedal and Yuriy Tsibizov https://github.com/ytsibizov/midibox

