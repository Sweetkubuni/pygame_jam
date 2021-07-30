import pygame, os
from config.config import colours
from hub import loadImage
from tilemaps.tilemap import Tile_map
from states.state import State
from levels.level import Level

class Game_world(State):
    """The game world"""
    def __init__(self, game):
        """Initialize the game world class."""
        super().__init__(game)
        temp_background = pygame.Surface(self.game.GAME_SIZE)
        temp_background.fill(colours["blue"])

        self.all_animations = {}
        for animations in os.listdir(self.game.animation_directory):
            self.all_animations[animations] = []
            for frames in os.listdir(os.path.join(self.game.animation_directory, animations)):
                img = pygame.image.load(os.path.join(self.game.animation_directory, animations, frames)).convert()
                img.set_colorkey((0,0,0))
                duration = frames.split("_")[-1].split(".")[0]
                self.all_animations[animations].append([img, int(duration)])
        
        self.levels = {
            1: Level(self,
                os.path.join(self.game.tilemap_directory, "level-1.csv"),
                temp_background,
                0, 0
            )
        }
        self.change_level(self.levels[1])
        
    def change_level(self, new_level):
        self.current_level = new_level

    def update(self):
        """Update the menu state."""
        self.current_level.update()

    def render(self):
        """Render the menu state."""
        self.current_level.render()
