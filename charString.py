import sys

print('Number of arguments: {}'.format(len(sys.argv)))
print('Argument(s) passed: {}'.format(str(sys.argv)))

charString = ""

if(sys.argv[1] != 'rs'):
    
    for i in range( (int(sys.argv[1]))  ): #loop of how many numbers 
        
        if(sys.argv[2]=='c'):
            charString += '{:02X}'.format(i)+" "
        
        #separates an n number of x bytes in hex. Format: s xx xx xx xx... (for adding space every byte in the 4 byte string)
        #example: s FF CC FF
        #result: FFCCFF 
        elif(sys.argv[2]=='s'):
            charString += sys.argv[2]+ " "

        #adds a prefix to a provided n array of xx bytes (separated)
        #Format: pf 11 11 11 11
        #result: 0x11, 0x11, 0x11, 0x11,
        elif(sys.argv[2]=='pf'):
            comma = ""    
            if(i!=(int(sys.argv[1]))): 
                comma=","
            charString += "0x" + sys.argv[2]+ comma


#returns an n array of a count from 0 to n bytes. Format: n xx, example: 4 FF
# would return FF FF FF FF 
elif (len(sys.argv)<4):
    count = 1

    for x in (str(sys.argv[2])):
        count = count + 1 
        if(count%2==0):
            charString +=" "
            count =0
        charString +=x




#removes space from a n number of x bytes in hex. Format: s xxxxxxxx... (for adding space every byte in the 4 byte string)
#example: s FFCCFF
#result: FF CC FF
else:
    for x in range(2,len(sys.argv)):
        charString += str(sys.argv[x])

print(charString)
