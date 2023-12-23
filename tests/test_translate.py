import pytest
import pathlib
from collections import namedtuple

from aiida_core_i18n import str_post_processing, po_translate, translate

@pytest.fixture(scope="function")
def static_path() -> pathlib.Path:
    """The path of this file"""
    return pathlib.Path(__file__).parent.resolve()

@pytest.mark.parametrize(
    ('input', 'expected'),
    [
        (
            "*POST*：创建一个 \"Dict \"对象，\"Dict \"对象", 
            "*POST*：创建一个 ``Dict``对象，``Dict``对象",
        ),
        (
            "`AiidaApi', 继承`flask_restful.Api'。该类定义了由REST API提供的资源。", 
            "``AiidaApi``, 继承``flask_restful.Api``。该类定义了由REST API提供的资源。",
        ),
        (
            "`AiidaApi`，继承`flask_restful.Api`。该类定义了由REST API提供的资源。", 
            "`AiidaApi`，继承 `flask_restful.Api`。该类定义了由REST API提供的资源。",
        ),
        (
            "所有的Python内置类型都可以被Flask序列化（例如``int``、``float``、``str``等），而对于自定义类型的序列化，我们让你参考`Flask文档<http://flask.pocoo.org/docs/>`_。", 
            "所有的Python内置类型都可以被Flask序列化（例如``int``、``float``、``str``等），而对于自定义类型的序列化，我们让你参考 `Flask文档<http://flask.pocoo.org/docs/>`_。",
        ),
        (
            "参见 :py:mod:`aiida.plugins`中的API文档。", 
            "参见 :py:mod:`aiida.plugins`中的API文档。",
        ),
    ]
)
def test_str_post_processing_legacy(input: str, expected: str):
    """test post process the string for code snippet"""
    got = str_post_processing(input)
    assert got == expected

    # apply the post processing again should not change the string
    # For the cases like adding space
    got = str_post_processing(got)
    assert got == expected

@pytest.mark.parametrize(
    "input",
    [
        r"``this is a code block``",
        r"AiiDA is supported by the `MARVEL National Centre of Competence in Research`_, the `MaX European Centre of Excellence`_",
        r"The :meth:`Process.is_valid_cache <aiida.engine.processes.process.Process.is_valid_cache>` is where the ",
        r"As discussed in the :ref:`topic section <topics:provenance:caching:limitations>`",
        r"This means that a :class:`~aiida.orm.nodes.process.workflow.workflow.WorkflowNode` will not be cached.",
        r"global_design",
        r"THTH_design_1",
    ]
)
def test_replace_protect(input: str):
    from aiida_core_i18n import replace_protected, revert_protected
    
    pstr, pairs = replace_protected(input)
    
    # by check there are things in the examples that require protection
    assert len(pairs) > 0, f"Nothing to protect in {input}"

    # Add prefix and suffix to the string to mock the translation
    pstr = " IGOTTRANSASWELL " + pstr + " IAMTRANS"
    pstr = revert_protected(pstr, pairs, lang="DE")
    
    assert pstr == f" IGOTTRANSASWELL {input} IAMTRANS"
    

# new test_str_post_processing where the en_source is recorded with the date.
@pytest.mark.parametrize(
    ('input', 'expected'),
    [
        (r"请访问 ``话语论坛 <https://aiida.discourse.group> `__``。", r"请访问 `话语论坛 <https://aiida.discourse.group>`__ 。"),
    ]
)
def test_str_post_processing(input: str, expected: str):
    """test post process the string for code snippet"""
    got = str_post_processing(input)
    assert got == expected 

    # apply the post processing again should not change the string
    
@pytest.mark.parametrize(
    ('input', 'expected'),
    [
        (r"Martin        Uhrin, It is a great day, Computational Materials Science **187**, 110086 (2021); DOI: `10.1016/j.commatsci.2020.110086 <https://doi.org/10.1016/j.commatsci.2020.110086>`_", r"Martin        Uhrin, It is a great day, Computational Materials Science **187**, 110086 (2021); DOI: `10.1016/j.commatsci.2020.110086 <https://doi.org/10.1016/j.commatsci.2020.110086>`_"),
    ]
)
def test_met_skip_rule(input: str, expected: str, monkeypatch):
    """Test the skip rule by translate, the deepl translate function is monkey patched to return a dummy string
    """
    # The return value should contain the `text` attribute
    monkeypatch.setattr("deepl.Translator.translate_text", lambda *args, **kwargs: namedtuple("Dummy", ["text"])("YOUSHALLNOTPASS"))

    got = translate(input)
    assert got == expected

@pytest.fixture(scope="function")
def pot_str(static_path: pathlib.Path) -> str:
    """Read the po file from statics"""
    with open(static_path / "statics" / "origin_text.txt", "r") as fh:
        s = fh.read()
    return s

@pytest.mark.apicall
def test_po_translate_default(pot_str, file_regression):
    """The actuall process of po file
    This consumes ~ 500 characters of deepl API
    """
    from aiida_core_i18n import deepl_status

    # may not be enough for the whole file if so, fail the test
    # We need go and maybe change
    max_chars = 500
    
    # Get initial count
    i_count = deepl_status("count")
    
    lines = pot_str.splitlines()
    
    translated_lines = po_translate(lines, max_chars)
    f_count = deepl_status("count")
    used = f_count - i_count

    if not used < max_chars:
        pytest.fail(f"Used {used} characters, more than the max_chars {max_chars}")
    
    print(f"Translated {used} characters in this test session")

    file_regression.check('\n'.join(translated_lines))
    
@pytest.mark.parametrize("override", [True, False])
def test_po_translate_override(pot_str, file_regression, monkeypatch, override: bool):
    """Monkey patch the translate function to return the same string
    In order to test the flow of po_translate
    """
    monkeypatch.setattr("aiida_core_i18n.translate", lambda x: x)
    
    lines = pot_str.splitlines()
    
    translated_lines = po_translate(lines, override=override, max_chars=500)
    file_regression.check('\n'.join(translated_lines))

@pytest.mark.parametrize("max_chars", [3, 20, 100, 500])
def test_po_translate_max_chars(pot_str, file_regression, monkeypatch, max_chars: int):
    """Monkey patch the translate function to return the same string"""

    monkeypatch.setattr("aiida_core_i18n.translate", lambda x: x)

    lines = pot_str.splitlines()

    translated_lines = po_translate(lines, max_chars=max_chars)
    file_regression.check('\n'.join(translated_lines))

def test_po_translate_raise_exception_when_no_auth_key(pot_str, monkeypatch):
    """Test the exception when no auth key"""
    monkeypatch.setattr("aiida_core_i18n.get_env_deepl_token", lambda: None)

    with pytest.raises(Exception):
        po_translate(pot_str.splitlines())
