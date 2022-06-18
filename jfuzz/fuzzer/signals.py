# -*- coding: UTF-8 -*-

from typing import Union, List
from cantools.database.can.signal import Signal


Numeric = Union[int, float, complex, None]


def setup_signals(signals: List[Signal]) -> dict[str, Numeric]:
    names: List[str] = []
    values: List[Numeric] = []

    for s in signals:
        names.append(s.name)

        if not s.minimum and not s.maximum:
            values.append(1)
        elif not s.choices and s.unit == 'N.m':
            value = random.uniform(s.minimum, s.maximum)    # type: ignore
            values.append(value)
        else:
            value = random.uniform(s.minimum, s.maximum)    # type: ignore
            values.append(value)

    return dict(zip(names, values))

