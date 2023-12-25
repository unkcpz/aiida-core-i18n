import typing
import deepl

from aiida_core_i18n.protection import replace_protected, revert_protected, met_skip_rule
from aiida_core_i18n.deepl_api import get_env_deepl_token
from aiida_core_i18n.post_process import str_post_processing


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

        if post_processing:
            tstr = str_post_processing(tstr)
        else:
            tstr = tstr

        # This should be after the post processing
        # It is safe since that exactly we want to protect, not only
        # protect the string from translation, but also protect it from the post processing.
        # otherwise the post processing may change the string.
        tstr = revert_protected(tstr, pairs)

        # lstrip the space in front of the string
        # but need to add a space in front of the line if it is a :meth:/class:/ref: string
        tstr = tstr.lstrip()
        for prefix in [":meth:", ":class:", ":ref:", ":py:"]:
            if tstr.startswith(prefix):
                tstr = " " + tstr
                break
        
        return tstr

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
    