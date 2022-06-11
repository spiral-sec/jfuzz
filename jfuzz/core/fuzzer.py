# -*- coding: UTF-8 -*-
import os
import random

import can
import cantools
from cantools.database import Message

from jfuzz.core.database import Database


class Fuzzer:
    def __init__(self):

        """
           Bring up 'socketcan' with 'vcan0' channel if environment value DEV is set,
           otherwise we connect to the VECTOR interface.

           (Make sure to register the app name in the Vector Hardware Configuration tool)
        """
        development_mode_enabled = os.environ.get('DEV', False)
        bustype = 'socketcan' if development_mode_enabled else 'vector'
        channel = 'vcan0' if development_mode_enabled else 0
        name = 'jfuzz' if development_mode_enabled else 'CANalyzer'

        print(f'[+] Building {bustype} interface... -- dev mode: {development_mode_enabled}')

        self.bus = can.interface.Bus(
            name=name,
            bustype=bustype,
            channel=channel,
            bitrate=10000
        )


    def setup_signals(self, signals: [cantools.database.Signal]) -> dict[str, any]:
        names : [str]= []
        values : [any] = []

        for s in signals:
            names.append(s.name)

            print(f'name: {s.name}')
            print(f's.choices: {s.choices}')
            print(f's.minimum: {s.minimum}')
            print(f's.maximum: {s.maximum}')
            print(f's.scale: {s.scale}')
            print(f's.unit: {s.unit}')
            print(f's.initial: {s.initial}')


            if s.choices:
                value = random.randint(s.minimum, s.maximum)
                values.append(s.choices[value])
            elif not s.choices and s.unit == 'N.m':
                value = random.randrange(s.minimum, s.maximum)
                values.append(value)
            elif not s.choices and s.unit == 'rpm':
                value = random.randint(s.minimum, s.maximum)
                values.append(value)
            else:
                values.append(s.scale)

            print()

        return dict(zip(names, values))

    def select_n_messages(self, database: Database, n: int = 10) -> [Message]:
        nb_messages = len(database.messages)
        result = []

        for _ in range(n % nb_messages):
            chosen = random.choice(range(nb_messages)) % nb_messages
            result.append(database.messages[chosen])
        return result


    def run(self, database: cantools.database, bundle_size: int = 10):
        print('[+] Setting up fuzzing run...')
        while 1:
            messages = self.select_n_messages(database, bundle_size)
            for msg in messages:
                to_send = database.encode_message(data=self.setup_signals(msg.signals), frame_id_or_name=msg.frame_id)
                message = can.Message(arbitration_id=msg.frame_id, data=to_send)
                self.bus.send(msg=message, timeout=5.0)
