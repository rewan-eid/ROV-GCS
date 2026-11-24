
DEFAULT_PROFILE = {
    "name": "default",
    "axes": {
        "forward": 1,
        "turn": 0
    },
    "buttons": {
        "arm": 0,
        "disarm": 1
    },
    "deadzone": 0.1
}


class ControllerProfile:
    def __init__(self, profile=None):
        self.profile = profile or DEFAULT_PROFILE.copy()

    def get_axis(self, action):
        return self.profile["axes"].get(action)

    def get_button(self, action):
        return self.profile["buttons"].get(action)

    def get_deadzone(self):
        return self.profile["deadzone"]
