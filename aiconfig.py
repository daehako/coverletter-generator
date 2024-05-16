import json

class AIConfig:
    def __init__(self, config_path):
        try:
            with open(config_path, 'r') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            print(f"Config file {config_path} not found.")
            self.config = {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the config file {config_path}.")
            self.config = {}

    def get(self, key, default=None):
        return self.config.get(key, default)