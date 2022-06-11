# -*- coding: UTF-8 -*-

import os

import can

"""
    This class implements the Bus interface provided by the python-can package.
    You can find the relevant documentation here:
        https://python-can.readthedocs.org/en/stable/

    Its main goal is to connect to the Vector interface, but it can also manage a virtual CAN interface
    on Linux for development purposes.
"""

class BUS(can.interface.Bus):
    def __init__(self) -> None:

        """
           Bring up 'socketcan' with 'vcan0' channel if environment value DEV is set,
           otherwise we connect to the VECTOR interface.

           (Make sure to register the app name in the Vector Hardware Configuration tool)
        """
        development_mode_enabled = os.environ.get('DEV', False)
        bustype = 'socketcan' if development_mode_enabled else 'vector'
        channel = 'vcan0' if development_mode_enabled else 0
        name = 'jfuzz' if development_mode_enabled else 'CANalyzer'

        super(self, BUS).__init__(
            name=name,
            bustype=bustype,
            channel=channel,
            bitrate=10000
        )
