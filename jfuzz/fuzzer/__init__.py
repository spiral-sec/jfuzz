# -*- coding: UTF-8 -*-
import os

import bitstruct
import can
from can import Logger
from can.thread_safe_bus import ThreadSafeBus
from cantools.database.can.database import Database

from jfuzz.core.config import Config
from jfuzz.fuzzer.signals import setup_signals # type: ignore


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

        self.bus = ThreadSafeBus(
            name=name,
            bustype=bustype,
            channel=channel,
            bitrate=50000,  # default CANalyzer settings
            fd=True,
        )

        if not self.is_dev: ## SocketCAN does not play well with other file descriptors apparently
            config = Config()
            sep_character = '/' if self.is_dev else '\\'
            filename = os.getcwd() + sep_character + config.settings.get('log_name', 'jfuzz') + \
                    config.settings.get('log_extension', '.asc')

            self.logger = Logger(filename)

    def read(self):
        if received := self.bus.recv():
            if not self.is_dev:
                self.logger.on_message_received(received)
            print(f'[-] {received}')

    def send(self, msg, database):
        signals = setup_signals(msg.signals)
        to_send = database.encode_message(data=signals, frame_id_or_name=msg.frame_id)
        message = can.Message(arbitration_id=msg.frame_id, data=to_send)

        try:
            self.bus.send(msg=message, timeout=5.0)
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


        print(f'[+] {message}')

    def run(self, database: Database):
        print('[~] Setting up fuzzing run...')
        self.bus.flush_tx_buffer()

