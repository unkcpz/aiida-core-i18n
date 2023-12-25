import re

def str_post_processing(raw_str: str) -> str:
    """deepl zh_CN has problem when translate the `` in CJK from English,
    this method will handle the process of it to render code snippet.
    """
    # if `{any_str}' -> ``{any_str}``
    tstr = re.sub(r"""(?:(?:(?<!`)(?<!:))`(\w.*?)')""", r'``\1``', raw_str, flags=re.ASCII)
    
    # if \" {any_str} \" -> ``{any_str}``
    tstr = re.sub(r'(?<!\w)\"(.*?)\"', lambda m: f"``{m.group(1).strip()}``", tstr, flags=re.ASCII)
    
    # for `{content}` make sure a space in front
    tstr = re.sub(r'(?:(?:(?<!^)(?<!\s)(?<!`)(?<!:))(`\w.*?`))', r' \1', tstr, flags=re.ASCII)
    
    ## for ``{content}`` make sure a space in front
    #tstr = re.sub(r'(?:(?:(?<!^)(?<!\s)(?<!`))(``\w.*?``))', r' \1', tstr, flags=re.ASCII)

    # r"请访问 ``话语论坛 <https://aiida.discourse.group> `__``。" -> r"请访问 `话语论坛 <https://aiida.discourse.group>`__。"
    tstr = re.sub(r"``(.*?)\s+`__``", r"`\1`__ ", tstr, flags=re.ASCII)

    # fix issue 102
    tstr = tstr.replace("``（", "`` （")

    # Strip the space in both ends, otherwise the next pp will be revert
    tstr = tstr.strip()

    return tstr