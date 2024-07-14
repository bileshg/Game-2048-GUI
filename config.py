from omegaconf import OmegaConf

conf = OmegaConf.load("config.yaml")

conf.tile = {}
conf.tile.width = conf.window.width // conf.game.cols
conf.tile.height = conf.window.height // conf.game.rows

conf.instructions = {}
conf.instructions.font = {}
conf.instructions.font.name = conf.font.name
conf.instructions.font.size = conf.font.size // 2 if conf.font.size // 2 > 10 else 10
