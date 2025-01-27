import zipfile
import os
from lupa import LuaRuntime

# Memory storage file (the zip file)
MEMORY_FILE = "memory.zip"

def create_or_open_memory():
    # Create or open the memory.zip file
    if not os.path.exists(MEMORY_FILE):
        with zipfile.ZipFile(MEMORY_FILE, 'w') as zf:
            pass  # Create an empty zip file
    return zipfile.ZipFile(MEMORY_FILE, 'a')

def list_files():
    with create_or_open_memory() as memory:
        return memory.namelist()

def write_program(filename):
    program_content = []
    print(f"Entering program mode. Write your code. Type 'OS_EXIT' to finish.")
    while True:
        line = input(f"{filename} > ").strip()
        if line == "OS_EXIT":
            break
        else:
            program_content.append(line)  # Add the line to the program content
    full_content = "\n".join(program_content)  # Join all lines with newline characters
    with create_or_open_memory() as memory:
        memory.writestr(filename, full_content)
    print(f"Program '{filename}' written successfully.")

def modify_program(filename):
    with create_or_open_memory() as memory:
        if filename not in memory.namelist():
            print(f"Program '{filename}' not found.")
            return
        existing_content = memory.read(filename).decode()
        program_content = existing_content.splitlines()
        print(f"Modifying '{filename}'. Existing content loaded. Type 'OS_EXIT' to finish.")
        while True:
            for idx, line in enumerate(program_content):
                print(f"{idx + 1}: {line}")
            line_number = input(f"Enter line number to edit or type 'add' to add a new line (or 'OS_EXIT' to finish): ").strip()
            if line_number.lower() == "os_exit":
                break
            elif line_number.lower() == "add":
                new_line = input(f"New line: ").strip()
                program_content.append(new_line)
            elif line_number.isdigit() and 1 <= int(line_number) <= len(program_content):
                new_line = input(f"New content for line {line_number}: ").strip()
                program_content[int(line_number) - 1] = new_line
            else:
                print("Invalid input. Please try again.")
        full_content = "\n".join(program_content)  # Join the modified content
        memory.writestr(filename, full_content)
        print(f"Program '{filename}' modified successfully.")

def remove_program(filename):
    with create_or_open_memory() as memory:
        if filename in memory.namelist():
            temp = memory.namelist()
            temp.remove(filename)
            with zipfile.ZipFile(MEMORY_FILE, 'w') as new_memory:
                for file in temp:
                    new_memory.writestr(file, memory.read(file))
            print(f"Program '{filename}' removed.")
        else:
            print("File not found.")

def run_lua_program(filename):
    with create_or_open_memory() as memory:
        if filename in memory.namelist():
            lua_code = memory.read(filename).decode()
            lua = LuaRuntime(unpack_returned_tuples=True)  # Lua runtime
            try:
                # Run the Lua script
                result = lua.execute(lua_code)
                print(f"Lua Script Output: {result}")
            except Exception as e:
                print(f"Error running Lua script: {e}")
        else:
            print("File not found.")

def main():
    print("PROGRAMMER")
    print("\n")
    while True:
        command = input("Enter command: ").strip().lower()

        if command == "exit":
            break
        elif command == "help":
            "PROGRAMMER HELP"
            print("\n")
            print("---------------------------------------------")
            print("write NAME - creates a lua script with NAME")
            print("modify NAME - modifies a lua script with NAME")
            print("remove NAME - removes lua script with NAME")
            print("run NAME - runs lua script with NAME")
            print("list - printing every file (definately not useless)")
            print("exit - exit the programmer")
            print("---------------------------------------------")
            print("\n")
            print("REMEMBER: ONLY SMALL LETTERS IN COMMANDS! (NOT WHEN PROGRAMMING)")
        elif command == "list":
            print(list_files())
        elif command.startswith("write "):
            _, filename = command.split(" ", 1)
            write_program(filename)
        elif command.startswith("modify "):
            _, filename = command.split(" ", 1)
            modify_program(filename)
        elif command.startswith("remove "):
            _, filename = command.split(" ", 1)
            remove_program(filename)
        elif command.startswith("run "):
            _, filename = command.split(" ", 1)
            run_lua_program(filename)
        else:
            print("Unknown command! use 'help' for list of commands")
