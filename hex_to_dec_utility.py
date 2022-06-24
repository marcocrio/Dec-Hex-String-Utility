#!/usr/bin/python

from distutils.log import error
import sys

import re


print ('\nNumber of arguments:', len(sys.argv)-1, 'arguments.')
print ('Argument List:', str(sys.argv[-(len(sys.argv)-1):]))
print ('\n')


try:

    #intialization
    argLen          = len(sys.argv)-1
    argList         = sys.argv[-(len(sys.argv)-1):]

    commands        = []
    arguments   = []
    charString      = ""

    #allowed_chars = set('32')

    for i in argList:

        if( i[:1] == "-"): 
            commands.append(i)
        else:
            if not(bool(re.match('^[012345678ABCDEFabcdef,xX]+$', i))): raise ValueError("Your '" + str(i) + "' argument is incorrectly formatted")
            arguments.append(i)


    print("Command:")        
    print( commands)

    print("Arguments:")
    print(arguments)
    print("\n")



    #Prints Description of available commands
    command = "-h" in commands  or   "--help" in commands
    if( commands[0] == "-h" or  commands[0] == "-help"):
        print ( "-h --help" )
        
        

#more than 3 argumens, could either be an argument with a flag or an argument with a space separated string of n bytes

#example 2: -m FF AA FF -> FFAAFF

    

#--------------------------------------------------------------------------------------------------------------------------#
#Prints a string of n separated byte-words in hex format with or w/o prefix in a comma separated or space separated fashion
#example 1: -c -p -cs 4 -> 0x01, 0x02, 0x03, 0x04

    command = "-c"  in commands or "--count"  in commands
    prefix  = "-p"  in commands or "--prefix" in commands #checks for prefix flag
    cs      = "-cs" in commands or "--comma"  in commands #checks for comma separated
    ns      = "-ns" in commands or "--no-sep" in commands #checks for no space separation

    if(command):
        print ( "-c --count:" )

        countNumber = int( arguments[0] ) if (int( arguments[0] ) < 257) else 256 #limits to 128 byte-words

        for i in range( countNumber  ): #Creates the count

            if(prefix): charString += "0x"      #appends prefix if chosen
            charString += '{:02X}'.format(i)    #prints the count
            if(cs):  charString += ","          #checks if -cs (comma separated) flag was setup
            if(not ns): charString += " "       #checks if no separation flag
        
        if(cs): charString = charString[:len(charString)-1]

#--------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------------------------------------#
#PENDING COMMENTING

    command = "-s"  in commands or "--separate"  in commands
    prefix  = "-p"  in commands or "--prefix" in commands #checks for prefix flag
    cs      = "-cs" in commands or "--comma"  in commands #checks for comma separated
    
    if(command):
        print ( "-s --separate:" )
        strToSep = arguments[0]

        if( not(len(strToSep)%2 ==0) ): raise ValueError('The provided string to be separated is not an even number')

        count = 1
        for x in strToSep: #Creates the count
            count = count + 1
            if(count%2==0):
                if(cs):  charString += ","          #checks if -cs (comma separated) flag was setup
                charString += " "                   #appends space
                if(prefix): charString += "0x"      #appends prefix if chosen
                count =0                            #resets count
                        
            charString +=x
            

        
        #correct added characters
        charString = charString[ - (len(charString)-2)  :] if(cs) else charString[ - (len(charString)-1)  :] 

#--------------------------------------------------------------------------------------------------------------------------#
            
#--------------------------------------------------------------------------------------------------------------------------#
#PENDING COMMENTING


    command = "-j"  in commands or "--join"   in commands
    prefix  = "-p"  in commands or "--prefix" in commands #checks for prefix flag
    cs      = "-cs" in commands or "--comma"  in commands #checks for comma separated
    
    if(command):
        print ( "-j --join:" )

        for x in arguments:
            #if( not((len(x)%2) == 0) ): raise ValueError('The provided string to be separated is not an even number')

            if(prefix): charString += "0x"      #appends prefix if chosen
            charString += str(x)
            if(cs):  charString += ","          #checks if -cs (comma separated) flag was setup

        if(cs): charString = charString[:len(charString)-1]

#--------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------#
    #Format:    -r 4 AA
    # Return:   AA AA AA AA   


    command = "-r"  in commands or "--repeat" in commands
    prefix  = "-p"  in commands or "--prefix"   in commands #checks for prefix flag
    cs      = "-cs" in commands or "--comma"    in commands #checks for comma separated
    ns      = "-ns" in commands or "--no-sep"   in commands #checks for no space separation

    if(command):
        print ( "-r --repeat:" )
        
        countNumber = int( arguments[0] ) if (int( arguments[0] ) < 257) else 256 #limits to 128 byte-words

        for x in range(int(arguments[0])):

            if(prefix): charString += "0x"      #appends prefix if chosen
            charString += arguments[1]
            if(cs):  charString += ","          #checks if -cs (comma separated) flag was setup
            if(not ns): charString += " "       #checks if no separation flag
            

        if(cs): charString = charString[:len(charString)-1]


#--------------------------------------------------------------------------------------------------------------------------#

    command = "-cln"    in commands or "--clean" in commands
    prefix  = "-p"      in commands or "--prefix"   in commands #checks for prefix flag
    ns      = "-ns"     in commands or "--no-sep"   in commands #checks for no space separation

    if(command):
        print ( "-c --clean:" )

        for x in arguments:
            x = x.replace(",","")
            x = x.replace("0x","") if ns else x.replace("0x"," ")
            charString += x


#--------------------------------------------------------------------------------------------------------------------------#


#features to add: 
    #Read from file (convert from file)
    #add leading 0's when singe character provided
    #convert decimal to hex
    #chek if array is already -s    
    #generate random
    #backwards count on -c 
    #separate by any character given
    #if separated by any chars


except Exception as e:
    print("\n\nError:")
    print(e)
    print("Please check your arguments.")
    print("\n")
    sys.exit()

try:

    #correct any possible added characters
    if(charString):
        if( charString[len(charString)-1]== " " or charString[len(charString)-1]== "," ): charString = charString[:len(charString)-1]
        print(charString)
        
    print("\n")

except:
    print("\n")
    sys.exit()