# Spark Commander

Python functions to send commands to the Spark over bluetooth

Based on the outputs of the Spark Parser which analyses the data sent to the Spark  

This works on a Windows 10 PC running Python 3.9 - using native sockets for bluetooth (which is only in Python 3.9)  
Otherwise you need ``` pip install pybluez ``` and ```#import bluetooth```.

It also needs the bluetooth address of your Spark. BluettoothCL from NirSoft will find it (on Windows).

There is a version for the Raspberry Pi 400 which will also locate the Spark from its name rather than bluetooth address.  This uses PyBluez which you need to  ```pip install pybluez```   

Tested on little-endian machines only so far ```print(sys.byteorder)``` .  

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

Will read a hex string of the preset and output it like a python array/dictionary like below (it looks nicer in python - it has newlines and tabs):

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

