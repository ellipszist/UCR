import glob
import json
import msvcrt
import os

def select_input(prompt, options):
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    while True:
        try:
            selected_option = int(input("Enter your choice: "))
            if selected_option < 1 or selected_option > len(options):
                print("Invalid input, please enter a valid number.")
                continue
            return options[selected_option - 1]
        except ValueError:
            print("Invalid input, please enter a valid number.")

def replace_characters(input_directory, output_directory, file_type, mapping_file):
    files = glob.glob(input_directory + f"/**/*.{file_type}", recursive=True)
    try:
        with open(mapping_file, "r") as mapping_file:
            character_mapping = json.load(mapping_file)
    except Exception as e:
        print(f"An error occurred while loading the mapping file: {e}")
        return False
    mapping = character_mapping.get("mapping")
    if not mapping:
        print("Mapping information not found.")
        return False
    metadata = character_mapping.get("metadata")
    if metadata:
        if metadata.get("author"):
            print(f"Author: {metadata.get('author')}")
        if metadata.get("source"):
            print(f"Source: {metadata.get('source')}")
        if metadata.get("date"):
            print(f"Date: {metadata.get('date')}")
        if metadata.get("contact"):
            print(f"Contact: {metadata.get('contact')}")
        if metadata.get("version"):
            print(f"Version: {metadata.get('version')}")
        if metadata.get("description"):
            print(f"Description: {metadata.get('description')}")
        if metadata.get("license"):
            print(f"License: {metadata.get('license')}")
    if os.path.exists(output_directory):
        response = input(f"The output directory '{output_directory}' already exists. Do you want to overwrite the files? (y/n) ")
        if response.lower() != 'y':
            print("Aborted.")
            return False
    success_count = 0
    fail_count = 0
    for file_path in files:
        try:
            with open(file_path, "r") as f:
                data = f.read()
        except Exception as e:
            print(f'An error occurred while reading {file_path} : {e}')
            fail_count += 1
            continue
        try:
            for old_char, new_char in mapping.items():
                data = data.replace(old_char, new_char)
        except Exception as e:
            print(f'An error occurred while replacing characters in {file_path} : {e}')
            fail_count += 1
            continue
        output_directory_path = os.path.dirname(file_path.replace(input_directory, output_directory))
        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)
        output_file_path = file_path.replace(input_directory, output_directory)
        try:
            with open(output_file_path, "w") as f:
                f.write(data)
            success_count += 1
        except Exception as e:
            print(f'An error occurred while writing {output_file_path} : {e}')
            fail_count += 1
            continue
    print(f"{success_count} files successfully processed.")
    if fail_count:
        print(f"{fail_count} files failed to process.")
    return True

directories = [directory for directory in os.listdir() if os.path.isdir(directory) and directory not in ["Mapping", "docs", ".git", "build", "dist"]]
input_directory = select_input("Select the input directory:", directories)

output_directory = input_directory + "_New"

text_file_types = ['txt', 'log', 'csv', 'ini', 'md', 'html', 'css', 'js', 'json']
file_types = list(set([file.split(".")[-1] for subdir, dirs, files in os.walk(input_directory) for file in files if file.split(".")[-1] in text_file_types]))
file_type = select_input("Select the file type:", file_types)

mapping_files = [file for file in os.listdir("Mapping") if file.endswith(".json")]
mapping_file = select_input("Select the mapping file:", mapping_files)
mapping_file = os.path.join("Mapping", mapping_file)

replace_characters(input_directory, output_directory, file_type, mapping_file)

print("\n\nPress any key to exit")
msvcrt.getch()
