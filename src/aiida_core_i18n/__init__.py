import re
import typing
import deepl
import os

DEEPL_TOKEN = os.environ.get("DEEPL_TOKEN")

def str_pp(raw_str):
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

def translate(inp_str, target_lang="ZH"):
    """Call deepl API to tranlate and do post process"""
    translator = deepl.Translator(DEEPL_TOKEN)
    
    try:
        translated = translator.translate_text(
            inp_str, 
            source_lang="EN", 
            target_lang=target_lang,
            # formality="more", # not supported by ZH
        )
    except deepl.DeepLException as exc:
        return ""
    else:
        res = str_pp(translated.text)
        
        return res

def po_translate(lines: typing.List[str]):
    output_lines = [i for i in lines]
    for ln, line in enumerate(lines):
        if line.startswith("msgid "):
            ln_start = ln
            for count, inner_line in enumerate(lines[ln:]):
                if inner_line.startswith("msgstr "):
                    ln_end = ln_start + count
                    break
                
            # print(f"start: {ln_start}: {lines[ln_start]}")
            # print(f"end: {ln_end}: {lines[ln_end]}")
            
            # if translated, skip， otherwise will override the translated result
            if lines[ln_end] != 'msgstr ""':
                continue
            
            if ln_end - ln_start > 1:
                inp_str = "".join([i.strip('"') for i in lines[ln_start+1:ln_end]])
            else:
                # get the string from double quotes
                inp_str = line.removeprefix('msgid "').removesuffix('"')
                
            # Do nothing to empty str
            if inp_str == "":
                continue
            
            translated = translate(inp_str)
            output_lines[ln_end] = f'msgstr "{translated}"'
            
    print('\n'.join(output_lines))
    return output_lines
    
            