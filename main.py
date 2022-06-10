# -*- coding: UTF-8 -*-
from jfuzz.core.database import Database
from jfuzz.core.interface import BUS


def main() -> None:

    filepath = './file.dbc'

    bus = BUS()
    database = Database(filepath)

    print(f'Parsing {filepath}\n')
    print(database.messages)

    for m in database.messages:
        bus.send_one(m)


if __name__ == '__main__':
    main()