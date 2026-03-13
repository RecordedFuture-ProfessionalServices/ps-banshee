import json

import pytest
from typer.testing import CliRunner

from banshee.commands.cmd_classic_alerts import app

runner = CliRunner()

COMMAND = 'rules'


@pytest.mark.vcr
def test_ca_rules_no_args():
    result = runner.invoke(app, args=[COMMAND])
    assert result.exit_code == 0

    # We expect JSON output by default
    output = json.loads(result.output)
    assert len(output) > 0


@pytest.mark.vcr
def test_ca_rules_args_pretty():
    result = runner.invoke(app, args=[COMMAND, '-p'])
    assert result.exit_code == 0

    with pytest.raises(json.JSONDecodeError):
        json.loads(result.output)
