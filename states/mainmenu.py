import pygame, os
from config.config import colours
from sprites.text import Text
from states.state import State
from states.instructions import Instructions
from tilemaps.app_single_output import app
from sprites.player import Player

class Main_menu(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)
        self.load_sprites()
        self.menu_screen_img = pygame.image.load(os.path.join(self.game.image_directory, "menu screen.png"))

        all_animations = {}
        for animations in os.listdir(self.game.animation_directory):
            all_animations[animations] = []
            for frames in os.listdir(os.path.join(self.game.animation_directory, animations)):
                img = pygame.image.load(os.path.join(self.game.animation_directory, animations, frames)).convert()
                img.set_colorkey((0,0,0))
                duration = frames.split("_")[-1].split(".")[0]
                all_animations[animations].append([img, int(duration)])
                
        self.zzz_animation = [all_animations["zzz"], True, (0,0)]
        self.ani_timer = 0
        self.ani_frame = 0
        self.text_loop = 30
        self.current_ani = self.zzz_animation

        app()
        self.game.player = Player(self.game, 100, 188)

        
    def load_sprites(self):
        self.all_sprites = pygame.sprite.Group()
        main_menu = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "> Press ENTER <", colours["white"], False, self.game.GAME_WIDTH *.5, self.game.GAME_HEIGHT - 30, True)
        self.all_sprites.add(main_menu)
    
    
    def update(self):
        """Update the menu state."""
        self.game.check_inputs()
        
        if self.game.actions[pygame.K_RETURN]:
            instructions = Instructions(self.game)
            instructions.enter_state()


    def render(self):
        """Render the menu state."""
        self.game.game_canvas.blit(self.menu_screen_img, (0,-30))
        self.all_sprites.draw(self.game.game_canvas)
        
        self.game.game_canvas.blit(self.current_ani[0][self.ani_frame][0], (20,12-30))
        if self.ani_timer < self.current_ani[0][self.ani_frame][1]:
            self.ani_timer += self.game.delta_time
        else:
            self.ani_timer = 0
            self.ani_frame += 1
        if self.ani_frame >= len(self.current_ani[0]):
            if self.current_ani[1] == True:
                
                self.ani_timer, self.ani_frame = 0, 0
            else: self.change_animation(self.previous_ani[3])

        self.text_loop -= 1
        if self.text_loop < 0:
            self.all_sprites.sprites()[0].update(content = ">Press ENTER<")
            if self.text_loop < -30: self.text_loop = 30
        else:
            self.all_sprites.sprites()[0].update(content = "> Press ENTER <")
