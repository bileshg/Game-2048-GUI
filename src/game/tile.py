import random
import pygame
import math
from src.utils.config import conf
from src.utils.colors import Colors


def get_position_number(row, col):
    return row * conf.game.cols + col


def get_random_position(tiles):
    if len(tiles) == conf.game.rows * conf.game.cols:
        raise ValueError("All positions are full")

    while True:
        row = random.randrange(0, conf.game.rows)
        col = random.randrange(0, conf.game.cols)

        position_number = get_position_number(row, col)

        if position_number not in tiles.keys():
            break

    return row, col, position_number


class Tile:

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col

        self.position_number = get_position_number(row, col)

        self.x = col * conf.tile.width
        self.y = row * conf.tile.height

    def draw(self, window, font):
        color = Colors.get_tile_color(self.value).value()
        pygame.draw.rect(window, color, (self.x, self.y, conf.tile.width, conf.tile.height))

        text = font.render(str(self.value), 1, Colors.font.value())
        window.blit(
            text,
            (
                self.x + (conf.tile.width / 2 - text.get_width() / 2),
                self.y + (conf.tile.height / 2 - text.get_height() / 2),
            ),
        )

    def set_position_coordinates(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / conf.tile.height)
            self.col = math.ceil(self.x / conf.tile.width)
        else:
            self.row = math.floor(self.y / conf.tile.height)
            self.col = math.floor(self.x / conf.tile.width)

        self.position_number = get_position_number(self.row, self.col)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def __str__(self):
        return f"Tile(x: {self.row}; y: {self.col}; value: {self.value})"


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col, position_number = get_random_position(tiles)
        tiles[position_number] = Tile(2, row, col)
    return tiles
