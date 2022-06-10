# -*- coding: UTF-8 -*-

"""
    This class implements the DBC parser from cantools, which sends back Messages that can be sent to the CAN bus
    with python-can
"""
from cantools import database


class Database:
    def __init__(self, filepath: str) -> None:
        self.__file = database.load_file(filepath)
        self.messages = self.__file.messages