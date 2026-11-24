
import time
import threading

from Core.input_manager import InputManager
from Core.event_bus import EventBus
from Core.config_manager import ConfigManager


def test_input_manager_initialization():
    manager = InputManager(input_rate=50)

    assert manager.input_rate == 50
    assert manager.running is False


def test_input_manager_start_stop():
    manager = InputManager(input_rate=50)

    manager.start()
    time.sleep(0.1)

    assert manager.running is True

    manager.stop()

    assert manager.running is False


def test_input_manager_receives_mapped_controller_data():
    manager = InputManager(input_rate=50)

    expected_controller_data = {
        "axes": [0.5, -0.7],
        "buttons": [1, 0],
        "hats": [],
        "mapped_axes": {
            "forward": -0.7,
            "turn": 0.5
        },
        "mapped_buttons": {
            "arm": 1,
            "disarm": 0
        }
    }

    class MockKeyboard:
        def update(self):
            return {"W", "A"}

    class MockController:
        def update(self):
            return expected_controller_data

    manager.keyboard = MockKeyboard()
    manager.controller = MockController()

    manager.start()

    try:
        received_data = None

        for _ in range(100):
            received_data = manager.get_input()

            if received_data.get("controller") == expected_controller_data:
                break

            time.sleep(0.01)

        assert set(received_data["keyboard"]) == {"W", "A"}
        assert received_data["controller"] == expected_controller_data

        assert received_data["controller"]["mapped_axes"]["forward"] == -0.7
        assert received_data["controller"]["mapped_buttons"]["arm"] == 1

    finally:
        manager.stop()


def test_input_manager_publishes_to_event_bus():
    event_bus = EventBus()
    manager = InputManager(input_rate=50, event_bus=event_bus)

    received_events = []
    event_received = threading.Event()

    class MockKeyboard:
        def update(self):
            return {"W"}

    class MockController:
        def update(self):
            return {
                "axes": [0.5],
                "buttons": [1],
                "hats": [],
                "mapped_axes": {"forward": 0.5},
                "mapped_buttons": {"arm": 1}
            }

    def handle_input(event):
        received_events.append(event)
        event_received.set()

    manager.keyboard = MockKeyboard()
    manager.controller = MockController()

    event_bus.subscribe("input_updated", handle_input)

    event_bus.start()
    manager.start()

    try:
        assert event_received.wait(timeout=2)

        assert received_events[0].event_type == "input_updated"
        assert received_events[0].data["keyboard"] == ["W"]
        assert received_events[0].data["controller"]["mapped_axes"]["forward"] == 0.5

    finally:
        manager.stop()
        event_bus.stop()


def test_input_manager_loads_config_settings():
    config = ConfigManager()
    manager = InputManager(config_manager=config)

    assert manager.input_rate == 50
    assert manager.controller.deadzone == 0.1


def test_input_manager_manual_rate_overrides_config():
    config = ConfigManager()
    manager = InputManager(
        input_rate=25,
        config_manager=config
    )

    assert manager.input_rate == 25
    assert manager.controller.deadzone == 0.1
