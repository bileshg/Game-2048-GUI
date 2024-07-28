import itertools
import pygame
import random

from src.game.direction import Direction
from src.utils.config import conf
from src.game.draw import draw
from src.game.tile import Tile, get_random_position, generate_tiles, get_position_number


def to_grid(tiles: dict):
    grid = [[None for _ in range(conf.game.cols)] for _ in range(conf.game.rows)]
    for tile in tiles.values():
        grid[tile.row][tile.col] = tile.value
    return grid


def sort_by(direction: Direction):
    return lambda x: x.col if direction in [Direction.LEFT, Direction.RIGHT] else x.row


def boundary_check(direction: Direction):
    checks = {
        Direction.LEFT: lambda tile: tile.col == 0,
        Direction.RIGHT: lambda tile: tile.col == conf.game.cols - 1,
        Direction.UP: lambda tile: tile.row == 0,
        Direction.DOWN: lambda tile: tile.row == conf.game.rows - 1
    }
    return checks[direction]


def merge_check(direction: Direction):
    def check(tile, next_tile):
        if direction == Direction.LEFT:
            return tile.x > next_tile.x + conf.move.velocity
        elif direction == Direction.RIGHT:
            return tile.x < next_tile.x - conf.move.velocity
        elif direction == Direction.UP:
            return tile.y > next_tile.y + conf.move.velocity
        elif direction == Direction.DOWN:
            return tile.y < next_tile.y - conf.move.velocity

    return check


def move_check(direction: Direction):
    def check(tile, next_tile):
        tile_width = conf.tile.width
        tile_height = conf.tile.height
        move_velocity = conf.move.velocity

        if direction == Direction.LEFT:
            return tile.x > next_tile.x + tile_width + move_velocity
        elif direction == Direction.RIGHT:
            return tile.x + tile_width + move_velocity < next_tile.x
        elif direction == Direction.UP:
            return tile.y > next_tile.y + tile_height + move_velocity
        elif direction == Direction.DOWN:
            return tile.y + tile_height + move_velocity < next_tile.y

    return check


class Game:

    def __init__(self, window, font, clock, tiles):
        self.window = window
        self.font = font
        self.clock = clock
        self.tiles = tiles

    def get_next_tile(self, tile: Tile, direction: Direction):
        row, col = tile.row, tile.col

        direction_map = {
            Direction.LEFT: (0, -1),
            Direction.RIGHT: (0, 1),
            Direction.UP: (-1, 0),
            Direction.DOWN: (1, 0)
        }

        row_adjust, col_adjust = direction_map[direction]
        row += row_adjust
        col += col_adjust

        return self.tiles.get(get_position_number(row, col))

    def move_tiles(self, direction: Direction):
        updated = True
        blocked = set()

        # dx, dy, reverse, ceil
        directions = {
            Direction.LEFT: (-conf.move.velocity, 0, False, True),
            Direction.RIGHT: (conf.move.velocity, 0, True, False),
            Direction.UP: (0, -conf.move.velocity, False, True),
            Direction.DOWN: (0, conf.move.velocity, True, False)
        }
        dx, dy, reverse, ceil = directions[direction]

        while updated:
            self.clock.tick(conf.game.fps)
            updated = False
            sorted_tiles = sorted(self.tiles.values(), key=sort_by(direction), reverse=reverse)

            tiles_to_remove = []
            for tile in sorted_tiles:
                if boundary_check(direction)(tile):
                    continue

                next_tile = self.get_next_tile(tile, direction)
                if not next_tile:
                    tile.move(dx, dy)
                elif tile.value == next_tile.value and tile not in blocked and next_tile not in blocked:
                    if merge_check(direction)(tile, next_tile):
                        tile.move(dx, dy)
                    else:
                        next_tile.value *= 2
                        tiles_to_remove.append(tile)
                        blocked.add(tile)
                        blocked.add(next_tile)
                elif move_check(direction)(tile, next_tile):
                    tile.move(dx, dy)
                else:
                    continue

                tile.set_position_coordinates(ceil)
                updated = True

            for tile in tiles_to_remove:
                sorted_tiles.remove(tile)

            self.update_tiles(sorted_tiles)

        return self.has_lost()

    def has_lost(self):
        if len(self.tiles) == 16:
            return not self.__has_possible_moves()

        row, col, position_number = get_random_position(self.tiles)
        self.tiles[position_number] = Tile(random.choice([2, 4]), row, col)
        return False

    def __has_possible_moves(self):
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for row, col in itertools.product(range(conf.game.rows), range(conf.game.cols)):
            position_number = get_position_number(row, col)
            tile = self.tiles.get(position_number)

            if not tile:
                return True

            for dr, dc in deltas:
                adj_row, adj_col = row + dr, col + dc
                if 0 <= adj_row < conf.game.rows and 0 <= adj_col < conf.game.cols:
                    adjacent_tile = self.tiles.get(get_position_number(adj_row, adj_col))
                    if adjacent_tile is None or adjacent_tile.value == tile.value:
                        return True

        return False

    def update_tiles(self, sorted_tiles):
        self.tiles.clear()
        for tile in sorted_tiles:
            self.tiles[tile.position_number] = tile

        draw(self.window, self.font, self.tiles)

    def __str__(self):
        return str(to_grid(self.tiles))


def game_event_helper(game, event):
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_LEFT, pygame.K_a]:
            return game.move_tiles(Direction.LEFT)
        if event.key in [pygame.K_RIGHT, pygame.K_d]:
            return game.move_tiles(Direction.RIGHT)
        if event.key in [pygame.K_UP, pygame.K_w]:
            return game.move_tiles(Direction.UP)
        if event.key in [pygame.K_DOWN, pygame.K_s]:
            return game.move_tiles(Direction.DOWN)

    return False


def game_loop(window, font, clock):
    run = True
    has_lost = False

    tiles = generate_tiles()
    game = Game(window, font, clock, tiles)

    while run:
        clock.tick(conf.game.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if not has_lost:
                    has_lost = game_event_helper(game, event)
                else:
                    if event.key == pygame.K_r:
                        tiles = generate_tiles()
                        game = Game(window, font, clock, tiles)
                        has_lost = False
                    if event.key == pygame.K_q:
                        run = False
                        break

        draw(window, font, tiles, has_lost)

    pygame.quit()
