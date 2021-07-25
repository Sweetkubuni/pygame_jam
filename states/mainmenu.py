import pygame, os
from config.config import colours
from sprites.text import Text
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
        self.load_sprites()

    def load_sprites(self):
        self.all_sprites = pygame.sprite.Group()
        main_menu = Text(os.path.join(self.game.font_directory,"FreePixel.ttf"), 20,
                         "Press Enter To Start!", colours["black"], 
                         self.game.GAME_HEIGHT/2, self.game.GAME_WIDTH/2)
        self.all_sprites.add(main_menu)
    
    
    def update(self):
        """Update the menu state."""
        if self.game.actions[pygame.K_RETURN]:
            game_world = Game_world(self.game)
            game_world.enter_state()

    def render(self):
        """Render the menu state."""
        self.game.game_canvas.fill(colours["green"]) #temporary
        self.all_sprites.draw(self.game.game_canvas)