#!/usr/bin/python

import sys
import re

print_cancel = False

def byteStringToHex(hexString) -> int:
    hexLetters = { 
        "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15,
        "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15 
    }
    decimal = 0
    shiftCnt = len(hexString) - 1
    for x in hexString:
        decVal = int(x, 16) if x.isdigit() else hexLetters[x]
        decimal += (decVal << (shiftCnt * 4))
        shiftCnt -= 1
    return decimal

def format_hex_string(hex_string):
    # Check if the string contains '0x' or '0X'. If it does, return it as is.
    if '0x' in hex_string or '0X' in hex_string:
        return hex_string

    # Split the string by commas
    hex_values = hex_string.split(',')

    # Prepend '0' if the hex value is a single digit and rejoin the string
    formatted_hex_values = [value if len(value) == 2 else '0' + value for value in hex_values]

    return ','.join(formatted_hex_values)


def print_help():
    help_text = '''
Commands:

-h  | --help        # displays available commands.
-c  | --count       # returns n specified byte_words (i.e. 01 02 03 04), 4 in this example.
-s  | --separate    # separates a string into byte words.
                            # Use -p for adding '0x' prefix and -cs for comma-separated strings.
                            # Example: -s -p -cs "0x01,0x02,0x03"
-j  | --join        # joins a space-separated array of given byte_words. (i.e. 01 02 03 04 -> 01020304).
-r  | --repeat      # returns an array of n-length of repeated byte_words (i.e AA AA AA AA).
-cl | --clean       # removes commas and prefixes in a string of byte_words (i.e 0x01, 0x02, 0x03 -> 01 02 03).
-re | --rendi       # reverses the endianess of a string of byte word characters 

Not impemented yet:
-u  | --upperc      # turns all lower case characters into uppercase of a string
-l  | --lowerc      # turns all uppercase character into lowercase characters of a string

Flags:
Note: flags are intended to be added as support alongside the commands

-upp | --uppercase   # turns a lower case string into uppercase
-p   | --prefix      # 0x prefix flag (i.e. 01,02,03 -> 0x01,0x02,0x03)
-cs  | --comma       # comma separated flag
-ns  | --no-sep      # no space separated flag
-sp  | --start-point # starting point flag [Starts at a given number where (starting_point + n < 0xFF ). n = # of byte_words  ]
                            # -sp example: -c 5 -sp 5 --> 05 06 07 08 09  
                            # where the -sp argument is an integer so if starting point is to be 0A the -sp value should be 10
                     
'''
    print(help_text)

def handle_count_command(commands, arguments):
    prefix = "-p" in commands or "--prefix" in commands
    cs = "-cs" in commands or "--comma" in commands
    ns = "-ns" in commands or "--no-sep" in commands
    sp = "-sp" in commands or "--start-point" in commands

    # Check if the number argument is provided and is a valid integer
    if not arguments or not arguments[0].isdigit():
        print("A numeric argument is required for the count command.\n\n")
        return

    number_of_bytes = int(arguments[0])
    starting_point = 0
    if sp:
        # Validate starting point argument
        if len(arguments) < 2 or not arguments[1].isdigit():
            print("A numeric starting point is required with the -sp flag.\n\n")
            return

        starting_point = byteStringToHex(arguments[1]) if bool(re.match('^[ABCDEFabcdef]+$', arguments[1])) else int(arguments[1])
        if starting_point + number_of_bytes > 0xFF:
            raise ValueError('Starting point would make the count go beyond 0xFF, which is not permitted\n\n')

    charString = ""
    for i in range(starting_point, starting_point + number_of_bytes):
        if prefix:
            charString += "0x"
        charString += '{:02X}'.format(i)
        if cs:
            charString += ","
        if not ns:  # Add space if not no-separation flag
            charString += " "

    # Remove trailing comma and space if present
    if cs or not ns:
        charString = charString.rstrip(", ")

    print(charString)
    print('\n\n')


def handle_separate_command(commands, arguments):
    prefix = "-p" in commands or "--prefix" in commands
    cs = "-cs" in commands or "--comma" in commands

    if not arguments:
        print("No string provided for separation.")
        return

    hex_string = arguments[0]

    if ',' in hex_string:
        hex_values = hex_string.split(',')
        if prefix:
            # Add '0x' prefix only if it's not already present
            hex_values = ['0x' + val.strip() if not val.strip().lower().startswith('0x') else val.strip() for val in hex_values]


    elif '0x' in hex_string.lower() or '0X' in hex_string:
        # If string already contains prefixed byte words
        hex_values = hex_string.split('0x')[1:]  # Split and ignore empty first element
        hex_values = ['0x' + val for val in hex_values]  # Prepend '0x' to each value
        
    else:
        # Split continuous string into byte words
        hex_values = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
        if prefix:
            hex_values = ['0x' + val for val in hex_values]  # Add '0x' prefix

    # Determine separator based on -cs flag and current presence of commas
    if cs and not any(',' in val for val in hex_values):
        separator = ', '
    else:
        separator = ' '

    separated_string = separator.join(hex_values)

    print(separated_string)



    print('\n\n')


