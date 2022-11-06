import pytest

from aiida_core_i18n import str_pp, po_translate

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
def test_str_pp(input, expected):
    """test post process the string for code snippet"""
    got = str_pp(input)
    assert got == expected
    
    
PO_STR = """# SOME DESCRIPTIVE TITLE.
# Copyright (C) 2014-2020, ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE (Theory and Simulation of Materials (THEOS) and National Centre for Computational Design and Discovery of Novel Materials (NCCR MARVEL)), Switzerland and ROBERT BOSCH LLC, USA. All rights reserved
# This file is distributed under the same license as the AiiDA package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
# 
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: AiiDA 2.0\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2022-11-03 14:17+0000\n"
"PO-Revision-Date: 2022-11-03 14:19+0000\n"
"Language-Team: Chinese (China) (https://www.transifex.com/aiidateam/teams/98967/zh_CN/)\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Language: zh_CN\n"
"Plural-Forms: nplurals=1; plural=0;\n"

#: ../../source/internals/engine.rst:5
msgid "Engine"
msgstr "引擎（已翻译）"

#: ../../source/internals/engine.rst:5
msgid "Engine"
msgstr ""

#: ../../source/internals/engine.rst:38
msgid "The ``WorkflowNode`` example"
msgstr ""

#: ../../source/internals/engine.rst:19
msgid ""
"There are several methods which the internal classes of AiiDA use to control"
" the caching mechanism:"
msgstr ""
"""

def test_po_translate(data_regression):
    """The actuall process of po file"""
    lines = PO_STR.splitlines()
    
    translated_lines = po_translate(lines)
    data_regression.check(translated_lines)
    