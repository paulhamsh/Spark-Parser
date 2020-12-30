fi = open ("arduino_preset.txt","r")
print ("[")
for lin in fi:
    st = lin.find ("{")
    end = lin.find ("}")

    l2 = lin[st+1:end-1]
    l3 = l2.replace("0x","")
    l4 = l3.replace (",","")
    print ("\""+l4+"\",")

print ("]")
fi.close()
