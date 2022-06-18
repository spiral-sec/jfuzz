# -*- coding: UTF-8 -*-

import json
import os

CONFIG_PATH = os.getcwd() + '/fuzzer_config.json'

class Config(object):
    def __init__(self):
        self.settings = {
            'version': 0.1,

            'log_extension': '.asc',
            'log_name': 'jfuzz',

            'crc_regex_pattern': '\\d_[a-zA-Z]+_CRC',
            'crc_algorithm': 'CRC8',
        }


    def to_json(self):
        return json.dumps(self.settings, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def fetch(self, path: str = CONFIG_PATH):
        with open(path, 'w') as file:
            file.write(self.to_json())

    def dump(self, path: str = CONFIG_PATH):
        with open(path, 'r') as file:
            self.settings.update(json.loads(file.read()))

