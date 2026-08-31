import pytest
import importlib


@pytest.mark.unit
def test_setting_reads_connection_string(monkeypatch):
    monkeypatch.setenv("CONNECTION_STRING", "mongodb://fake:27017")

    import app.core.config as config_module

    importlib.reload(config_module)

    assert config_module.settings.CONNECTION_STRING == "mongodb://fake:27017"


@pytest.mark.unit
def test_settings_project_name():
    import app.core.config as config_module

    assert config_module.settings.PROJECT_NAME == "Microservicio Analítica"
