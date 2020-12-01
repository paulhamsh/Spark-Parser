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


Based on the work of Justin Nelson https://github.com/jrnelson90/tinderboxpedal and Yuriy Tsibizov https://github.com/ytsibizov/midibox
