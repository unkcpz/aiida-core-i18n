import re

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