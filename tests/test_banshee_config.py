import pytest
from psengine.config import Config, get_config
from pydantic import ValidationError

from banshee.app_config import BansheeConfig

# ---------------------------------------------------------------------------
# BansheeConfig field: sandbox_choice
# ---------------------------------------------------------------------------


def test_sandbox_choice_default_is_eu(monkeypatch):
    monkeypatch.delenv('RF_SANDBOX_CHOICE', raising=False)
    cfg = BansheeConfig(rf_token=None, app_id='test/1.0.0')
    assert cfg.sandbox_choice == 'eu'


def test_sandbox_choice_reads_from_env(monkeypatch):
    monkeypatch.setenv('RF_SANDBOX_CHOICE', 'usa')
    cfg = BansheeConfig(rf_token=None, app_id='test/1.0.0')
    assert cfg.sandbox_choice == 'usa'


def test_sandbox_choice_all_valid_regions(monkeypatch):
    for region in ('eu', 'usa', 'apj', 'public', 'private'):
        monkeypatch.delenv('RF_SANDBOX_CHOICE', raising=False)
        cfg = BansheeConfig(rf_token=None, app_id='test/1.0.0', sandbox_choice=region)
        assert cfg.sandbox_choice == region


def test_sandbox_choice_normalises_uppercase_env(monkeypatch):
    monkeypatch.setenv('RF_SANDBOX_CHOICE', 'EU')
    cfg = BansheeConfig(rf_token=None, app_id='test/1.0.0')
    assert cfg.sandbox_choice == 'eu'


def test_sandbox_choice_normalises_uppercase_kwarg(monkeypatch):
    monkeypatch.delenv('RF_SANDBOX_CHOICE', raising=False)
    cfg = BansheeConfig(rf_token=None, app_id='test/1.0.0', sandbox_choice='APJ')
    assert cfg.sandbox_choice == 'apj'


def test_sandbox_choice_invalid_raises_validation_error(monkeypatch):
    monkeypatch.setenv('RF_SANDBOX_CHOICE', 'xyz')
    with pytest.raises(ValidationError):
        BansheeConfig(rf_token=None, app_id='test/1.0.0')


def test_sandbox_choice_invalid_kwarg_raises_validation_error(monkeypatch):
    monkeypatch.delenv('RF_SANDBOX_CHOICE', raising=False)
    with pytest.raises(ValidationError):
        BansheeConfig(rf_token=None, app_id='test/1.0.0', sandbox_choice='nope')


# ---------------------------------------------------------------------------
# get_config() returns BansheeConfig after Config.init(config_class=BansheeConfig)
# ---------------------------------------------------------------------------


def test_get_config_returns_banshee_config_instance(monkeypatch):
    monkeypatch.delenv('RF_SANDBOX_CHOICE', raising=False)
    Config.init(config_class=BansheeConfig, rf_token=None, app_id='test/1.0.0')
    cfg = get_config()
    assert isinstance(cfg, BansheeConfig)
