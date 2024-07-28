import pygame

from src.utils.config import conf
from src.game.engine import game_loop


def main():
    pygame.init()
    font = pygame.font.SysFont(conf.font.name, conf.font.size, bold=True)
    window = pygame.display.set_mode((conf.window.width, conf.window.height))
    pygame.display.set_caption(conf.window.title)
    clock = pygame.time.Clock()

    game_loop(window, font, clock)


if __name__ == "__main__":
    main()
