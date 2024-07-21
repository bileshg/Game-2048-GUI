import unittest
from src.game.tile import get_position_number, get_random_position, Tile, generate_tiles
from src.utils.config import conf


# sourcery skip: no-loop-in-tests
class TestGetPositionNumber(unittest.TestCase):

    def test_get_position_number_happy_path(self):
        test_cases = [
            (0, 0, 0),  # top-left corner
            (0, 3, 3),  # top-right corner
            (3, 0, 12),  # bottom-left corner
            (3, 3, 15),  # bottom-right corner
            (1, 2, 6),  # middle of the grid
            (2, 1, 9),  # another middle value
        ]

        for row, col, expected in test_cases:
            with self.subTest(row=row, col=col):
                result = get_position_number(row, col)
                self.assertEqual(result, expected)

    def test_get_position_number_edge_cases(self):
        test_cases = [
            (0, 4, 4),  # column just outside the grid
            (4, 0, 16),  # row just outside the grid
            (4, 4, 20),  # both row and column just outside the grid
            (-1, 0, -4),  # negative row
            (0, -1, -1),  # negative column
            (-1, -1, -5),  # both row and column negative
        ]

        for row, col, expected in test_cases:
            with self.subTest(row=row, col=col):
                result = get_position_number(row, col)
                self.assertEqual(result, expected)

    def test_get_position_number_error_cases(self):
        test_cases = [
            ("a", 0, TypeError),  # row is not an integer
            (0, "b", TypeError),  # column is not an integer
            (None, 0, TypeError),  # row is None
            (0, None, TypeError),  # column is None
        ]

        for row, col, expected_exception in test_cases:
            with self.subTest(row=row, col=col):
                with self.assertRaises(expected_exception):
                    get_position_number(row, col)


class TestGetRandomPosition(unittest.TestCase):

    def test_get_random_position_with_no_tiles(self):
        tiles = {}

        row, col, position_number = get_random_position(tiles)
        self.assertGreaterEqual(row, 0)
        self.assertLess(row, conf.game.rows)
        self.assertGreaterEqual(col, 0)
        self.assertLess(col, conf.game.cols)

    def test_get_random_position_with_one_row_full(self):
        tiles = {
            0: Tile(2, 0, 0),
            1: Tile(4, 0, 1),
            2: Tile(8, 0, 2),
            3: Tile(16, 0, 3),
        }

        row, col, position_number = get_random_position(tiles)

        self.assertNotIn(position_number, tiles.keys())
        self.assertGreater(row, 0)
        self.assertLess(row, conf.game.rows)

    def test_get_random_position_with_one_column_full(self):
        tiles = {
            0: Tile(2, 0, 0),
            4: Tile(4, 1, 0),
            8: Tile(8, 2, 0),
            12: Tile(16, 3, 0),
        }

        row, col, position_number = get_random_position(tiles)

        self.assertNotIn(position_number, tiles.keys())
        self.assertGreater(col, 0)
        self.assertLess(col, conf.game.cols)

    def test_get_random_position_with_all_positions_full(self):
        tiles = {
            0: Tile(2, 0, 0),
            1: Tile(4, 0, 1),
            2: Tile(8, 0, 2),
            3: Tile(16, 0, 3),
            4: Tile(32, 1, 0),
            5: Tile(64, 1, 1),
            6: Tile(128, 1, 2),
            7: Tile(256, 1, 3),
            8: Tile(512, 2, 0),
            9: Tile(1024, 2, 1),
            10: Tile(2048, 2, 2),
            11: Tile(4096, 2, 3),
            12: Tile(8192, 3, 0),
            13: Tile(16384, 3, 1),
            14: Tile(32768, 3, 2),
            15: Tile(65536, 3, 3),
        }

        with self.assertRaises(ValueError):
            get_random_position(tiles)

    def test_get_random_position_with_one_empty_position(self):
        tiles = {
            0: Tile(2, 0, 0),
            1: Tile(4, 0, 1),
            2: Tile(8, 0, 2),
            3: Tile(16, 0, 3),
            4: Tile(32, 1, 0),
            5: Tile(64, 1, 1),
            6: Tile(128, 1, 2),
            # 7: Tile(256, 1, 3),  # empty position
            8: Tile(512, 2, 0),
            9: Tile(1024, 2, 1),
            10: Tile(2048, 2, 2),
            11: Tile(4096, 2, 3),
            12: Tile(8192, 3, 0),
            13: Tile(16384, 3, 1),
            14: Tile(32768, 3, 2),
            15: Tile(65536, 3, 3),
        }

        row, col, position_number = get_random_position(tiles)

        self.assertNotIn(position_number, tiles.keys())
        self.assertEqual(row, 1)
        self.assertEqual(col, 3)


class TileTest(unittest.TestCase):
    def setUp(self):
        self.tile = Tile(2, 0, 0)

    def test_tile_initialization_sets_correct_attributes(self):
        self.assertEqual(self.tile.value, 2)
        self.assertEqual(self.tile.row, 0)
        self.assertEqual(self.tile.col, 0)

    def test_moving_tile_changes_its_position(self):
        initial_x = self.tile.x
        initial_y = self.tile.y
        self.tile.move(10, 15)
        self.assertEqual(self.tile.x, initial_x + 10)
        self.assertEqual(self.tile.y, initial_y + 15)


class TestGenerateTiles(unittest.TestCase):

    def test_generate_tiles_creates_two_tiles(self):
        tiles = generate_tiles()
        self.assertEqual(len(tiles), 2)

    def test_generate_tiles_instances_are_tiles(self):
        tiles = generate_tiles()
        for tile in tiles.values():
            with self.subTest(tile=tile):
                self.assertIsInstance(tile, Tile)

    def test_generate_tiles_creates_tiles_with_correct_values(self):
        tiles = generate_tiles()
        for tile in tiles.values():
            with self.subTest(tile=tile):
                self.assertIn(tile.value, [2, 4])


if __name__ == '__main__':
    unittest.main()
