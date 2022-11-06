import pytest

from aiida_core_i18n import str_pp

@pytest.mark.parametrize(
    ('input', 'expected'),
    [
        ("*POST*：创建一个 \"Dict \"对象，\"Dict \"对象", "*POST*：创建一个 ``Dict``对象， ``Dict``对象"),
        ("`AiidaApi', 继承`flask_restful.Api'。该类定义了由REST API提供的资源。", "``AiidaApi``, 继承 ``flask_restful.Api``。该类定义了由REST API提供的资源。"),
        ("`AiidaApi`，继承`flask_restful.Api`。该类定义了由REST API提供的资源。", "`AiidaApi`，继承 `flask_restful.Api`。该类定义了由REST API提供的资源。"),
        ("所有的Python内置类型都可以被Flask序列化（例如``int``、``float``、``str``等），而对于自定义类型的序列化，我们让你参考`Flask文档<http://flask.pocoo.org/docs/>`_。", "所有的Python内置类型都可以被Flask序列化（例如 ``int``、 ``float``、 ``str``等），而对于自定义类型的序列化，我们让你参考 `Flask文档<http://flask.pocoo.org/docs/>`_。"),
        ("参见 :py:mod:`aiida.plugins`中的API文档。", "参见 :py:mod:`aiida.plugins`中的API文档。")
    ]
)
def test_str_pp(input, expected):
    """test post process the string for code snippet"""
    got = str_pp(input)
    assert got == expected