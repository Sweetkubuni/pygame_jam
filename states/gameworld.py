import pygame, os
from config.config import colours
from hub import loadImage
from tilemaps.tilemap import Tile_map
from states.state import State

class Game_world(State):
    """The game world"""
    def __init__(self, game):
        """Initialize the game world class."""
        super().__init__(game)
        self.tile_map = Tile_map(
            os.path.join(self.game.tilemap_directory, "game-world.csv"), 
            {
                0: loadImage(os.path.join(self.game.tile_directory, "dirt.jpg")),
                1: loadImage(os.path.join(self.game.tile_directory, "grass.jpg")),
                2: loadImage(os.path.join(self.game.tile_directory, "sky.jpg")),
                3: loadImage(os.path.join(self.game.tile_directory, "cave.jpg"))
            }
        )
        self.tiles = self.tile_map.load_tiles()
        

    def update(self):
        """Update the menu state."""
        if self.game.actions[pygame.K_RETURN]:
            game_world = Game_world(self.game)
            game_world.enter_state()

    def render(self):
        """Render the menu state."""
        self.tiles.draw(self.game.game_canvas)