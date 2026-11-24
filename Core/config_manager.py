
import json
from pathlib import Path


class ConfigManager:

    def __init__(self):
        self.config_path = (
            Path(__file__).resolve().parent.parent
            / "config"
            / "settings.json"
        )

        self.settings = {}

    def load_config(self):
        with open(self.config_path, "r") as file:
            self.settings = json.load(file)

        return self.settings

    def get(self, key, default=None):
        return self.settings.get(key, default)
