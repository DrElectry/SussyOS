import browse
import filemanager
import programmer
import socket
from pathlib import Path

print("Booting Up SussyOS...")

def check_internet():
    try:
        # Connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

if check_internet():
    print("Succesfully Connected to the Internet!")
else:
    print("Warning! No Internet Connection, browser wouldn't work!")
    
my_file = Path("memory.zip")
if my_file.is_file():
    print("Memory founded...")
else:
    print("Warning! No memory found, it will be created dynamicly...")
    
my_file = Path("filemanager.py")
if my_file.is_file():
    print("File Manager is founded...")
else:
    print("ERROR: No File Manager is founded!")

my_file = Path("browse.py")
if my_file.is_file():
    print("Browser is founded...")
else:
    print("ERROR: No Browser is founded!")
my_file = Path("programmer.py")
if my_file.is_file():
    print("Programmer is founded...")
else:
    print("ERROR: No Programmer is founded!")
    
print("Booted Succesfully! :)")

print("\n")
print("-----------------------------------------------------------------")
print("#######  #     #  #######  #######  #     #      #######  #######")
print("#        #     #  #        #         #    #      #     #  #")
print("#######  #     #  #######  #######    #####      #     #  #######")
print("      #  #     #        #        #        #      #     #        #")
print("#######  #######  #######  #######  ######       #######  #######")
print("-----------------------------------------------------------------")
print("\n")

def main():
    while True:
        command = input("Command: ")
        if command == "help":
            print("HELP")
            print("\n")
            print("--------------------------------")
            print("browser - launches sussy browser")
            print("filemanager - launches file manager")
            print("programmer - lua programmer mode")
            print("exit - exit sussyos")
            print("--------------------------------")
            print("\n")
            print("REMEMBER: ONLY SMALL LETTERS IN COMMANDS!")
        if command == "browser":
            browse.main()
        if command == "filemanager":
            filemanager.main()
        if command == "programmer":
            programmer.main()
        if command == "exit":
            break
        else:
            print("Wrong command! use 'help' for list of commands")
        
main()