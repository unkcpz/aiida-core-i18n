import os
import errno
from pathlib import Path

src_files = {} # Where all original rst files are stored
langs = {} # All the languages of the project
docs_dir = "./aiida-core/docs"
index = 0

# Scan for .rst files
for root, dirs, files in os.walk(docs_dir):
    for file in files:
        # Populate a record in src_files with an empty list
        index = index + 1
        src_files[index] = []

        src_files[index].append(os.path.join(root, file)) # store full path as a first element in the list
        src_files[index].append(os.path.relpath(src_files[index][0], docs_dir)) # store part without root directory
                                                                                    # (file name with another directory)

# Find all languages
for root, dirs, files in os.walk("./locale"):
    for name in dirs:
        # mkdir of docs/<lang> if not exist
        Path(f"./docs/{name}").mkdir(parents=True, exist_ok=True)
        
        langs[name] = (os.path.join(root, name), f"./docs/{name}")
    break

# In each language folder create a symlink for .rst file
for lang, paths in langs.items():
    # create src link
    for idx, (abs_path, rel_path) in src_files.items():
        # print(abs, rel)
        src = os.path.join("../..", abs_path)
        for num in range(rel_path.count("/")):
            src = os.path.join("..", src)
        
        dest = os.path.join(paths[1], rel_path)
        
        print("Create symlink from " + src + " -> " + dest)
        try:
            os.symlink(src, dest)
        except FileNotFoundError as exc:
            path = os.path.dirname(dest)
            # print(path)
            print("parent folder not exist. create")
            Path(path).mkdir(parents=True, exist_ok=True)
            os.symlink(src, dest)
        except FileExistsError as exc:
            print("exist. override")
            os.remove(dest)
            os.symlink(src, dest)
            
    # create locale link
    src = os.path.join("../../..", "locale")
    dst = os.path.join(f"./docs/{lang}", "source/locale")
    
    os.symlink(src, dst)