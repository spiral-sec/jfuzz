# -*- coding: UTF-8 -*-
import os
import random

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
        self.is_dev = os.name != 'nt'
        bustype = 'socketcan' if self.is_dev else 'vector'
        channel = 'vcan0' if self.is_dev else 0
        name = 'jfuzz' if self.is_dev else 'CANalyzer'

        print(f'[~] Building {bustype} bus // dev mode [{self.is_dev}]')

        self.bus = can.interface.Bus(
            name=name,
            bustype=bustype,
            channel=channel,
            bitrate=10000,
            fd=True,
        )

        if not self.is_dev: ## SocketCAN does not play well with other file descriptors apparently
            self.logger = Logger('jfuzz.blf')

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

    def read(self):
        if received := self.bus.recv():
            if not self.is_dev:
                self.logger.on_message_received(received)
            print(f'[-] {received}')

    def send(self, msg, database):
        signals = self.setup_signals(msg.signals)
        to_send = database.encode_message(data=signals, frame_id_or_name=msg.frame_id)
        message = can.Message(arbitration_id=msg.frame_id, data=to_send)
        self.bus.send(msg=message, timeout=5.0)

        print(f'[+] {message}')

    def run(self, database: cantools.database.can.Database, bundle_size: int = 10):
        print('[~] Setting up fuzzing run...')
        self.bus.flush_tx_buffer()
        while 1:
            messages = self.select_n_messages(database, bundle_size)
            for msg in messages:
                try:

                    if not self.is_dev:
                        self.read()

                    self.send(msg, database)

                # May happen when encoding cantools messages
                except OverflowError:
                    pass

                # Happens only sometimes with SocketCAN
                except can.exceptions.CanOperationError:
                    pass

                # Only happens on Vector sometimes
                except bitstruct.Error:
                    pass

                # Must always happen if there is an error
                except:
                    if not self.is_dev:
                        self.logger.stop()
                    self.bus.shutdown()
