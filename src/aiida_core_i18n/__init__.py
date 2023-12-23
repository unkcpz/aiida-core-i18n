import re
import typing
import deepl
import os
import typing as t

def get_env_deepl_token() -> str:
    """Get the deepl token from the environment variable"""
    return os.environ.get("DEEPL_TOKEN")

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

    # r"请访问 ``话语论坛 <https://aiida.discourse.group> `__``。" -> r"请访问 `话语论坛 <https://aiida.discourse.group>`__。"
    res = re.sub(r"``(.*?)\s+`__``", r"`\1`__ ", res, flags=re.ASCII)
    
    return res.strip()

def met_skip_rule(inp_str: str) -> bool:
    """The rule when met, skip the translation
    """
    # if string is a citation, skip (container link to a doi url)
    # e.g. Martin        Uhrin, It is a great day, Computational Materials Science **187**, 110086 (2021); DOI: `10.1016/j.commatsci.2020.110086 <https://doi.org/10.1016/j.commatsci.2020.110086>`_
    if re.match(r".*DOI: `.*? <https://doi.org/.*?>`_.*?", inp_str):
        return True
    
    return False

# We don't want to translate the code snippet, so we use
# a special string to replace the `` in the code snippet to avoid
# the translation.
# `` -> EDBS after translated, recover to ``
# EDBS for End Double BackSlash etc.
def replace_protected(inp_str: str) -> t.Tuple[str, dict[str, str]]:
    """Replace the protected characters"""
    pairs = {}
    pstr = inp_str.replace('``', 'EDBS')
    pairs['``'] = 'EDBS'
    
    return pstr, pairs

def revert_protected(pstr: str, pairs: dict) -> str:
    """Revert the protected characters"""
    for origin, gaurd in pairs.items():
        pstr = pstr.replace(gaurd, origin)
    
    return pstr

def translate(inp_str: str, target_lang="ZH", post_processing: bool=True) -> str:
    """Call deepl API to tranlate and do post process"""
    # If the inp_str meet the skip rule, return the inp_str immediately
    if met_skip_rule(inp_str):
        return inp_str
    
    translator = deepl.Translator(get_env_deepl_token())
    
    
    # Replace in order to be translated
    tstr, pairs = replace_protected(inp_str)

    try:
        translated = translator.translate_text(
            tstr, 
            source_lang="EN", 
            target_lang=target_lang,
            # formality="more", # not supported by ZH
        )
    except deepl.DeepLException:
        raise
    except ValueError:
        raise
    else:
        # Revert the protected characters
        tstr = translated.text
        tstr = revert_protected(tstr, pairs)
        
        if post_processing:
            res = str_post_processing(tstr)
        else:
            res = tstr
        
        return res

def po_translate(
    lines: typing.List[str], 
    max_chars: int = 100,
    override: bool = False,
) -> typing.List[str]:
    """Translate the po files line by line"""
    # Clean the lines by striping the \n
    lines = [l.rstrip('\n') for l in lines]

    # The text file must be an empty line at the end
    if lines[-1] != "":
        lines.append("")

    output_lines = lines.copy()
    n_chars = 0

    for ln, line in enumerate(lines):
        # if the translated characters exceed the limit, stop
        if n_chars > max_chars:
            break

        # msgid is the source english text
        if not line.startswith("msgid "):
            continue
        
        # Process the lines between msgid and msgstr
        ln_start = ln
        for c, inner_line in enumerate(lines[ln:]):
            current_ln = ln_start + c
            if inner_line.startswith("msgstr "):
                ln_msgstr = current_ln
            if inner_line == "":
                ln_end = current_ln
                break

        msgid_lines = lines[ln_start:ln_msgstr]
        msgstr_lines = lines[ln_msgstr:ln_end]

        # Skip empty msgid (the po file identifier)
        if len(msgid_lines) == 1 and msgid_lines[0] == 'msgid ""':
            continue
            
        # if translated, skip， otherwise the result will be overwritten
        def is_translated(lines: typing.List[str]) -> bool:
            """Check if the msgstr is translated"""
            if len(lines) > 1:
                return True
            else:
                return lines[0] != 'msgstr ""'

        if is_translated(msgstr_lines) and not override:
            continue
            
        # convert to the oneliner string from multiple lines
        if len(msgid_lines) > 1:
            inp_str = "".join([i.strip('"') for i in msgid_lines[1:]])
        else:
            # get the string from double quotes
            inp_str = line.removeprefix('msgid "').removesuffix('"')

        # Do nothing to empty str
        if inp_str == "":
            continue

        try:
            translated = translate(inp_str)
        except Exception as exc:
            raise RuntimeError(f"Error when translate '{inp_str}'") from exc
        else:
            n_chars += len(inp_str)

        output_lines[ln_msgstr] = f'msgstr "{translated}"'

        if len(msgstr_lines) > 1:
            # if msgstr is multiple lines, remove the original lines
            # this will happend when override is True
            output_lines[ln_msgstr+1:ln_end] = [''] * (ln_end - ln_msgstr - 1)
            
    return output_lines
    
            
def deepl_status(info: str = "verbose") -> int:
    """Get the status of the deepl API"""
    import deepl
    token = get_env_deepl_token()
    if token is None:
        raise RuntimeError("Please set the 'DEEPL_TOKEN' environment variable")
    
    translator = deepl.Translator(token)
    
    usage = translator.get_usage()
    
    if info == "verbose":
        return usage
    elif info == "count":
        return usage.character.count
    elif info == "limit":
        return usage.character.limit
    elif info == "avail":
        return usage.character.limit - usage.character.count
    else:
        raise ValueError("Please set the correct parameter")