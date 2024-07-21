import unittest
from unittest.mock import patch, MagicMock

import pygame

from src.game.engine import Game, Direction
from src.game.tile import generate_tiles, Tile
from src.utils.config import conf


# Custom mock for pygame.Surface
class MockSurface(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = kwargs.get('width', 100)
        self.height = kwargs.get('height', 100)

    # Add any specific methods or properties expected by pygame functions here
    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class GamePygameTest(unittest.TestCase):
    def setUp(self):
        self.window = MockSurface(width=conf.window.width, height=conf.window.height)
        self.font = MagicMock()
        self.clock = MagicMock()
        self.tiles = generate_tiles()
        self.game = Game(self.window, self.font, self.clock, self.tiles)

    def test_has_lost_with_no_moves_left(self):
        def create_tile(value, row, col):
            return Tile(value, row, col)

        tile_values = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]

        self.game.tiles = {
            row * 4 + col: create_tile(tile_values[row][col], row, col)
            for row in range(4)
            for col in range(4)
        }

        # Ensure the game logic correctly identifies this as a loss
        self.assertTrue(self.game.has_lost())

    def test_has_not_lost_with_space_left(self):
        def create_tile(value, row, col):
            return Tile(value, row, col)

        tile_values = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 0]
        ]

        self.game.tiles = {
            row * 4 + col: create_tile(tile_values[row][col], row, col)
            if tile_values[row][col] != 0
            else None
            for row in range(4)
            for col in range(4)
        }

        # Ensure the game logic correctly identifies this as a win
        self.assertFalse(self.game.has_lost())

    def test_has_not_lost_with_moves_left(self):
        def create_tile(value, row, col):
            return Tile(value, row, col)

        tile_values = [
            [2, 4, 2, 4],
            [2, 4, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]

        self.game.tiles = {
            row * 4 + col: create_tile(tile_values[row][col], row, col)
            for row in range(4)
            for col in range(4)
        }

        # Ensure the game logic correctly identifies this as a win
        self.assertFalse(self.game.has_lost())


if __name__ == '__main__':
    unittest.main()
