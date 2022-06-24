#! python3

from sys import argv

print("\n")

for i in range(1, len(argv)):
    print (  "{:02X}".format( int( argv[i] ) ) , end=" " )    
    
print("\n")