
import time
import logging

from Core.config_manager import ConfigManager
from Core.event_bus import EventBus
from Core.input_manager import InputManager


def main():
    config = ConfigManager()
    settings = config.load_config()

    logging.basicConfig(
        level=getattr(
            logging,
            settings.get("logging_level", "INFO").upper(),
            logging.INFO
        ),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    event_bus = EventBus()

    def handle_input(event):
        pass

    event_bus.subscribe("input_updated", handle_input)

    input_manager = InputManager(
        event_bus=event_bus,
        config_manager=config
    )

    event_bus.start()
    input_manager.start()

    logging.info("ROV Ground Control Station started")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Shutting down ROV Ground Control Station")

    finally:
        input_manager.stop()
        event_bus.stop()


if __name__ == "__main__":
    main()
