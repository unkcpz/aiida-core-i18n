import re
import typing as t
import hashlib

def met_skip_rule(inp_str: str) -> bool:
    """The rule when met, skip the translation of the entire string
    """
    # if string is a citation, skip (container link to a doi url)
    # e.g. Martin        Uhrin, It is a great day, Computational Materials Science **187**, 110086 (2021); DOI: `10.1016/j.commatsci.2020.110086 <https://doi.org/10.1016/j.commatsci.2020.110086>`_
    if re.match(r".*DOI: `.*? <https://doi.org/.*?>`_.*?", inp_str):
        return True
    
    return False

def str2hash(inp_str: str) -> str:
    """Convert the string to hash and keep 8 digits (capitalize)"""
    return hashlib.md5(inp_str.encode()).hexdigest()[:8].upper()

code_snippet_protect_list = [
    (r"(?:(?:(?<!`)(?<!:))(`\w.*?`_))", True), # 1
    (r"(?:(?:(?<!`)(?<!:))(:py:.*?:`.*?`))", True), # 2
    (r"(?:(?:(?<!`)(?<!:))(:meth:`.*?`))", True), # 2
    (r"(?:(?:(?<!`)(?<!:))(:class:`.*?`))", True), # 3
    (r"(?:(?:(?<!`)(?<!:))(:ref:`.*?`))", True), # 4
    (r"(?:(?:(?<!`)(?<!:))({ref}`.*?`))", True), # 5
]

# 1
# I have "`text1`_, `othertext2`_"
# -> "hash(`text1`_), hash(`othertext2`_)" 
# using regex to do it
# I also want to output the pairs of the hash and the original text
# so I can revert it back later
# I use a dict to store the pairs

# 2 - 4
# For string contains part start with :meth:, :class:, :ref:
# I want to protect the inline code snippet in the string
# e.g. :meth:`ProcessNodeCaching.is_valid_cache <aiida.orm.nodes.process.process.ProcessNodeCaching.is_valid_cache>` 调用
# 11
# For string contains ``text`` I want to protect it as well
    
# 21
# For string contains text_textp I want to protect it as well
# Don't add a space in front

terminology_protect_list = [
    (r"(?:(?:(?<!`)(?<!:))(``.*?``))", False), # 11
    (r"(?:(?:(?<!`)(?<!:))(\w+[-_]\w+))", False), # 21
    (r"(?:(?:(?<!`)(?<!:))([eE]ngine))", False), # 101
    (r"(?:(?:(?<!`)(?<!:))([wW]orkflow))", False), # 102
    (r"(?:(?:(?<!`)(?<!:))([nN]ode))", False), # 103
    (r"(?:(?:(?<!`)(?<!:))([eE]ntry\s+[pP]oint))", False), # 104
    (r"(?:(?:(?<!`)(?<!:))([pP]rovenance))", False), # 105
    (r"(?:(?:(?<!`)(?<!:))([pP]rovenance\s+[gG]raph))", False), # 106
    (r"(?:(?:(?<!`)(?<!:))([iI]mport[s]?))", False), # 107
]
    

def replace_protected(pstr: str) -> t.Tuple[str, dict[str, str]]:
    """Replace the protected characters"""
    pairs = {}
    
    for finder in code_snippet_protect_list + terminology_protect_list:
        space_in_front = finder[1]
        for m in re.finditer(finder[0], pstr, flags=re.ASCII):
            origin = m.group(1)
            gaurd = f"{str2hash(origin)}"
            pstr = pstr.replace(f"{origin}", gaurd)
            pairs[origin] = (gaurd, space_in_front)
    
    return pstr, pairs

def revert_protected(pstr: str, pairs: dict, lang: str="ZH") -> str:
    """Revert the protected characters"""
    for origin, (gaurd, space_in_front) in pairs.items():
        if lang == "ZH" and space_in_front:
            # Add a space in front if string start with :meth: like ":meth: {context}" -> "_space:meth: {context}"
            origin = " " + origin
        
        pstr = pstr.replace(gaurd, origin)
    
    return pstr