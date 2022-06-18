# -*- coding: UTF-8 -*-
from jfuzz.core.database import DBC
from jfuzz.core.fuzzer import Fuzzer


def main() -> None:
    dbc = DBC('.')
    Fuzzer().run(dbc.database, 10)



if __name__ == '__main__':
    main()
