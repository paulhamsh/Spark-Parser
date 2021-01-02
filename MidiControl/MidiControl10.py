import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.midi
import time
from   SparkClass import *
from   SparkReaderClass import *
from   SparkCommsClass import *

from   sys import platform

print()
if platform == "win32":
    #for Windows
    import socket
    midi_device_name = b'Launchkey MIDI'
    print ("Midi Control on Windows")
else:
    #for Raspberry Pi
    import bluetooth
    midi_device_name = b'Launchkey MK2 25 MIDI 1'
    print ("Midi Control on Raspberry Pi or Linux")

 
# Change to address of YOUR Spark or leave as "" to search for a Spark
my_spark = "08:EB:ED:4E:47:07"  


#
# Spark presets and options
#

spark_noisegates =  ["bias.noisegate"]
spark_compressors = ["LA2AComp","BlueComp","Compressor","BassComp","BBEOpticalComp"]
spark_drives =      ["Booster","DistortionTS9","Overdrive","Fuzz","ProCoRat","BassBigMuff",
                     "GuitarMuff","MaestroBassmaster","SABdriver"]
spark_amps=         ["RolandJC120","Twin","ADClean","94MatchDCV2","Bassman","AC Boost","Checkmate",
                     "TwoStoneSP50","Deluxe65","Plexi","OverDrivenJM45","OverDrivenLuxVerb",
                     "Bogner","OrangeAD30","AmericanHighGain","SLO100","YJM100","Rectifier",
                     "EVH","SwitchAxeLead","Invader","BE101","Acoustic","AcousticAmpV2","FatAcousticV2",
                     "FlatAcoustic","GK800","Sunny3000","W600","Hammer500"]
spark_modulations = ["Tremolo","ChorusAnalog","Flanger","Phaser","Vibrato01","UniVibe",
                     "Cloner","MiniVibe","Tremolator","TremoloSquare"]
spark_delays =      ["DelayMono","DelayEchoFilt","VintageDelay","DelayReverse",
                     "DelayMultiHead","DelayRe201"]
spark_reverbs =     ["bias.reverb"]

spark_effects =     {"Noisegate":   spark_noisegates, 
                     "Compressor":  spark_compressors,
                     "Drive":       spark_drives,
                     "Amp":         spark_amps, 
                     "Mod":         spark_modulations, 
                     "Delay":       spark_delays, 
                     "Reverb":      spark_reverbs}

