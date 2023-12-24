import pytest
from click.testing import CliRunner

from aiida_core_i18n.__main__ import cli

@pytest.mark.apicall
def test_i18n_cli_status():
    runner = CliRunner()
    
    result = runner.invoke(cli, ['status'])
    assert result.exit_code == 0

    for status in ["count", "limit", "verbose", "avail"]:
        result = runner.invoke(cli, ['status', '-p', status])
        assert result.exit_code == 0

@pytest.mark.apicall
def test_i18n_cli_translate():
    runner = CliRunner()
    
    result = runner.invoke(cli, ['translate', "--max-chars", "100", "--", "tests/statics/origin_text.txt"])

    assert result.exit_code == 0