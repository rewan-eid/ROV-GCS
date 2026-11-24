from Core.profiles import ControllerProfile


def test_default_profile():
    profile = ControllerProfile()

    assert profile.get_axis("forward") == 1
    assert profile.get_axis("turn") == 0
    assert profile.get_button("arm") == 0
    assert profile.get_button("disarm") == 1
    assert profile.get_deadzone() == 0.1


def test_custom_profile():
    custom = {
        "name": "custom",
        "axes": {"forward": 2, "turn": 3},
        "buttons": {"arm": 4, "disarm": 5},
        "deadzone": 0.2
    }

    profile = ControllerProfile(custom)

    assert profile.get_axis("forward") == 2
    assert profile.get_button("arm") == 4
    assert profile.get_deadzone() == 0.2


def test_unknown_action():
    profile = ControllerProfile()

    assert profile.get_axis("unknown") is None
    assert profile.get_button("unknown") is None