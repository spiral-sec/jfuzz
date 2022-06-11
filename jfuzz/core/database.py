# -*- coding: UTF-8 -*-

import os
from os import walk

import cantools
from cantools.database import load_file

"""
    This class implements the DBC parser from cantools, which sends back Messages that can be sent to the CAN bus
    with python-can
"""

class Database:
    def __init__(self, project_dir_path: str) -> None:
        self.files: [str] = []
        self.messages = []
        self.database: cantools.database.Database = cantools.database.Database()

        self.collect_dbc_files(project_dir_path)
        for file in self.files:
            self.database.add_dbc_file(file, encoding='cp1252')

    def collect_dbc_files(self, dir_path) -> None:
        sep = '/' if os.environ.get('DEV', False) else '\\'

        for root, _dirs, files in walk(dir_path):
            for file in files:
                if file.endswith('.dbc'):
                    new_file = root + sep + file
                    self.files.append(new_file)
        return None
