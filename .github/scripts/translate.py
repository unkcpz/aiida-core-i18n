#!/usr/bin/env python
import os
import subprocess
import glob

def list_files_by_size(folder_path):
    files = glob.glob(folder_path + "*")
    files.sort(key=lambda file: os.path.getsize(file))
    return files

def translate_files(lang):
    folder_path = f"./translations/{lang}/"
    files = list_files_by_size(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)
        character_limit = get_character_limit() * 0.8
        file_content = read_file(file_path)

        if len(file_content) <= character_limit:
            translated_content = translate_text(file_content)
            write_file(file_path, translated_content)
        else:
            print(f"File {file} exceeds the character limit.")

def get_character_limit():
    # Call the API to get the character limit
    # Replace this with the actual API call
    return 10000

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

def translate_text(text):
    # Call the aiida-core-i18n command to translate the text
    # Replace this with the actual command
    translated_text = subprocess.check_output(["aiida-core-i18n", "translate", text])
    return translated_text.decode("utf-8")

# Example usage
translate_files("en")
