import json

BASE_CONFIG_FILE = "res/base_config.json"

class Config:
    def __init__(self):
        base_config_file = open(BASE_CONFIG_FILE)

        self.base_config = json.load(base_config_file)

        base_config_file.close()

    def get_baseconfig(self):
        return self.base_config

def init():
    global config
    config = Config()