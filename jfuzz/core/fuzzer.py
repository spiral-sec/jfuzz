# -*- coding: UTF-8 -*-
import os
import random
import signal
import sys
import time
from pprint import pprint

import bitstruct
import can
import cantools
from can import Logger
from cantools.database import Message

from jfuzz.core.database import Database


class Fuzzer:
    def __init__(self):

        """
           Bring up 'socketcan' with 'vcan0' channel if environment value DEV is set,
           otherwise we connect to the VECTOR interface.

           (Make sure to register CANalyzer on channel 1 in the Vector Hardware Configuration tool)
        """
        development_mode_enabled = os.environ.get('DEV', False)
        bustype = 'socketcan' if development_mode_enabled else 'vector'
        channel = 'vcan0' if development_mode_enabled else 0
        name = 'jfuzz' if development_mode_enabled else 'CANalyzer'

        print(f'[~] Building {bustype} bus // dev mode [{development_mode_enabled}]')

        self.logger = Logger('jfuzz.blf')

        self.bus = can.ThreadSafeBus(
            name=name,
            bustype=bustype,
            channel=channel,
            fd=True,
            receive_own_messages=True
        )

    @staticmethod
    def setup_signals(signals: [cantools.database.Signal]) -> dict[str, any]:
        names: [str] = []
        values: [any] = []

        for s in signals:
            names.append(s.name)

            if not s.minimum and not s.maximum:
                values.append(1)
            elif not s.choices and s.unit == 'N.m':
                value = random.uniform(s.minimum, s.maximum)
                values.append(value)
            else:
                value = random.uniform(s.minimum, s.maximum)
                values.append(value)

        return dict(zip(names, values))

    @staticmethod
    def select_n_messages(database: Database, n: int = 10) -> [Message]:
        nb_messages = len(database.messages)
        result = []

        for _ in range(n % nb_messages):
            chosen = random.choice(range(nb_messages))
            result.append(database.messages[chosen])
        return result

    def run(self, database: cantools.database.can.Database, bundle_size: int = 10):
        print('[~] Setting up fuzzing run...')
        while 1:
            messages = self.select_n_messages(database, bundle_size)
            for msg in messages:
                try:
                    if received := self.bus.recv(timeout=0.05):
                        self.logger.on_message_received(received)
                        print(f'[-] {received}')

                    signals = self.setup_signals(msg.signals)
                    to_send = database.encode_message(data=signals, frame_id_or_name=msg.frame_id)
                    message = can.Message(arbitration_id=msg.frame_id, data=to_send)
                    self.bus.send(msg=message, timeout=0.05)

                    self.logger.on_message_received(received)
                    print(f'[+] {message}')

                # May happen when encoding cantools messages
                except OverflowError:
                    pass

                # Only happens on Vector sometimes
                except bitstruct.Error:
                    pass

                # Must always happen if there is an error
                except:
                    self.logger.stop()
                    self.bus.shutdown()
