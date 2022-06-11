# -*- coding: UTF-8 -*-
import can

from jfuzz.core.database import Database
from jfuzz.core.bus import BUS
from jfuzz.core.fuzzer import Fuzzer


def main() -> None:
    bus = BUS()
    dbc = Database('.')
    Fuzzer().run(bus, dbc.database, 10)



if __name__ == '__main__':
    main()