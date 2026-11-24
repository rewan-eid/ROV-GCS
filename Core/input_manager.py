
import threading
import time

from Core.keyboard import KeyboardInput
from Core.controller import ControllerInput
from Core.events import Event


class InputManager:
    def __init__(
        self,
        input_rate=None,
        event_bus=None,
        config_manager=None
    ):
        self.config_manager = config_manager

        settings = {}
        if self.config_manager is not None:
            settings = self.config_manager.load_config()

        self.input_rate = (
            input_rate
            if input_rate is not None
            else settings.get("input_rate", 50)
        )

        self.keyboard = KeyboardInput()
        self.controller = ControllerInput(
            deadzone=settings.get("deadzone")
        )

        self.event_bus = event_bus

        self.running = False
        self.thread = None

        self.latest_input = {}
        self.lock = threading.Lock()

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(
            target=self._input_loop,
            daemon=True
        )
        self.thread.start()

    def stop(self):
        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=2)

    def _input_loop(self):
        interval = 1.0 / self.input_rate

        while self.running:
            start_time = time.perf_counter()

            keyboard_data = self.keyboard.update()
            controller_data = self.controller.update()

            data = {
                "keyboard": list(keyboard_data),
                "controller": controller_data
            }

            with self.lock:
                self.latest_input = data

            if self.event_bus is not None:
                event = Event(
                    event_type="input_updated",
                    data=data.copy()
                )
                self.event_bus.publish(event)

            elapsed = time.perf_counter() - start_time
            time.sleep(max(0, interval - elapsed))

    def get_input(self):
        with self.lock:
            return self.latest_input.copy()
