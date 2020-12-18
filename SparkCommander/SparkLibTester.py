########
#
# Spark Commander
#
# Program to send commands to Positive Grid Spark
#
# See https://github.com/paulhamsh/Spark-Parser

#### PRESETS ####

from AllPresets import *
from SparkLib import *



for i in range (len(preset_list)):
    b = pack_preset(preset_list[i])

    for x in range(len(b)):
        if b[x].hex() != preset_listh[i][x]:
            print("ERROR\n")
            print(b[x].hex())
            print(preset_listh[i][x])
    print()
print()

    
