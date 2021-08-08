import pygame, os
from config.config import colours
from sprites.text import Text
from states.state import State
from states.gameworld import Game_world

class Instructions(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)

        self.game = game
        
        all_animations = {}
        for animations in os.listdir(self.game.animation_directory):
            all_animations[animations] = []
            for frames in os.listdir(os.path.join(self.game.animation_directory, animations)):
                img = pygame.image.load(os.path.join(self.game.animation_directory, animations, frames)).convert()
                img.set_colorkey((0,0,0))
                duration = frames.split("_")[-1].split(".")[0]
                all_animations[animations].append([img, int(duration)])

        self.all_sounds = {}
        for sound in os.listdir(self.game.sound_directory):
            self.all_sounds[sound.split(".")[0]] = pygame.mixer.Sound(os.path.join(self.game.sound_directory, sound))

        self.score_timer = 0

        self.coin_animation = [all_animations["coin"], True, (0,0)]
        self.ani1_timer, self.ani2_timer, self.ani3_timer = 29, 70, 50
        self.ani1_frame, self.ani2_frame, self.ani3_frame = 0, 5, 2
        

        self.text_loop = 30

        self.load_sprites()
        
    def load_sprites(self):
        self.controls_img = pygame.image.load(os.path.join(self.game.image_directory, "controls.png")).convert()
        self.controls_img.set_colorkey((0,0,0))

        self.chest_img = pygame.image.load(os.path.join(self.game.tile_directory, "chest.png")).convert()
        self.chest_img.set_colorkey((0,0,0))

        self.enemy_img = pygame.image.load(os.path.join(self.game.image_directory, "ground_follow.png")).convert()
        self.enemy_img.set_colorkey((0,0,0))

        self.arrow_img = pygame.image.load(os.path.join(self.game.image_directory, "arrow.png")).convert()
        self.arrow_img.set_colorkey((0,0,0))
        
        self.line_1_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 18, "Shovel    Move      Shovel Down", colours["white"], False, 8, 72, False)

        self.start_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "> Press ENTER to Start! <", colours["white"], False, self.game.GAME_WIDTH *.5, self.game.GAME_HEIGHT - 30, True)
        
    def update(self):
        """Update the menu state."""
        self.game.check_inputs()
        
        if self.game.actions[pygame.K_RETURN]:
            game_world = Game_world(self.game)
            game_world.enter_state()
            
    def render(self):
        """Render the menu state."""
        self.game.game_canvas.fill(colours["black"])

        self.game.game_canvas.blit(self.controls_img, (16,10))
        self.line_1_txt.update(self.game.game_canvas)        

        self.score_timer += 1
        if self.score_timer > 120:
            self.game.game_canvas.blit(self.chest_img, (24+30,120+16))
        if self.score_timer == 120:
            pygame.mixer.find_channel(True).play(self.all_sounds["attack"])

        if self.score_timer > 140:
            self.game.game_canvas.blit(self.enemy_img, (50+40,140+16))
        if self.score_timer == 140:
            pygame.mixer.find_channel(True).play(self.all_sounds["attack"])

        if self.score_timer > 220:
            self.game.game_canvas.blit(self.arrow_img, (100+30,130))
            
        if self.score_timer > 260:
            # Coins ---------------
            self.game.game_canvas.blit(self.coin_animation[0][self.ani1_frame][0], (190,140))
            if self.ani1_timer < self.coin_animation[0][self.ani1_frame][1]:
                self.ani1_timer += self.game.delta_time
            else:
                self.ani1_timer = 0
                self.ani1_frame += 1
            if self.ani1_frame >= len(self.coin_animation[0]):
                if self.coin_animation[1] == True:
                    self.ani1_timer, self.ani1_frame = 0, 0
                else: self.change_animation(self.previous_ani[3])

            self.game.game_canvas.blit(self.coin_animation[0][self.ani2_frame][0], (220,124+8))
            if self.ani2_timer < self.coin_animation[0][self.ani2_frame][1]:
                self.ani2_timer += self.game.delta_time
            else:
                self.ani2_timer = 0
                self.ani2_frame += 1
            if self.ani2_frame >= len(self.coin_animation[0]):
                if self.coin_animation[1] == True:
                    self.ani2_timer, self.ani2_frame = 0, 0
                else: self.change_animation(self.previous_ani[3])

            self.game.game_canvas.blit(self.coin_animation[0][self.ani3_frame][0], (204,160))
            if self.ani3_timer < self.coin_animation[0][self.ani3_frame][1]:
                self.ani3_timer += self.game.delta_time
            else:
                self.ani3_timer = 0
                self.ani3_frame += 1
            if self.ani3_frame >= len(self.coin_animation[0]):
                if self.coin_animation[1] == True:
                    self.ani3_timer, self.ani3_frame = 0, 0
                else: self.change_animation(self.previous_ani[3])
                
        if self.score_timer == 260:
            pygame.mixer.find_channel(True).play(self.all_sounds["coin"])
            
        if self.score_timer > 300:
            self.text_loop -= 1
            if self.text_loop < 0:
                self.start_txt.update(content = ">Press ENTER to Start!<")
                if self.text_loop < -30: self.text_loop = 30
            else:
                self.start_txt.update(content = "> Press ENTER to Start! <")
        if self.score_timer == 300:
            pygame.mixer.find_channel(True).play(self.all_sounds["thing"])

        

