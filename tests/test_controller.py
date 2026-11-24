
import pygame

from Core.controller import ControllerInput
from Core.profiles import ControllerProfile


def test_controller_initialization():
    controller = ControllerInput()
    assert controller.deadzone == 0.1
    assert controller.controller is None
    assert controller.connected is False


def test_apply_deadzone():
    controller = ControllerInput()

    assert controller.apply_deadzone(0.05) == 0.0
    assert controller.apply_deadzone(-0.05) == 0.0
    assert controller.apply_deadzone(0.5) == 0.5


def test_connect_no_controller(monkeypatch):
    controller = ControllerInput()

    monkeypatch.setattr("pygame.joystick.get_count", lambda *_args: 0)

    assert controller.connect() is False
    assert controller.connected is False


def test_connect_success(monkeypatch):
    controller = ControllerInput()

    class MockJoystick:
        def init(self):
            pass

    monkeypatch.setattr("pygame.joystick.get_count", lambda *_args: 1)
    monkeypatch.setattr(
        "pygame.joystick.Joystick",
        lambda index: MockJoystick()
    )

    assert controller.connect() is True
    assert controller.connected is True


def test_disconnect():
    controller = ControllerInput()

    class MockJoystick:
        def quit(self):
            pass

    controller.controller = MockJoystick()
    controller.connected = True

    controller.disconnect()

    assert controller.controller is None
    assert controller.connected is False


def test_update_reads_controller_inputs(monkeypatch):
    controller = ControllerInput()

    class MockJoystick:
        def get_init(self):
            return True

        def get_numaxes(self):
            return 2

        def get_axis(self, index):
            return [0.5, -0.5][index]

        def get_numbuttons(self):
            return 2

        def get_button(self, index):
            return [1, 0][index]

        def get_numhats(self):
            return 1

        def get_hat(self, index):
            return (0, 1)

    controller.controller = MockJoystick()
    controller.connected = True

    monkeypatch.setattr("pygame.event.pump", lambda *_args: None)
    monkeypatch.setattr("pygame.event.get", lambda *_args: [])

    result = controller.update()

    assert result["axes"] == [0.5, -0.5]
    assert result["buttons"] == [1, 0]
    assert result["hats"] == [(0, 1)]


def test_controller_hotplug_connect(monkeypatch):
    controller = ControllerInput()

    class MockEvent:
        type = pygame.JOYDEVICEADDED

    monkeypatch.setattr(
        "pygame.event.get",
        lambda *_args: [MockEvent()]
    )
    monkeypatch.setattr("pygame.event.pump", lambda *_args: None)
    monkeypatch.setattr("pygame.joystick.get_count", lambda *_args: 0)

    controller.update()

    assert controller.connected is False


def test_controller_hotplug_disconnect(monkeypatch):
    controller = ControllerInput()

    class MockJoystick:
        def get_instance_id(self):
            return 1

        def quit(self):
            pass

    class MockEvent:
        type = pygame.JOYDEVICEREMOVED
        instance_id = 1

    controller.controller = MockJoystick()
    controller.connected = True

    monkeypatch.setattr(
        "pygame.event.get",
        lambda *_args: [MockEvent()]
    )
    monkeypatch.setattr("pygame.event.pump", lambda *_args: None)

    controller.update()

    assert controller.controller is None
    assert controller.connected is False


def test_controller_uses_custom_profile():
    custom = {
        "name": "custom",
        "axes": {"forward": 1, "turn": 0},
        "buttons": {"arm": 0, "disarm": 1},
        "deadzone": 0.25
    }

    profile = ControllerProfile(custom)
    controller = ControllerInput(profile=profile)

    assert controller.deadzone == 0.25
    assert controller.apply_deadzone(0.2) == 0.0
    assert controller.apply_deadzone(0.5) == 0.5


def test_get_mapped_axes():
    controller = ControllerInput()

    axes = [0.5, -0.7]
    mapped = controller.get_mapped_axes(axes)

    assert mapped == {
        "forward": -0.7,
        "turn": 0.5
    }


def test_get_mapped_buttons():
    controller = ControllerInput()

    buttons = [1, 0]
    mapped = controller.get_mapped_buttons(buttons)

    assert mapped == {
        "arm": 1,
        "disarm": 0
    }
