"""Tool to translate raw en strings to every languages
bookkeeping the Deepl API behavior by date.
"""
import pathlib
from datetime import datetime

from aiida_core_i18n import translate

# list of original strings (English)
inp_strs = [
    r"Please visit the `Discourse forum <https://aiida.discourse.group>`__.",
]

rec_folder = pathlib.Path(__file__).parent / "_bookkeeping"

def rec(inp_strs: list[str], lang: str, output_folder: pathlib.Path):
    """Write raw strings to the file"""

    if not output_folder.is_dir():
        output_folder.mkdir(parents=True)

    # Call translate to the inp_strs and record the result
    # by the date of running this script, and save to the _bookkeeping folder
    with open(output_folder / f"{lang}_{datetime.now().strftime('%Y-%m-%d')}.txt", "w") as fh:
        # write the metadata (date, lang) to the file
        fh.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
        fh.write(f"Source: EN Target: {lang}\n\n")
        
        for inp_str in inp_strs:
            res = translate(inp_str, target_lang=f"{lang}", post_processing=False)

            fh.write(f"Input: \n\t{inp_str}\n")
            fh.write(f"Output: \n\t{res}\n\n")

if __name__ == "__main__":
    # record the raw strings and the translated strings
    rec(inp_strs, "ZH", rec_folder)

    # compare the file with the previous one in date, if the same (exclude the first line for date) 
    # means the API behavior is the same as before, remove the newly created file. 

    # find the latest two files by date (2023-12-23) in filename (ZH_2023-12-23.txt)
    files = sorted(rec_folder.glob("ZH_*.txt"), key=lambda f: f.name.lstrip("ZH_").rstrip(".txt"), reverse=True)[:2]

    if len(files) < 2:
        print("No enough files to compare, exit")
        exit(1)

    # compare the two files if the same remove the one with the latest date
    with open(files[0], "r") as fh0, open(files[1], "r") as fh1:
        lines0 = fh0.readlines()[1:]
        lines1 = fh1.readlines()[1:]

        if lines0 == lines1:
            print("Same API behavior, remove the newly created file")
            files[0].unlink()
        
    
