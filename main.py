# -*- coding: UTF-8 -*-


from jfuzz.fuzzer import Fuzzer
from jfuzz.fuzzer.database import DBC


def main() -> None:
    dbc = DBC('.')
    Fuzzer().run(dbc.database)



if __name__ == '__main__':
    main()
