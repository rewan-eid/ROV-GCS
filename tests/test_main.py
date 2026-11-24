
from unittest.mock import MagicMock

import main


def test_main_startup_and_shutdown(monkeypatch):
    mock_config = MagicMock()
    mock_config.load_config.return_value = {
        "input_rate": 50,
        "deadzone": 0.1,
        "logging_level": "INFO"
    }

    mock_event_bus = MagicMock()
    mock_input_manager = MagicMock()

    monkeypatch.setattr(
        main,
        "ConfigManager",
        lambda: mock_config
    )

    monkeypatch.setattr(
        main,
        "EventBus",
        lambda: mock_event_bus
    )

    monkeypatch.setattr(
        main,
        "InputManager",
        lambda **kwargs: mock_input_manager
    )

    def stop_program(_):
        raise KeyboardInterrupt

    monkeypatch.setattr(main.time, "sleep", stop_program)

    main.main()

    mock_event_bus.start.assert_called_once()
    mock_input_manager.start.assert_called_once()
    mock_input_manager.stop.assert_called_once()
    mock_event_bus.stop.assert_called_once()