preset1  = { "PresetNumber": [0x00, 0x7f], "UUID": "07079063-94A9-41B1-AB1D-02CBC5D00790","Name": "Silver Ship","Version": "0.7","Description": "1-Clean","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "Off","Parameters": [0.138313, 0.224643, 0.000000] }, { "Name": "LA2AComp","OnOff": "On","Parameters": [0.000000, 0.852394, 0.373072] }, { "Name": "Booster","OnOff": "Off","Parameters": [0.722592] }, { "Name": "RolandJC120","OnOff": "On","Parameters": [0.632231, 0.281820, 0.158359, 0.671320, 0.805785] }, { "Name": "Cloner","OnOff": "On","Parameters": [0.199593, 0.000000] }, { "Name": "VintageDelay","OnOff": "Off","Parameters": [0.378739, 0.425745, 0.419816, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.285714, 0.408354, 0.289489, 0.388317, 0.582143, 0.650000, 0.200000] }], "End Filler": 0xb4}
preset2  = { "PresetNumber": [0x00, 0x7f], "UUID": "CDE99591-C05D-4AE0-9E34-EC4A81F3F84F","Name": "Sweet Memory","Version": "0.7","Description": "1-Clean","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "Off","Parameters": [0.099251, 0.570997, 0.000000] }, { "Name": "BlueComp","OnOff": "Off","Parameters": [0.430518, 0.663291, 0.355048, 0.557014] }, { "Name": "DistortionTS9","OnOff": "Off","Parameters": [0.058011, 0.741722, 0.595924] }, { "Name": "94MatchDCV2","OnOff": "On","Parameters": [0.528926, 0.500905, 0.246163, 0.417119, 0.782293] }, { "Name": "Flanger","OnOff": "Off","Parameters": [0.413793, 0.663043, 0.655172] }, { "Name": "DelayRe201","OnOff": "On","Parameters": [0.097778, 0.312182, 0.485182, 0.369640, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.561185, 0.506659, 0.417857, 0.300847, 0.602287, 0.594118, 0.000000] }], "End Filler": 0xeb}
preset3  = { "PresetNumber": [0x00, 0x7f], "UUID": "F577F7F3-E8E0-4D35-8975-0427C2054DCE","Name": "Dancing in the room","Version": "0.7","Description": "Description for Blues Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "Off","Parameters": [0.283019, 0.304245] }, { "Name": "Compressor","OnOff": "On","Parameters": [0.325460, 0.789062] }, { "Name": "Booster","OnOff": "Off","Parameters": [0.666735] }, { "Name": "Twin","OnOff": "On","Parameters": [0.613433, 0.371715, 0.453167, 0.676660, 0.805785] }, { "Name": "ChorusAnalog","OnOff": "On","Parameters": [0.185431, 0.086409, 0.485027, 0.567797] }, { "Name": "DelayEchoFilt","OnOff": "Off","Parameters": [0.533909, 0.275554, 0.455372, 0.457702, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.508871, 0.317935, 0.461957, 0.349689, 0.339286, 0.481753, 0.700000] }], "End Filler": 0x48}
preset4  = { "PresetNumber": [0x00, 0x7f], "UUID": "D8757D67-98EA-4888-86E5-5F1FD96A30C3","Name": "Royal Crown","Version": "0.7","Description": "1-Clean","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.211230, 0.570997, 0.000000] }, { "Name": "Compressor","OnOff": "On","Parameters": [0.172004, 0.538197] }, { "Name": "DistortionTS9","OnOff": "Off","Parameters": [0.703110, 0.278146, 0.689846] }, { "Name": "ADClean","OnOff": "On","Parameters": [0.677083, 0.501099, 0.382828, 0.585946, 0.812231] }, { "Name": "ChorusAnalog","OnOff": "On","Parameters": [0.519976, 0.402152, 0.240642, 0.740579] }, { "Name": "DelayMono","OnOff": "On","Parameters": [0.173729, 0.233051, 0.493579, 0.600000, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.688801, 0.392857, 0.461138, 0.693705, 0.488235, 0.466387, 0.300000] }], "End Filler": 0xa2}
preset5  = { "PresetNumber": [0x00, 0x7f], "UUID": "9D2F2AA3-4EC5-4BD7-A3CD-A76FD55698DB","Name": "Wooden Bridge","Version": "0.7","Description": "Description for Blues Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.316873, 0.304245] }, { "Name": "Compressor","OnOff": "Off","Parameters": [0.341085, 0.665754] }, { "Name": "Booster","OnOff": "On","Parameters": [0.661412] }, { "Name": "Bassman","OnOff": "On","Parameters": [0.768152, 0.491509, 0.476547, 0.284314, 0.389779] }, { "Name": "UniVibe","OnOff": "Off","Parameters": [0.500000, 1.000000, 0.700000] }, { "Name": "VintageDelay","OnOff": "On","Parameters": [0.152219, 0.663314, 0.144982, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.120109, 0.150000, 0.500000, 0.406755, 0.299253, 0.768478, 0.100000] }], "End Filler": 0x12}
preset6  = { "PresetNumber": [0x00, 0x7f], "UUID": "B08F2421-0686-484E-B6EC-8F660A9344FC","Name": "Stone Breaker","Version": "0.7","Description": "Description for Blues Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.105936, 0.231329] }, { "Name": "Compressor","OnOff": "On","Parameters": [0.341085, 0.665754] }, { "Name": "DistortionTS9","OnOff": "Off","Parameters": [0.117948, 0.390437, 0.583560] }, { "Name": "TwoStoneSP50","OnOff": "On","Parameters": [0.634593, 0.507692, 0.664699, 0.519608, 0.714050] }, { "Name": "Tremolator","OnOff": "Off","Parameters": [0.330000, 0.500000, 1.000000] }, { "Name": "DelayRe201","OnOff": "On","Parameters": [0.324783, 0.204820, 0.460643, 0.304200, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.554974, 0.842373, 0.783898, 0.385087, 0.659664, 0.294118, 0.000000] }], "End Filler": 0x59}
preset7  = { "PresetNumber": [0x00, 0x7f], "UUID": "55D60EB5-1735-4746-B0C4-16C53D8CA203","Name": "Country road","Version": "0.7","Description": "Description for Blues Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.283019, 0.304245] }, { "Name": "Compressor","OnOff": "Off","Parameters": [0.461066, 0.608902] }, { "Name": "DistortionTS9","OnOff": "On","Parameters": [0.200747, 0.216084, 0.583560] }, { "Name": "AC Boost","OnOff": "On","Parameters": [0.707792, 0.591124, 0.383605, 0.532821, 0.195119] }, { "Name": "Tremolo","OnOff": "Off","Parameters": [0.454134, 0.699934, 0.596154] }, { "Name": "DelayRe201","OnOff": "Off","Parameters": [0.331450, 0.348991, 0.672299, 0.453144, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.622826, 0.150000, 0.500000, 0.621429, 0.369905, 0.350000, 0.100000] }], "End Filler": 0x57}
preset8  = { "PresetNumber": [0x00, 0x7f], "UUID": "2E2928B5-D87E-4346-B58F-145B88C581BE","Name": "Blues Ark","Version": "0.7","Description": "1-Clean","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.127897, 0.313185, 0.000000] }, { "Name": "LA2AComp","OnOff": "On","Parameters": [0.000000, 0.832474, 0.304124] }, { "Name": "DistortionTS9","OnOff": "On","Parameters": [0.570513, 0.549669, 0.706421] }, { "Name": "Twin","OnOff": "On","Parameters": [0.679549, 0.371715, 0.593663, 0.676660, 0.479191] }, { "Name": "ChorusAnalog","OnOff": "Off","Parameters": [0.377119, 0.310128, 0.510580, 0.455357] }, { "Name": "DelayMono","OnOff": "On","Parameters": [0.173729, 0.239186, 0.521186, 0.606780, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.325512, 0.392857, 0.461138, 0.100520, 0.488235, 0.466387, 0.300000] }], "End Filler": 0xa3}
preset9 =  { "PresetNumber": [0x00, 0x7f], "UUID": "BB40E550-77D0-40B1-B0D3-D15D3D0C19EE","Name": "Modern Stone","Version": "0.7","Description": "Description for Rock Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.271226, 0.370283] }, { "Name": "BlueComp","OnOff": "On","Parameters": [0.389830, 0.665254, 0.305085, 0.644068] }, { "Name": "Overdrive","OnOff": "Off","Parameters": [0.586207, 0.500288, 0.530172] }, { "Name": "AmericanHighGain","OnOff": "On","Parameters": [0.616274, 0.431090, 0.419846, 0.495112, 0.850637] }, { "Name": "ChorusAnalog","OnOff": "Off","Parameters": [0.120593, 0.279661, 0.185763, 0.485297] }, { "Name": "DelayMono","OnOff": "Off","Parameters": [0.271017, 0.190613, 0.355976, 0.555932, 0.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.175725, 0.680389, 0.761837, 0.177584, 0.302521, 0.408933, 0.300000] }], "End Filler": 0xe6}
preset10 = { "PresetNumber": [0x00, 0x7f], "UUID": "BFCFC107-6E80-4F26-8549-F44638856241","Name": "Crazy Crue","Version": "0.7","Description": "1-Clean","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.104459, 0.232455, 0.000000] }, { "Name": "Compressor","OnOff": "Off","Parameters": [0.683015, 0.327260] }, { "Name": "DistortionTS9","OnOff": "On","Parameters": [0.355043, 0.314570, 0.554487] }, { "Name": "YJM100","OnOff": "On","Parameters": [0.562574, 0.485294, 0.317001, 0.250528, 0.576942] }, { "Name": "ChorusAnalog","OnOff": "Off","Parameters": [0.127396, 0.172299, 0.745763, 0.750884] }, { "Name": "DelayRe201","OnOff": "On","Parameters": [0.071111, 0.223224, 0.285796, 0.537533, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.147366, 0.506659, 0.417857, 0.268239, 0.602287, 0.594118, 0.000000] }], "End Filler": 0xcc}
preset11 = { "PresetNumber": [0x00, 0x7f], "UUID": "6AF9D829-CEA7-4189-AC80-B3364A563EB4","Name": "Dark Soul","Version": "0.7","Description": "1-Clean","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.116817, 0.128289, 0.000000] }, { "Name": "BBEOpticalComp","OnOff": "Off","Parameters": [0.712698, 0.370691, 0.000000] }, { "Name": "Overdrive","OnOff": "On","Parameters": [0.586207, 0.334725, 0.256692] }, { "Name": "SLO100","OnOff": "On","Parameters": [0.590909, 0.512066, 0.583825, 0.287179, 0.507674] }, { "Name": "Flanger","OnOff": "Off","Parameters": [0.413793, 0.663043, 0.655172] }, { "Name": "DelayMono","OnOff": "Off","Parameters": [0.215111, 0.192443, 0.478663, 0.400000, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.340062, 0.809783, 0.295483, 0.149187, 0.582143, 0.650000, 0.200000] }], "End Filler": 0x58}
preset12 = { "PresetNumber": [0x00, 0x7f], "UUID": "7984DF4F-5885-4FE2-9786-F3F31E322E44","Name": "British Accent","Version": "0.7","Description": "Description for Pop Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.095322, 0.242286] }, { "Name": "Compressor","OnOff": "Off","Parameters": [0.499939, 0.337629] }, { "Name": "Booster","OnOff": "On","Parameters": [0.602726] }, { "Name": "OrangeAD30","OnOff": "On","Parameters": [0.620474, 0.312894, 0.484227, 0.527442, 0.492836] }, { "Name": "Cloner","OnOff": "Off","Parameters": [0.500000, 0.000000] }, { "Name": "DelayRe201","OnOff": "Off","Parameters": [0.224783, 0.324451, 0.153894, 0.488644, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.205106, 0.721662, 0.656790, 0.193705, 0.488235, 0.466387, 0.300000] }], "End Filler": 0xca}
preset13 = { "PresetNumber": [0x00, 0x7f], "UUID": "96E26248-0AA3-4D45-B767-8BB9337346C9","Name": "Iron Hammer","Version": "0.7","Description": "Description for Metal Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.217472, 0.000000] }, { "Name": "Compressor","OnOff": "On","Parameters": [0.547004, 0.647572] }, { "Name": "DistortionTS9","OnOff": "Off","Parameters": [0.147861, 0.400662, 0.640123] }, { "Name": "SwitchAxeLead","OnOff": "On","Parameters": [0.572609, 0.352941, 0.374004, 0.460784, 0.705431] }, { "Name": "UniVibe","OnOff": "Off","Parameters": [0.500000, 1.000000, 0.700000] }, { "Name": "DelayRe201","OnOff": "Off","Parameters": [0.207006, 0.281507, 0.411563, 0.461977, 1.000000] }, { "Name": "bias.reverb","OnOff": "Off","Parameters": [0.103649, 0.720854, 0.531337, 0.189948, 0.631056, 0.380978, 0.200000] }], "End Filler": 0x49}
preset14 = { "PresetNumber": [0x00, 0x7f], "UUID": "82C5B8E8-7889-4302-AC19-74DF543872E1","Name": "Millenial Lead","Version": "0.7","Description": "Description for Metal Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.209660, 0.064809] }, { "Name": "BlueComp","OnOff": "Off","Parameters": [0.392063, 0.665254, 0.452324, 0.597193] }, { "Name": "DistortionTS9","OnOff": "On","Parameters": [0.046116, 0.357616, 0.769957] }, { "Name": "BE101","OnOff": "On","Parameters": [0.587958, 0.343137, 0.475797, 0.394193, 0.875443] }, { "Name": "ChorusAnalog","OnOff": "Off","Parameters": [0.761324, 0.132422, 0.491161, 0.567797] }, { "Name": "DelayMono","OnOff": "On","Parameters": [0.161777, 0.180514, 0.500135, 0.600000, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.095109, 0.660326, 0.692935, 0.285326, 0.500000, 0.500000, 0.300000] }], "End Filler": 0x01}
preset15 = { "PresetNumber": [0x00, 0x7f], "UUID": "5F27120E-5119-4923-ADA9-42CCB5B01A95","Name": "Heavy Axe","Version": "0.7","Description": "Description for Metal Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.108097, 0.051788] }, { "Name": "BBEOpticalComp","OnOff": "Off","Parameters": [0.712698, 0.441540, 0.000000] }, { "Name": "DistortionTS9","OnOff": "On","Parameters": [0.080701, 0.298013, 0.554487] }, { "Name": "EVH","OnOff": "On","Parameters": [0.599518, 0.467647, 0.407468, 0.357744, 0.820512] }, { "Name": "Phaser","OnOff": "Off","Parameters": [0.331250, 0.620000] }, { "Name": "DelayMono","OnOff": "Off","Parameters": [0.228444, 0.180514, 0.463325, 0.400000, 1.000000] }, { "Name": "bias.reverb","OnOff": "Off","Parameters": [0.285714, 0.709984, 0.582967, 0.388317, 0.582143, 0.650000, 0.200000] }], "End Filler": 0xe4}
preset16 = { "PresetNumber": [0x00, 0x7f], "UUID": "961F7F40-77C3-4E98-A694-DF9CA4069955","Name": "Dual Train","Version": "0.7","Description": "Description for Rock Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.148831, 0.000000] }, { "Name": "BBEOpticalComp","OnOff": "On","Parameters": [0.707544, 0.526591, 0.000000] }, { "Name": "DistortionTS9","OnOff": "On","Parameters": [0.016884, 0.370637, 0.719230] }, { "Name": "Rectifier","OnOff": "On","Parameters": [0.706630, 0.425070, 0.450462, 0.498249, 0.795350] }, { "Name": "Cloner","OnOff": "Off","Parameters": [0.330986, 0.000000] }, { "Name": "DelayMono","OnOff": "Off","Parameters": [0.226572, 0.140636, 0.550847, 0.555932, 0.000000] }, { "Name": "bias.reverb","OnOff": "Off","Parameters": [0.366912, 0.672237, 0.314634, 0.284543, 0.302521, 0.433390, 0.300000] }], "End Filler": 0xc6}
preset17 = { "PresetNumber": [0x00, 0x7f], "UUID": "94109418-E7D9-4B99-83F7-DDB11CA5847D","Name": "Spooky Melody","Version": "0.7","Description": "Description for Alternative Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.500000, 1.000000] }, { "Name": "Compressor","OnOff": "On","Parameters": [0.351691, 0.354167] }, { "Name": "DistortionTS9","OnOff": "Off","Parameters": [0.272170, 0.642384, 0.595924] }, { "Name": "Twin","OnOff": "On","Parameters": [0.613433, 0.489362, 0.453167, 0.505091, 0.580000] }, { "Name": "UniVibe","OnOff": "On","Parameters": [0.636598, 0.000000, 0.493814] }, { "Name": "DelayEchoFilt","OnOff": "On","Parameters": [0.231858, 0.555041, 0.529055, 0.308814, 0.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.963044, 0.232082, 0.176398, 0.224767, 0.228167, 0.357143, 0.500000] }], "End Filler": 0x19}
preset18 = { "PresetNumber": [0x00, 0x7f], "UUID": "E237C4CF-172B-4D68-AA5B-659F57715658","Name": "Fuzzy Jam","Version": "0.7","Description": "Description for Alternative Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.500000, 1.000000] }, { "Name": "Compressor","OnOff": "On","Parameters": [0.435025, 0.647572] }, { "Name": "Fuzz","OnOff": "On","Parameters": [0.436505, 1.000000] }, { "Name": "ADClean","OnOff": "On","Parameters": [0.677083, 0.364470, 0.353902, 0.341186, 0.680000] }, { "Name": "UniVibe","OnOff": "Off","Parameters": [0.500000, 1.000000, 0.700000] }, { "Name": "VintageDelay","OnOff": "Off","Parameters": [0.293103, 0.646739, 0.284055, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.493323, 0.293282, 0.520823, 0.398143, 0.469538, 0.455462, 0.600000] }], "End Filler": 0x13}
preset19 = { "PresetNumber": [0x00, 0x7f], "UUID": "A3601E1D-8018-42A8-9A19-9B6F0DAB6F46","Name": "Angry Monkey","Version": "0.7","Description": "Description for Alternative Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.500000, 1.000000] }, { "Name": "BlueComp","OnOff": "On","Parameters": [0.389830, 0.665254, 0.305085, 0.644068] }, { "Name": "GuitarMuff","OnOff": "On","Parameters": [0.619421, 0.692053, 0.805691] }, { "Name": "94MatchDCV2","OnOff": "On","Parameters": [0.512397, 0.557982, 0.415584, 0.438462, 0.351240] }, { "Name": "Flanger","OnOff": "On","Parameters": [1.000000, 0.338540, 0.245856] }, { "Name": "DelayMono","OnOff": "On","Parameters": [0.096667, 0.101227, 0.395705, 0.320000, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.554341, 0.308929, 0.237733, 0.738432, 0.265140, 0.276786, 0.400000] }], "End Filler": 0xe3}
preset20 = { "PresetNumber": [0x00, 0x7f], "UUID": "50A3B945-1A86-4E06-B10B-550E3226DDF2","Name": "Hide and Seek","Version": "0.7","Description": "Description for Alternative Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.500000, 1.000000] }, { "Name": "BlueComp","OnOff": "Off","Parameters": [0.590723, 0.665254, 0.305085, 0.644068] }, { "Name": "Booster","OnOff": "On","Parameters": [0.668454] }, { "Name": "Bogner","OnOff": "On","Parameters": [0.655844, 0.626593, 0.640734, 0.351588, 0.338571] }, { "Name": "MiniVibe","OnOff": "Off","Parameters": [0.047057, 0.117188] }, { "Name": "DelayMultiHead","OnOff": "On","Parameters": [0.706667, 0.644172, 0.564417, 0.650000, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.448518, 0.405932, 0.566185, 0.648674, 0.302521, 0.180672, 0.300000] }], "End Filler": 0x45}
preset21 = { "PresetNumber": [0x00, 0x7f], "UUID": "3013444B-9929-499F-964D-707E9D8F5FA0","Name": "Bass Driver","Version": "0.7","Description": "Description for Bass Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.419271, 0.226562] }, { "Name": "BassComp","OnOff": "On","Parameters": [0.372727, 0.530303] }, { "Name": "SABdriver","OnOff": "On","Parameters": [0.535256, 1.000000, 0.724359, 1.000000] }, { "Name": "W600","OnOff": "On","Parameters": [0.664699, 0.423077, 0.276884, 0.415083, 0.448052] }, { "Name": "UniVibe","OnOff": "Off","Parameters": [0.500000, 1.000000, 0.700000] }, { "Name": "VintageDelay","OnOff": "Off","Parameters": [0.359402, 0.400883, 0.350280, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.253261, 0.462500, 0.234401, 0.137733, 0.293818, 0.638043, 0.100000] }], "End Filler": 0x91}
preset22 = { "PresetNumber": [0x00, 0x7f], "UUID": "D99DC07A-C997-4ABD-833A-0C13EA8BEE5A","Name": "Comped Cleaner","Version": "0.7","Description": "Description for Bass Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.205729, 0.226562] }, { "Name": "BassComp","OnOff": "On","Parameters": [0.193040, 0.334991] }, { "Name": "MaestroBassmaster","OnOff": "Off","Parameters": [0.698052, 0.276184, 0.566086] }, { "Name": "GK800","OnOff": "On","Parameters": [0.688351, 0.407152, 0.399197, 0.746875, 0.774234] }, { "Name": "Cloner","OnOff": "Off","Parameters": [0.248888, 0.000000] }, { "Name": "DelayMono","OnOff": "Off","Parameters": [0.163333, 0.214724, 0.355828, 0.320000, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.168478, 0.744565, 0.130435, 0.288043, 0.323370, 0.293478, 0.600000] }], "End Filler": 0x54}
preset23 = { "PresetNumber": [0x00, 0x7f], "UUID": "57AF2690-F7C8-4766-9A92-F3A51629B959","Name": "Cozy Serenade","Version": "0.7","Description": "Description for Acoustic Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "On","Parameters": [0.143229, 0.000000] }, { "Name": "BlueComp","OnOff": "On","Parameters": [0.506411, 0.356543, 0.348913, 0.407461] }, { "Name": "Booster","OnOff": "Off","Parameters": [0.567515] }, { "Name": "FatAcousticV2","OnOff": "On","Parameters": [0.453955, 0.292760, 0.565172, 0.575339, 0.829431] }, { "Name": "ChorusAnalog","OnOff": "Off","Parameters": [0.761324, 0.236716, 0.745763, 0.431636] }, { "Name": "DelayMono","OnOff": "Off","Parameters": [0.187778, 0.211656, 0.334356, 0.400000, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.315883, 0.652174, 0.111413, 0.357842, 0.339286, 0.489905, 0.700000] }], "End Filler": 0x2f}
preset24 = { "PresetNumber": [0x00, 0x7f], "UUID": "DEFBB271-B3EE-4C7E-A623-2E5CA53B6DDA","Name": "Studio Session","Version": "0.7","Description": "Description for Acoustic Preset 1","Icon": "icon.png","BPM": 120.0,"Pedals": [ { "Name": "bias.noisegate","OnOff": "Off","Parameters": [0.500000, 0.346698] }, { "Name": "BBEOpticalComp","OnOff": "On","Parameters": [0.758266, 0.258550, 0.000000] }, { "Name": "DistortionTS9","OnOff": "Off","Parameters": [0.139574, 0.407285, 0.689846] }, { "Name": "Acoustic","OnOff": "On","Parameters": [0.639823, 0.385056, 0.383449, 0.599397, 0.519480] }, { "Name": "ChorusAnalog","OnOff": "On","Parameters": [0.841681, 0.227514, 0.935947, 0.351279] }, { "Name": "DelayMono","OnOff": "Off","Parameters": [0.223999, 0.211189, 0.490933, 0.600000, 1.000000] }, { "Name": "bias.reverb","OnOff": "On","Parameters": [0.722819, 0.326169, 0.275776, 0.360714, 0.343944, 0.486025, 0.400000] }], "End Filler": 0x23}


spark_presets = {"Silver Ship":         preset1,
                 "Sweet Memory":        preset2,
                 "Dancing in the room": preset3,
                 "Royal Crown":         preset4,
                 "Spooky Melody":       preset17,
                 "Fuzzy Jam":           preset18}


effects_current = {"Noisegate": "bias.noisegate", 
                   "Compressor": "LA2AComp",
                   "Drive": "Booster",
                   "Amp": "RolandJC120", 
                   "Mod": "Cloner", 
                   "Delay": "Vintage Delay", 
                   "Reverb": "bias.reverb"}

# check midi command table

def validate_map(map):
    err = 0
    for a_cmd in map:

        cmd = map[a_cmd][0]


        # test all the commands are ok
        if cmd not in ["HardwarePreset","ChangeParam","ChangeEffect","EffectOnOff","ChangePreset"]:
            print (">>> %s is not a valid command to Spark" % cmd)
            err += 1
        
        # check the effect types (not needed for HardwarePreset)
        if cmd in ["ChangeParam","ChangeEffect","EffectOnOff"]:
            eff_type = map[a_cmd][1]
            eff_name = map[a_cmd][2]
            if eff_type not in effects_current:
                print (">>> %s is not a valid effect" % eff_type)
                err += 1
            else:
                if cmd in ["ChangeEffect"]:
                    if eff_name not in spark_effects[eff_type]:
                        print (">>> %s is not a valid effect name" % eff_name)
                        err += 1
        if cmd == "ChangePreset":
            pres = map[a_cmd][1]
            if pres not in spark_presets:
                print (">>> %s is not a valid preset" % pres)
    return err  

    
# Spark communications functions

def send_receive(b):
    comms.send_it(b)
#    a=comms.read_it(100)
    a=comms.get_data()
    
def send_preset(pres):
    for i in pres:
        comms.send_it(i)
        #a=comms.read_it(100)
        a=comms.get_data()
    
    comms.send_it(change_user_preset[0])
    a= comms.get_data()
    #a=comms.read_it(100)
    
def just_send(b):
    comms.send_it(b)

#
# Connect to the Spark
#

print ()
print ("BLUETOOTH TO SPARK")
print ("==================")
print ("Trying to connect to Spark")

#comms = SparkComms("bt_socket")
# below for Raspberry Pi
#comms = SparkComms("bluetooth")
comms = SparkComms("bt_socket")
comms.connect(my_spark)

# for later
reader = SparkReadMessage()

print("Sending Silver Ship preset")
msg = SparkMessage()
change_user_preset = msg.change_hardware_preset(0x7f)
b = msg.create_preset(spark_presets["Silver Ship"])
send_preset(b)

#
# Find the Midi device
#

print ()
print ("SETTING UP MIDI")
print ("===============")
print ("Starting midi")
pygame.midi.init()    

# list all midi devices
i=-1
for x in range( 0, pygame.midi.get_count() ):
    inf = pygame.midi.get_device_info(x)
    # Looking specifically for the Novation Launchkey device here
    if inf[1]== midi_device_name and inf[2] == 1:
        i = x
 
# open a specific midi device
if i>0:
    inp = pygame.midi.Input(i)
    print ("Found Launchkey")
else:
    print ("Could not find Launchkey midi device")
    quit()
    
# Start the main routine
    
    

midi_map = {"NoteOn-40":    ["HardwarePreset", 0],
            "NoteOn-41":    ["HardwarePreset", 1],
            "NoteOn-42":    ["HardwarePreset", 2],
            "NoteOn-43":    ["HardwarePreset", 3],

            "NoteOn-48":    ["ChangeEffect", "Amp", "RolandJC120"],
            "NoteOn-49":    ["ChangeEffect", "Amp", "Twin"],
            "NoteOn-50":    ["ChangeEffect", "Amp", "AC Boost"],
            "NoteOn-51":    ["ChangeEffect", "Amp", "OrangeAD30"],
            
            "CC-21":        ["ChangeParam", "Amp", 0],       # Gain
            "CC-22":        ["ChangeParam", "Amp", 3],       # Bass
            "CC-23":        ["ChangeParam", "Amp", 2],       # Mid
            "CC-24":        ["ChangeParam", "Amp", 1],       # Treble
            "CC-25":        ["ChangeParam", "Amp", 4],       # Master
            "CC-26":        ["ChangeParam", "Mod", 0],       # Mod
            "CC-27":        ["ChangeParam", "Delay", 0],     # Delay
            "CC-28":        ["ChangeParam", "Reverb", 0],    # Reverb

            "NoteOn-36":    ["EffectOnOff", "Drive", "On"],
            "NoteOn-37":    ["EffectOnOff", "Drive", "Off"],
            "NoteOn-38":    ["EffectOnOff", "Delay", "On"],
            "NoteOn-39":    ["EffectOnOff", "Delay", "Off"],

            "NoteOn-44":    ["ChangePreset","Silver Ship"],
            "NoteOn-45":    ["ChangePreset","Sweet Memory"],
            "NoteOn-46":    ["ChangePreset","Spooky Melody"],
            "NoteOn-47":    ["ChangePreset","Fuzzy Jam"]
            }
 
commands = { 0x80: "NoteOff",
             0x90: "NoteOn",
             0xB0: "CC",
             0xC0: "PgmChg" }
             

# check the commands for basic validity

print ()
print ("Checking the midi command table")

errors = validate_map(midi_map)
if errors > 0:
    print ("Need to fix the midi command table quitting")
    quit()

# run the event loop

print()
print ("RUNNING THE COMMANDER")
print ("=====================")

while True:
    if inp.poll():

        midi_in =inp.read(1000)
        for midi_data in midi_in:
            mi = midi_data[0]
            m_cmd = (mi[0] & 0xf0)
            m_val = mi[1]
            m_param = 0
            
            if m_cmd in commands:
                m_str = commands[m_cmd] + "-%d" % m_val
            else:
                m_str = ""
                
            m_param_val= mi[2] / 127

            if m_str in midi_map.keys():
                s_cmd = midi_map [m_str]
            else:
                s_cmd = ["None"]
                print ("Unknown midi command %s" % m_str)

            this_cmd = s_cmd[0]
            if this_cmd == "HardwarePreset":
                hw_preset = s_cmd[1]
                print("Change to hw preset %d" % hw_preset)
                b=msg.change_hardware_preset(hw_preset)
                send_receive(b[0])
                
                # so now we need to know what was in that preset
                comms.send_preset_request(hw_preset)
                dat = comms.get_data()
                reader.set_message(dat)
                reader.read_message()
                asdict = eval(reader.python)

                # changed preset so update our local view of it
                pedals = asdict["Pedals"]
                effects_current["Noisegate"]  = pedals[0]["Name"]
                effects_current["Compressor"] = pedals[1]["Name"]
                effects_current["Drive"]      = pedals[2]["Name"]
                effects_current["Amp"]        = pedals[3]["Name"]
                effects_current["Mod"]        = pedals[4]["Name"]
                effects_current["Delay"]      = pedals[5]["Name"]
                effects_current["Reverb"]     = pedals[6]["Name"]                
            elif this_cmd == "ChangeParam":
                effect_type = s_cmd[1]
                current_effect = effects_current[effect_type]
                param_num = s_cmd[2]
                print ("Change %s (%s) param number %d to %f" % (effect_type, current_effect, param_num, m_param_val))
                b=msg.change_effect_parameter(current_effect, param_num, m_param_val)
                just_send(b[0])
            elif this_cmd == "ChangeEffect":
                effect_type = s_cmd[1]
                new_effect = s_cmd[2]
                current_effect = effects_current[effect_type]
                effects_current[effect_type] = new_effect
                print ("Change %s from %s to %s" % (effect_type, current_effect, new_effect))
                b=msg.change_effect(current_effect, new_effect)
                send_receive(b[0])
            elif this_cmd == "EffectOnOff":
                effect_type = s_cmd[1]
                new_value = s_cmd[2]
                current_effect = effects_current[effect_type]
                print ("Change %s (%s) to %s" % (effect_type, current_effect, new_value))
                b=msg.turn_effect_onoff(current_effect, new_value)
                send_receive(b[0])
            elif this_cmd == "ChangePreset":
                new_preset_name = s_cmd[1]
                new_preset = spark_presets[new_preset_name]
                print ("Change to new preset ", new_preset["Name"])
                b = msg.create_preset(new_preset)
                send_preset(b)
                
                pedals = new_preset["Pedals"]
                effects_current["Noisegate"]  = pedals[0]["Name"]
                effects_current["Compressor"] = pedals[1]["Name"]
                effects_current["Drive"]      = pedals[2]["Name"]
                effects_current["Amp"]        = pedals[3]["Name"]
                effects_current["Mod"]        = pedals[4]["Name"]
                effects_current["Delay"]      = pedals[5]["Name"]
                effects_current["Reverb"]     = pedals[6]["Name"]                   
    pygame.time.wait(10)


if cs is not None:
    cs.close()
