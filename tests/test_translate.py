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
            "*POST* ：创建一个 ``Dict``对象，``Dict``对象",
        ),
        (
            "`AiidaApi', 继承`flask_restful.Api'。该类定义了由REST API提供的资源。", 
            "``AiidaApi``, 继承``flask_restful.Api``。该类定义了由REST API提供的资源。",
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
        r"This is ``this is a code block``",
        r"AiiDA is supported by the `MARVEL National Centre of Competence in Research`_, the `MaX European Centre of Excellence`_",
        r"The :meth:`Process.is_valid_cache <aiida.engine.processes.process.Process.is_valid_cache>` is where the ",
        r"As discussed in the :ref:`topic section <topics:provenance:caching:limitations>`",
        r"As discussed in the :py:ref:`topic section <topics:provenance:caching:limitations>`",
        r"This means that a :class:`~aiida.orm.nodes.process.workflow.workflow.WorkflowNode` will not be cached.",
        r"This is global_design",
        r"THTH_design_1",
        r"Termi workflow", r"Termi Workflow",
        r"Termi Engine", r"Termi engine",
        r"Termi entry point", r"Termi Entry Point",
        r"Termi Node", r"Termi node",
        r"Mini_spec", r"Mini_Spec",
        r"import", r"Import", r"imports", r"Imports",
        r"{ref}`how-to:use:me`",
        r"|aiida-core|: The main Python package",
        r"During \"full\" maintenance",
        r"`aiida-core` is protected.",
        r"`aiida core` is protected.",
        r"Termi schema", r"Termi Schema",
        r"`aiida` and `core` is protected.",
        r"The process function is protected.",
        r"The processes is protected.",
        r"The 'quote' is protected.",
        r"The verdi is protected.",
        r"builder is protected.",
        r"The double colon :: is protected.",
    ]
)
def test_replace_protect(input: str):
    from aiida_core_i18n import replace_protected, revert_protected
    
    pstr, pairs = replace_protected(input)
    print(pstr)
    
    # by check there are things in the examples that require protection
    assert len(pairs) > 0, f"Nothing to protect in {input}"

    # Add prefix and suffix to the string to mock the translation
    pstr = " IGOTTRANSASWELL " + pstr + " IAMTRANS"
    pstr = revert_protected(pstr, pairs, lang="DE")

    assert pstr == f" IGOTTRANSASWELL {input} IAMTRANS"

@pytest.mark.parametrize(
    "input",
    [
        r"The inputs and output that we define are essentially determined by the sub process that the work chain will be running. Since the ``ArithmeticAddCalculation`` requires the inputs ``x`` and ``y``, and produces the ``sum`` as output, we `mirror` those in the specification of the work chain, otherwise we wouldn't be able to pass the necessary inputs. Finally, we define the logical outline, which if you look closely, resembles the logical flow chart presented in :numref:`workflow-error-handling-flow-loop` a lot. We start by *setting up* the work chain and then enter a loop: *while* the subprocess has not yet finished successfully *and* we haven't exceeded the maximum number of iterations, we *run* another instance of the process and then *inspect* the results. The while conditions are implemented in the ``should_run_process`` outline step. When the process finishes successfully or we have to abandon, we report the *results*. Now unlike with normal work chain implementations, we *do not* have to implement these outline steps ourselves. They have already been implemented by the ``BaseRestartWorkChain`` so that we don't have to. This is why the base restart work chain is so useful, as it saves us from writing and repeating a lot of `boilerplate code <https://en.wikipedia.org/wiki/Boilerplate_code>`__.",
        r"AiiDA is supported by the `MARVEL National Centre of Competence in Research`_, the `MaX European Centre of Excellence`_",
    ]
)
def test_a_huge_nested_replace_protect(input: str):
    from aiida_core_i18n import replace_protected, revert_protected
    
    pstr, pairs = replace_protected(input)
    print(pstr)
    
    # by check there are things in the examples that require protection
    assert len(pairs) > 0, f"Nothing to protect in {input}"

    # Add prefix and suffix to the string to mock the translation
    pstr = " IGOTTRANSASWELL " + pstr + " IAMTRANS"
    pstr = revert_protected(pstr, pairs, lang="DE")

    assert pstr == f" IGOTTRANSASWELL {input} IAMTRANS"
    
@pytest.mark.parametrize(
    "input",
    [
        r"`aiida-core ` is not protected."
        r"the 'quote without space' is not protected.",
    ]
)
def test_replace_protect_not(input: str):
    from aiida_core_i18n import replace_protected, revert_protected

    pstr, pairs = replace_protected(input)

    # by check there are things in the examples that require protection
    with pytest.raises(AssertionError):
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
        (r"它将 API 与 ``flask.Flask``（即代表网络应用的 Flask 基本类）的实例耦合。这样，应用程序就配置好了，如果需要，还可以连接起来。", r"它将 API 与 ``flask.Flask`` (即代表网络应用的 Flask 基本类)的实例耦合。这样，应用程序就配置好了，如果需要，还可以连接起来。"),
        (r"Two space here  Make no sence", r"Two space here Make no sence"),
        (r"这种关系在*db_dblinks*表中有记录。", r"这种关系在 *db_dblinks* 表中有记录。"),
        (r"这种关系1在*db_dblinks* 表中有记录。", r"这种关系1在 *db_dblinks* 表中有记录。"),
        (r"这种关系1.1在 *db_dblinks*表中有记录。", r"这种关系1.1在 *db_dblinks* 表中有记录。"),
        (r"这种关系1.2在  *db_dblinks*表中有记录。", r"这种关系1.2在 *db_dblinks* 表中有记录。"),
        (r"这种关系2在**db_dblinks**表中有记录。", r"这种关系2在 **db_dblinks** 表中有记录。"),
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
    from aiida_core_i18n.deepl_api import deepl_status

    # may not be enough for the whole file if so, fail the test
    # We need go and maybe change
    max_chars = 1000
    
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
