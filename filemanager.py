import os
import zipfile
import subprocess
import winreg

def get_default_program(file_extension):
    """Fetch the default program associated with a file extension on Windows."""
    try:
        # Open registry key for the file extension
        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f'.{file_extension}')
        file_type = winreg.QueryValue(registry_key, '')  # Get file type (e.g., txtfile)
        if not file_type:
            raise FileNotFoundError(f"No file type associated with .{file_extension}")
        
        # Open registry key for the program ID
        prog_id_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f'{file_type}\\shell\\open\\command')
        program = winreg.QueryValue(prog_id_key, '')  # Get default program command
        program = program.split('"')[1] if '"' in program else program.split(' ')[0]
        return program
    except FileNotFoundError:
        return None
    except OSError as e:
        print(f"Error accessing the registry for .{file_extension}: {e}")
        return None

def store_file_in_zip(zip_filename, file_path):
    """Store a file in the zip archive."""
    with zipfile.ZipFile(zip_filename, 'a') as zipf:
        zipf.write(file_path, os.path.basename(file_path))

def extract_file_from_zip(zip_filename, file_name, extract_to='.'):
    """Extract a file from the zip archive."""
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        zipf.extract(file_name, extract_to)

def remove_file_from_local(zip_filename, file_name):
    """Remove a file from the zip archive."""
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        file_list = zipf.namelist()

    if file_name in file_list:
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for f in file_list:
                if f != file_name:
                    zipf.write(f)

def overwrite_file(zip_filename, old_file_name, new_file_path):
    """Overwrite a file in the archive."""
    remove_file_from_local(zip_filename, old_file_name)
    store_file_in_zip(zip_filename, new_file_path)

def read_file_from_local(zip_filename, file_name):
    """Read (print) the content of a file from the zip archive."""
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        zipf.extract(file_name, 'temp')
    
    try:
        with open(f'temp/{file_name}', 'r') as f:
            print(f.read())
    except UnicodeDecodeError:
        print("This is a binary file, cannot print its content.")
    finally:
        os.remove(f'temp/{file_name}')

def edit_file(zip_filename, file_name, new_data):
    """Edit a file's content inside the archive."""
    remove_file_from_local(zip_filename, file_name)
    with open('temp_file', 'w') as f:
        f.write(new_data)  # Assuming text data for simplicity
    store_file_in_zip(zip_filename, 'temp_file')
    os.remove('temp_file')

def open_file_with_program(file_path):
    """Open the file using the default program for its extension."""
    file_extension = os.path.splitext(file_path)[-1].lower().replace('.', '')  # Extract file extension
    program = get_default_program(file_extension)
    
    if program:
        try:
            subprocess.run([program, file_path], check=True)
            print(f"Opening {file_path} with {program}")
        except Exception as e:
            print(f"Failed to open {file_path}: {e}")
    else:
        print(f"No default program found for .{file_extension} files. Attempting system default...")
        try:
            subprocess.run(['start', file_path], shell=True)
        except Exception as e:
            print(f"Failed to open {file_path} with the system default: {e}")

def open_extracted_file(zip_filename, file_name):
    """Extract the file and open it with the default program."""
    extract_file_from_zip(zip_filename, file_name)
    open_file_with_program(file_name)

def wipe_memory(zip_filename):
    """Delete all files from the zip archive."""
    try:
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            pass  # Opening in 'w' mode clears the existing content of the zip file
        print("All files have been deleted from memory.")
    except Exception as e:
        print(f"Error while wiping memory: {e}")

def main():
    print("FILE MANAGER")
    zip_filename = 'memory.zip'

    while True:
        print("\nCommands: add, remove, overwrite, read, edit, open, wipe, exit")
        command = input("Enter command: ").strip().lower()

        if command == 'add':
            file_path = input("Enter the path of the file to add: ").strip()
            if os.path.isfile(file_path):
                store_file_in_zip(zip_filename, file_path)
                print(f"File {file_path} added to local storage.")
            else:
                print("File not found!")

        elif command == 'remove':
            file_name = input("Enter the file name to remove: ").strip()
            remove_file_from_local(zip_filename, file_name)
            print(f"File {file_name} removed from local storage.")

        elif command == 'overwrite':
            old_file_name = input("Enter the file name to overwrite: ").strip()
            new_file_path = input("Enter the path of the new file: ").strip()
            if os.path.isfile(new_file_path):
                overwrite_file(zip_filename, old_file_name, new_file_path)
                print(f"File {old_file_name} overwritten with {new_file_path}.")
            else:
                print("New file not found!")

        elif command == 'read':
            file_name = input("Enter the file name to read: ").strip()
            read_file_from_local(zip_filename, file_name)

        elif command == 'edit':
            file_name = input("Enter the file name to edit: ").strip()
            new_data = input("Enter the new content: ")
            edit_file(zip_filename, file_name, new_data)
            print(f"File {file_name} edited.")

        elif command == 'open':
            file_name = input("Enter the file name to open: ").strip()
            open_extracted_file(zip_filename, file_name)

        elif command == 'wipe':
            confirm = input("Are you sure you want to delete everything? (y/n): ").strip().lower()
            if confirm == 'y':
                wipe_memory(zip_filename)
            else:
                print("Wipe operation canceled.")

        elif command == 'exit':
            print("Exiting program.")
            break

        else:
            print("Invalid command. Try again.")

