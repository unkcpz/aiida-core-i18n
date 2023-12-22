#!/usr/bin/env python
import argparse
import pathlib
import subprocess

def list_files_by_size(folder_path: pathlib.Path):
    files = [f for f in folder_path.glob("*")]
    files.sort(key=lambda file: file.stat().st_size)

    return files

def calc_count() -> int:
    """Run aiida-core-i18n status and return the count"""
    res = subprocess.run(["aiida-core-i18n", "status", "-p", "count"], check=True, capture_output=True)

    return int(res.stdout)

def calc_avail() -> int:
    """Run aiida-core-i18n status and return the available characters"""
    res = subprocess.run(["aiida-core-i18n", "status", "-p", "avail"], check=True, capture_output=True)

    return int(res.stdout)

def translate_files(folder_path: pathlib.Path, character_limit: int = 500):
    if not folder_path.is_dir():
        print(f"ERROR: {folder_path} is not a folder")
        return
    
    files = list_files_by_size(folder_path)

    used = 0
    i_count = calc_count()
    total_avail = calc_avail()
    if total_avail < character_limit:
        print(f"ERROR: The total available characters {total_avail} is less than the character limit {character_limit}")
        character_limit = total_avail
        
    session_avail = character_limit
    for file in files:
        session_avail -= used
        print(f"Available characters in this session: {session_avail}")

        if session_avail <= 0:
            print("Run out of characters in this session, exit.")
            break
        
        print(f"Translating {file.name}...")
        subprocess.run(["aiida-core-i18n", "translate", str(file), "--max-chars", str(session_avail), "--override-file"], check=True)

        # calculate how many characters used this translation session
        new_count = calc_count()
        used = new_count - i_count
        i_count = new_count

        print(f"Translated {used} characters in this session")
        
if __name__ == "__main__":
    # use argparse to get the folder path and character limit
    parser = argparse.ArgumentParser()

    parser.add_argument("folder_path", help="The path to the folder containing the files to translate", type=pathlib.Path)
    parser.add_argument("--limit", help="The character limit for the translation", default=500, type=int)

    args = parser.parse_args()

    translate_files(args.folder_path, args.limit)
