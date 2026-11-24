
from Core.config_manager import ConfigManager


def test_load_config():
    manager = ConfigManager()

    settings = manager.load_config()

    assert settings["input_rate"] == 50
    assert settings["deadzone"] == 0.1
    assert settings["window_title"] == "ROV Ground Control Station"


def test_get_setting():
    manager = ConfigManager()
    manager.load_config()

    assert manager.get("input_rate") == 50
    assert manager.get("unknown_setting", 100) == 100
