import pygame
from config import conf
from colors import Colors


def draw_grid(window):
    for row in range(1, conf.game.rows):
        y = row * conf.tile.height
        pygame.draw.line(
            window,
            Colors.outline.value(),
            (0, y),
            (conf.window.width, y),
            conf.border.width
        )

    for col in range(1, conf.game.cols):
        x = col * conf.tile.width
        pygame.draw.line(
            window,
            Colors.outline.value(),
            (x, 0),
            (x, conf.window.height),
            conf.border.width
        )

    pygame.draw.rect(
        window,
        Colors.outline.value(),
        (0, 0, conf.window.width, conf.window.height),
        conf.border.width
    )


def draw_lost(window, font):
    # Blur the screen
    surface = pygame.Surface(window.get_size())
    surface.set_alpha(176)
    surface.fill(Colors.background.value())
    window.blit(surface, (0, 0))

    txt_game_over = font.render(
        "Game Over!!!",
        1,
        Colors.font.value()
    )

    sub_font = pygame.font.SysFont(conf.instructions.font.name, conf.instructions.font.size, bold=True)

    txt_restart = sub_font.render(
        "Press R to restart",
        1,
        Colors.font.value()
    )

    txt_quit = sub_font.render(
        "Press Q to quit",
        1,
        Colors.font.value()
    )

    window.blit(
        txt_game_over,
        (
            conf.window.width // 2 - txt_game_over.get_width() // 2,
            conf.window.height // 2.5 - txt_game_over.get_height() // 2
        )
    )

    window.blit(
        txt_restart,
        (
            conf.window.width // 2 - txt_restart.get_width() // 2,
            conf.window.height // 2 + txt_game_over.get_height()
        )
    )

    window.blit(
        txt_quit,
        (
            conf.window.width // 2 - txt_quit.get_width() // 2,
            conf.window.height // 2 + txt_game_over.get_height() + txt_restart.get_height()
        )
    )


def draw(window, font, tiles, game_over=False):
    window.fill(Colors.background.value())

    for tile in tiles.values():
        tile.draw(window, font)

    draw_grid(window)

    if game_over:
        draw_lost(window, font)

    pygame.display.update()
