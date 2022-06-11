# -*- coding: UTF-8 -*-
import can

from jfuzz.core.database import Database
from jfuzz.core.fuzzer import Fuzzer


def main() -> None:
    dbc = Database('.')
    Fuzzer().run(dbc.database, 10)



if __name__ == '__main__':
    main()