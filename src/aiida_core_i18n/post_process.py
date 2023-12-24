def str_post_processing(tstr: str) -> str:
    """deepl zh_CN has problem when translate the `` in CJK from English,
    this method will handle the process of it to render code snippet.
    """
    ## for `{content}` make sure a space in front
    #tstr = re.sub(r'(?:(?:(?<!^)(?<!\s)(?<!`)(?<!:))(`\w.*?`))', r' \1', tstr, flags=re.ASCII)
    
    ## r"请访问 ``话语论坛 <https://aiida.discourse.group> `__``。" -> r"请访问 `话语论坛 <https://aiida.discourse.group>`__。"
    #tstr = re.sub(r"``(.*?)\s+`__``", r"`\1`__ ", tstr, flags=re.ASCII)

    ## Strip the space in both ends, otherwise the next pp will be revert
    #tstr = tstr.strip()
    
    # The post processing squeeze the string to without space
    # The space is added in the revert_protected
    tstr = tstr.replace(" ", "")
    tstr = tstr.strip()

    return tstr