import itertools
import pygame
import random
from enum import Enum
from config import conf
from utils import draw
from tile import Tile, get_random_position, generate_tiles, get_position_number


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


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
    checks = {
        Direction.LEFT: lambda tile, next_tile: tile.x > next_tile.x + conf.move.velocity,
        Direction.RIGHT: lambda tile, next_tile: tile.x < next_tile.x - conf.move.velocity,
        Direction.UP: lambda tile, next_tile: tile.y > next_tile.y + conf.move.velocity,
        Direction.DOWN: lambda tile, next_tile: tile.y < next_tile.y - conf.move.velocity
    }
    return checks[direction]


def move_check(direction: Direction):
    checks = {
        Direction.LEFT: lambda tile, next_tile: tile.x > next_tile.x + conf.tile.width + conf.move.velocity,
        Direction.RIGHT: lambda tile, next_tile: tile.x + conf.tile.width + conf.move.velocity < next_tile.x,
        Direction.UP: lambda tile, next_tile: tile.y > next_tile.y + conf.tile.height + conf.move.velocity,
        Direction.DOWN: lambda tile, next_tile: tile.y + conf.tile.height + conf.move.velocity < next_tile.y
    }
    return checks[direction]


class Game:

    def __init__(self, window, font, clock, tiles):
        self.window = window
        self.font = font
        self.clock = clock
        self.tiles = tiles

    def get_next_tile(self, direction: Direction):
        next_tile = {
            Direction.LEFT: lambda tile: self.tiles.get(tile.position_number - 1),
            Direction.RIGHT: lambda tile: self.tiles.get(tile.position_number + 1),
            Direction.UP: lambda tile: self.tiles.get(tile.position_number - conf.game.cols),
            Direction.DOWN: lambda tile: self.tiles.get(tile.position_number + conf.game.cols)
        }
        return next_tile[direction]

    def move_tiles(self, direction: Direction):
        updated = True
        blocks = set()

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

            for i, tile in enumerate(sorted_tiles):
                if boundary_check(direction)(tile):
                    continue

                next_tile = self.get_next_tile(direction)(tile)
                if not next_tile:
                    tile.move(dx, dy)
                elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                    if merge_check(direction)(tile, next_tile):
                        tile.move(dx, dy)
                    else:
                        next_tile.value *= 2
                        sorted_tiles.pop(i)
                        blocks.add(next_tile)
                elif move_check(direction)(tile, next_tile):
                    tile.move(dx, dy)
                else:
                    continue

                tile.set_position_coordinates(ceil)
                updated = True

            self.update_tiles(sorted_tiles)

        return self.has_lost()

    def has_lost(self):
        if len(self.tiles) == 16:
            return self.__has_lost_helper()

        row, col, position_number = get_random_position(self.tiles)
        self.tiles[position_number] = Tile(random.choice([2, 4]), row, col)
        return False

    def __has_lost_helper(self):
        for row, col in itertools.product(range(conf.game.rows), range(conf.game.cols)):
            position_number = get_position_number(row, col)

            tile = self.tiles.get(position_number)

            if not tile:
                return False

            # Check Adjacent Tiles
            if row > 0 and self.tiles.get(get_position_number(row - 1, col)).value == tile.value:
                return False

            if row < conf.game.rows - 1 and self.tiles.get(get_position_number(row + 1, col)).value == tile.value:
                return False

            if col > 0 and self.tiles.get(get_position_number(row, col - 1)).value == tile.value:
                return False

            if col < conf.game.cols - 1 and self.tiles.get(get_position_number(row, col + 1)).value == tile.value:
                return False

        return True

    def update_tiles(self, sorted_tiles):
        self.tiles.clear()
        for tile in sorted_tiles:
            self.tiles[tile.position_number] = tile

        draw(self.window, self.font, self.tiles)


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
