import os
import deepl

def get_env_deepl_token() -> str:
    """Get the deepl token from the environment variable"""
    return os.environ.get("DEEPL_TOKEN")
            
def deepl_status(info: str = "verbose") -> int:
    """Get the status of the deepl API"""
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