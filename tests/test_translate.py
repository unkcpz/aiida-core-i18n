import pytest
import pathlib

from aiida_core_i18n import str_post_processing, po_translate

@pytest.fixture(scope="function")
def static_path() -> pathlib.Path:
    """The path of this file"""
    return pathlib.Path(__file__).parent.resolve()

@pytest.mark.parametrize(
    ('input', 'expected'),
    [
        ("*POST*：创建一个 \"Dict \"对象，\"Dict \"对象", "*POST*：创建一个 ``Dict``对象， ``Dict``对象"),
        ("`AiidaApi', 继承`flask_restful.Api'。该类定义了由REST API提供的资源。", "``AiidaApi``, 继承 ``flask_restful.Api``。该类定义了由REST API提供的资源。"),
        ("`AiidaApi`，继承`flask_restful.Api`。该类定义了由REST API提供的资源。", "`AiidaApi`，继承 `flask_restful.Api`。该类定义了由REST API提供的资源。"),
        ("所有的Python内置类型都可以被Flask序列化（例如``int``、``float``、``str``等），而对于自定义类型的序列化，我们让你参考`Flask文档<http://flask.pocoo.org/docs/>`_。", "所有的Python内置类型都可以被Flask序列化（例如 ``int``、 ``float``、 ``str``等），而对于自定义类型的序列化，我们让你参考 `Flask文档<http://flask.pocoo.org/docs/>`_。"),
        ("参见 :py:mod:`aiida.plugins`中的API文档。", "参见 :py:mod:`aiida.plugins`中的API文档。"),
    ]
)
def test_str_post_processing(input: str, expected: str):
    """test post process the string for code snippet"""
    got = str_post_processing(input)
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
    lines = pot_str.splitlines()
    
    translated_lines = po_translate(lines)
    file_regression.check('\n'.join(translated_lines))
    
@pytest.mark.parametrize("override", [True, False])
def test_po_translate_override(pot_str, file_regression, monkeypatch, override: bool):
    """Monkey patch the translate function to return the same string
    In order to test the flow of po_translate
    """
    monkeypatch.setattr("aiida_core_i18n.translate", lambda x: x)
    
    lines = pot_str.splitlines()
    
    translated_lines = po_translate(lines, override=override)
    file_regression.check('\n'.join(translated_lines))

@pytest.mark.parametrize("max_chars", [3, 20, 100])
def test_po_translate_max_chars(pot_str, file_regression, monkeypatch, max_chars: int):
    """Monkey patch the translate function to return the same string"""

    monkeypatch.setattr("aiida_core_i18n.translate", lambda x: x)

    lines = pot_str.splitlines()

    translated_lines = po_translate(lines, max_chars=max_chars)
    file_regression.check('\n'.join(translated_lines))