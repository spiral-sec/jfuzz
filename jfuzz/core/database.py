# -*- coding: UTF-8 -*-

import os
from os import walk

import can
from cantools.database import load_file

"""
    This class implements the DBC parser from cantools, which sends back Messages that can be sent to the CAN bus
    with python-can
"""

class Database:
    def __init__(self, project_dir_path: str) -> None:
        self.files: [str] = []
        self.messages : [can.Message] = []
        self.nodes : [str] = []

        self.collect_dbc_files(project_dir_path)
        for file in self.files:
            self.parse(file)

    def collect_dbc_files(self, dir_path) -> None:
        sep = '/' if os.environ.get('DEV', False) else '\\'

        for root, _dirs, files in walk(dir_path):
            for file in files:
                if file.endswith('.dbc'):
                    new_file = root + sep + file
                    self.files.append(new_file)
        return None


    def parse(self, filepath: str) -> None:

        """
        :param filepath: path of .dbc file
        :return: Nothing
        """

        if cantools_db := load_file(filepath):
            for node in cantools_db.nodes:
                self.nodes.append(node.name)

            for msg in cantools_db.messages:
                print(f'msg to translate -> {msg}')
