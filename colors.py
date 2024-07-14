import math
from dataclasses import dataclass


@dataclass
class Color:
    red: int
    green: int
    blue: int

    def value(self) -> tuple[int, int, int]:
        return self.red, self.green, self.blue


class Colors:
    background = Color(187, 173, 160)
    outline = Color(205, 192, 180)
    font = Color(119, 110, 101)
    tiles = [
        Color(237, 229, 218),
        Color(238, 225, 201),
        Color(243, 178, 122),
        Color(246, 150, 101),
        Color(247, 124, 95),
        Color(247, 95, 59),
        Color(237, 208, 115),
        Color(237, 204, 99),
        Color(236, 202, 80),
    ]

    @staticmethod
    def get_tile_color(value: int) -> Color:
        return Colors.tiles[int(math.log2(value)) - 1]
