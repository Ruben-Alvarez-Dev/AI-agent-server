# Configuration Loader

import json
import os

class ConfigLoader:
    _instance = None

    def __new__(cls, config_path='src/config/configuration.json'):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance.load_config(config_path)
        return cls._instance

    def load_config(self, config_path: str):
        """
        Loads the configuration from the specified JSON file.
        """
        print(f"Loading configuration from '{config_path}'...")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
                print("Configuration loaded successfully.")
            else:
                print(f"Warning: Configuration file not found at '{config_path}'.")
                self.config = {}
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading configuration: {e}")
            self.config = {}

    def get(self, key, default=None):
        """
        Retrieves a value from the configuration.
        """
        return self.config.get(key, default)

# Singleton instance
config = ConfigLoader()
