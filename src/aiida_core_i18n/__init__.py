import re
import typing
import deepl
import os

DEEPL_TOKEN = os.environ.get("DEEPL_TOKEN")

def str_post_processing(raw_str: str) -> str:
    """deepl zh_CN has problem when translate the `` in CJK from English,
    this method will handle the process of it to render code snippet.
    """
    # if `{any_str}' -> ``{any_str}``
    tstr = re.sub(r"""(?:(?:(?<!`)(?<!:))`(\w.*?)')""", r'``\1``', raw_str, flags=re.ASCII)
    
    # if \" {any_str} \" -> ``{any_str}``
    tstr = re.sub(r'(?<!\w)\"(.*?)\"', lambda m: f"``{m.group(1).strip()}``", tstr, flags=re.ASCII)
    
    # Final process
    # for `{content}` make sure a space in front
    add_space = re.sub(r'(?:(?:(?<!^)(?<!\s)(?<!`)(?<!:))(`\w.*?`))', r' \1', tstr, flags=re.ASCII)
    
    # for ``{content}`` make sure a space in front
    res = re.sub(r'(?:(?:(?<!^)(?<!\s)(?<!`))(``\w.*?``))', r' \1', add_space, flags=re.ASCII)
    
    return res.strip()

def translate(inp_str: str, target_lang="ZH") -> str:
    """Call deepl API to tranlate and do post process"""
    translator = deepl.Translator(DEEPL_TOKEN)
    
    # `` -> EDBS after translated, recover to ``
    # EDBS for End Double BackSlash
    
    # substitute the `` with EDBS
    tstr = inp_str.replace('``', 'EDBS')
    
    try:
        translated = translator.translate_text(
            tstr, 
            source_lang="EN", 
            target_lang=target_lang,
            # formality="more", # not supported by ZH
        )
    except deepl.DeepLException as exc:
        return ""
    else:
        # substitue EDBS back to ``
        tstr = translated.text
        tstr = tstr.replace('EDBS', '``')
        
        res = str_post_processing(tstr)
        
        return res

def po_translate(lines: typing.List[str], override: bool = False) -> typing.List[str]:
    """Translate the po files line by line"""
    output_lines = [i for i in lines]
    for ln, line in enumerate(lines):
        if line.startswith("msgid "):
            ln_start = ln
            for count, inner_line in enumerate(lines[ln:]):
                if inner_line.startswith("msgstr "):
                    ln_end = ln_start + count
                    break
                
            # if translated, skip， otherwise the result will be overwritten
            if lines[ln_end] != 'msgstr ""' and not override:
                continue
            
            if ln_end - ln_start > 1:
                # combine the string from multiple lines
                inp_str = "".join([i.strip('"') for i in lines[ln_start+1:ln_end]])
            else:
                # get the string from double quotes
                inp_str = line.removeprefix('msgid "').removesuffix('"')
                
            # Do nothing to empty str
            if inp_str == "":
                continue
            
            translated = translate(inp_str)
            output_lines[ln_end] = f'msgstr "{translated}"'
            
    return output_lines
    
            