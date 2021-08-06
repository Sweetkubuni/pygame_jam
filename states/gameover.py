import pygame, os
from config.config import colours
from sprites.text import Text
from states.state import State

class Game_over(State):
    """The main menu"""
    def __init__(self, game, player_coins, player_kills, player_height):
        """Initialize the menu class."""
        super().__init__(game)
        
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

        self.player_coins, self.player_kills, self.player_height = 0, 0, 0
        self.total_player_coins, self.total_player_kills, self.total_player_height = player_coins, player_kills, player_height

        self.load_sprites()

        self.score_timer = 0

        
    def load_sprites(self):
        self.all_sprites = pygame.sprite.Group()
        self.game_over_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "GAME OVER", colours["white"], False, self.game.GAME_WIDTH *.5, 80, True)
        self.coins_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "Coins - "  + str(self.player_coins), colours["white"], False, self.game.GAME_WIDTH *.5, 140, True)
        self.kills_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "Enemies - " + str(self.player_kills), colours["white"], False, self.game.GAME_WIDTH *.5, 165, True)
        self.height_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "Depth - " + str(int(self.player_height)), colours["white"], False, self.game.GAME_WIDTH *.5, 190, True)
    def update(self):
        """Update the menu state."""
        self.game.check_inputs()

    def render(self):
        """Render the menu state."""
        self.game.game_canvas.fill(colours["black"])

        self.game_over_txt.update(self.game.game_canvas)
        
        self.score_timer += 1
        if self.score_timer > 120:
            if self.total_player_coins > self.player_coins: self.player_coins += 0.5
            self.coins_txt.update(self.game.game_canvas, content = "Coins - "  + str(int(self.player_coins)))
        if self.score_timer == 120:
            pygame.mixer.find_channel(True).play(self.all_sounds["coin"])
            
        if self.score_timer > 200:
            if self.total_player_kills > self.player_kills: self.player_kills += 0.2
            self.kills_txt.update(self.game.game_canvas, content = "Enemies - " + str(int(self.player_kills)))
        if self.score_timer == 200:
            pygame.mixer.find_channel(True).play(self.all_sounds["coin"])
            
        if self.score_timer > 280:
            if self.total_player_height > self.player_height: self.player_height += 10
            self.height_txt.update(self.game.game_canvas, content = "Depth - " + str(int(self.player_height)))
        if self.score_timer == 280:
            pygame.mixer.find_channel(True).play(self.all_sounds["coin"])
        
        
