import enum


class Size(enum.Enum):
    _1x1 = (1, 1)
    _3_6x1 = (3.6, 1)
    _3x2 = (3, 2)
    _4x3 = (4, 3)
    _5x1 = (5, 1)

    def __str__(self) -> str:
        return self.name.lstrip("_")