def handle_join_command(commands, arguments):
    prefix = "-p" in commands or "--prefix" in commands
    cs = "-cs" in commands or "--comma" in commands

    joined_string = ""

    for arg in arguments:
        hex_bytes = arg.split()

        for byte in hex_bytes:
            if prefix:
                joined_string += "0x"
            joined_string += byte
            if cs:
                joined_string += ","

    # Remove the trailing comma if necessary
    if cs and joined_string.endswith(","):
        joined_string = joined_string[:-1]

    print(joined_string)
    print('\n\n')

def handle_repeat_command(commands, arguments):
    prefix = "-p" in commands or "--prefix" in commands
    cs = "-cs" in commands or "--comma" in commands
    ns = "-ns" in commands or "--no-sep" in commands

    if len(arguments) < 2:
        print("The repeat command requires two arguments: the number of repetitions and the byte word.\n\n")
        return

    try:
        repeat_count = int(arguments[0])
    except ValueError:
        print("The first argument for the repeat command must be a valid integer.\n\n")
        return

    byte_word = arguments[1]

    # Check if the byte word already contains the '0x' prefix
    already_has_prefix = byte_word.startswith("0x") or byte_word.startswith("0X")

    repeated_string = ""
    for _ in range(repeat_count):
        if prefix and not already_has_prefix:
            repeated_string += "0x"
        repeated_string += byte_word
        if cs:
            repeated_string += ","
        if not ns:
            repeated_string += " "

    # Remove trailing comma and space if present
    if cs or not ns:
        repeated_string = repeated_string.rstrip(", ")

    print(repeated_string)
    print('\n\n')

def handle_clean_command(commands, arguments):
    if not arguments:
        if not print_cancel:
            print("No string provided for cleaning.\n\n")
        return

    prefix = "-p" in commands or "--prefix" in commands
    cs = "-cs" in commands or "--comma" in commands
    ns = "-ns" in commands or "--no-sep" in commands
    hex_string = arguments[0]

    # Remove '0x' or '0X' prefixes, spaces, and commas
    cleaned_string = hex_string.replace('0x', '').replace('0X', '').replace(',', '').replace(' ', '')

    # Insert space after every two characters (byte word)
    cleaned_string = ' '.join(cleaned_string[i:i+2] for i in range(0, len(cleaned_string), 2))

    if prefix:
        # Add '0x' prefix to each byte word
        cleaned_string = ' '.join('0x' + byte_word for byte_word in cleaned_string.split())

    if cs:
        # Add a comma after each byte word, except the last one
        byte_words = cleaned_string.split()
        cleaned_string = ', '.join(byte_words)

    if ns:
        # Remove all spaces if -ns flag is set
        cleaned_string = cleaned_string.replace(' ', '')

    if not print_cancel:
        print(cleaned_string)
        print('\n\n')

def handle_uppercase_command(commands, arguments):
    # Implement uppercase functionality
    print("Uppercase command not implemented yet.")

def handle_reverse_endianess_command(commands, arguments):
    if not arguments:
        print("No string provided for endianess reversal.\n\n")
        return

    hex_string = arguments[0]

    # Determine if the string is using '0x' or '0X' prefixes
    if '0x' in hex_string.lower():
        # Handle '0x' prefixed byte words
        byte_words = re.findall(r'0x[0-9A-Fa-f]{2}', hex_string)
    else:
        # Handle non-prefixed byte words
        # Remove commas and spaces, then split into byte words
        cleaned_string = hex_string.replace(',', '').replace(' ', '')
        byte_words = [cleaned_string[i:i+2] for i in range(0, len(cleaned_string), 2)]

    # Reverse the order of byte words
    reversed_string = ' '.join(byte_words[::-1])

    # global print_cancel
    # print_cancel = True
    handle_clean_command(commands, [reversed_string])
    # print_cancel = False

    # print(reversed_string)
    print('\n\n')


def main():
    argLen = len(sys.argv) - 1
    argList = sys.argv[1:]

    print('\nNumber of arguments:', argLen, 'arguments.')
    print('Argument List:', argList)
    print('\n')

    if not argList:
        print("No arguments provided. Use -h or --help for usage information.")
        sys.exit()

    # Process commands
    commands = [arg for arg in argList if arg.startswith("-")]
    arguments = [arg for arg in argList if not arg.startswith("-")]

    if "-h" in commands or "--help" in commands:
        print_help()

        
    elif "-c" in commands or "--count" in commands:
        handle_count_command(commands, arguments)
        

    elif "-s" in commands or "--separate" in commands:
        print("\nNote: This command requires to encapsulate your string in quotations marks: \"0x00,0x01,0x02\"... \n")
        handle_separate_command(commands, arguments)
        
        
    elif "-j" in commands or "--join" in commands:
        handle_join_command(commands, arguments)
    
    elif "-r" in commands or "--repeat" in commands:
        handle_repeat_command(commands, arguments)
    elif "-cl" in commands or "--clean" in commands:
        print("\nNote: This command requires to encapsulate your string in quotations marks: \"0x00,0x01,0x02\"... \n")
        handle_clean_command(commands, arguments)


    elif "-re" in commands or "--rendi" in commands:
        print("\nNote: This command requires to encapsulate your string in quotations marks: \"0x00,0x01,0x02\"... \n")
        handle_reverse_endianess_command(commands, arguments)

    # Add other command handlers here



if __name__ == "__main__":
    main()
