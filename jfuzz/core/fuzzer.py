# -*- coding: UTF-8 -*-
import random

import can
from cantools.database import Message

from jfuzz.core.bus import BUS
from jfuzz.core.database import Database


class Fuzzer:
    def select_n_messages(self, database: Database, n: int = 10) -> [Message]:
        result = []
        nb_messages = len(database.messages)

        for _ in range(n):
            chosen = random.choice(range(nb_messages)) % nb_messages
            result.append(database.messages[chosen])
        return result


    def run(self, bus: BUS, database: Database, bundle_size: int = 10):
        while 1:
            messages = self.select_n_messages(database, bundle_size)
            print(f'selected {messages}')
            for msg in messages:
                can_message = can.Message(arbitration_id=msg.frame_id, data=b'')
                print(f'Sending {can_message}')
                bus.interface.send(msg=can_message, timeout=5.0)
