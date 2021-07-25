import pygame, os
from config.config import colours
from states.state import State
from states.gameworld import Game_world

class Main_menu(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)
        self.image_paths = {
            "main-menu-bg": os.path.join(self.game.asset_directory, "images", "main-menu", "background.jpg")
        }
        self.images = {k:pygame.image.load(v) for k,v in self.image_paths.items()}
    def update(self):
        """Update the menu state."""
        if self.game.actions[pygame.K_RETURN]:
            game_world = Game_world(self.game)
            game_world.enter_state()

    def render(self):
        """Render the menu state."""
        #self.game.game_canvas.blit(pygame.transform.scale(self.images["main-menu-bg"], (self.game.GAME_WIDTH//2, self.game.GAME_HEIGHT//2)), (0, 0))
        self.game.game_canvas.fill(colours["green"]) #temporary