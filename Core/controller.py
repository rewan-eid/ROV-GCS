from Core.profiles import ControllerProfile
import pygame


class ControllerInput:
    def __init__(self, deadzone=None, profile=None):
        pygame.init()
        pygame.joystick.init()

        self.profile = profile or ControllerProfile()
        self.deadzone = (
            self.profile.get_deadzone()
            if deadzone is None
            else deadzone
        )

        self.controller = None
        self.connected = False

    def connect(self):
        pygame.joystick.quit()
        pygame.joystick.init()

        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            self.connected = True
            return True

        self.controller = None
        self.connected = False
        return False

    def disconnect(self):
        if self.controller is not None:
            self.controller.quit()

        self.controller = None
        self.connected = False

    def apply_deadzone(self, value):
        if abs(value) < self.deadzone:
            return 0.0
        return value

    def get_mapped_axes(self, axes):
        return {
            action: axes[index]
            for action, index in self.profile.profile["axes"].items()
            if isinstance(index, int) and 0 <= index < len(axes)
        }

    def get_mapped_buttons(self, buttons):
        return {
            action: buttons[index]
            for action, index in self.profile.profile["buttons"].items()
            if isinstance(index, int) and 0 <= index < len(buttons)
        }

    def update(self):
        pygame.event.pump()

        events = pygame.event.get([
            pygame.JOYDEVICEADDED,
            pygame.JOYDEVICEREMOVED
        ])

        for event in events:
            if event.type == pygame.JOYDEVICEADDED:
                if not self.connected:
                    self.connect()

            elif event.type == pygame.JOYDEVICEREMOVED:
                if self.controller is not None:
                    if self.controller.get_instance_id() == event.instance_id:
                        self.disconnect()

        if self.controller is None:
            return None

        if not self.controller.get_init():
            self.disconnect()
            return None

        axes = [
            self.apply_deadzone(self.controller.get_axis(i))
            for i in range(self.controller.get_numaxes())
        ]

        buttons = [
            self.controller.get_button(i)
            for i in range(self.controller.get_numbuttons())
        ]

        hats = [
            self.controller.get_hat(i)
            for i in range(self.controller.get_numhats())
        ]

        return {
            "axes": axes,
            "buttons": buttons,
            "hats": hats,
            "mapped_axes": self.get_mapped_axes(axes),
            "mapped_buttons": self.get_mapped_buttons(buttons)
        }