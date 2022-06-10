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

class BUS(object):
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

        self.__internal = can.interface.Bus(
            name=name,
            bustype=bustype,
            channel=channel,
            preserve_timestamps=True,
            bitrate=1000000
        )


    """
        Sends one CAN message.

        Prefer send_many() for fuzzing.
    """
    def send_one(self, message: can.Message) -> None:
        try:
            self.__internal.send(message)
        except can.CanError:
            print(f'Error: could not send {message}')


    """
        Sends a range of generated messages.
    """
    def send_many(self, messages: [can.Message]) -> None:
        try:
            for message in messages:
                self.__internal.send(message)

        except:
            print('Unexpected exception')

