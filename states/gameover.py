import pygame, os, json
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

        self.score_timer = 0
        self.score = 20*self.total_player_coins + 40*self.total_player_kills + self.total_player_height

        with open(os.path.join("config", "scores.json"), "r") as scores_json_file:
            scores = json.load(scores_json_file)
    
            if int(scores["highscore"]) < self.score:
                scores["highscore"] = self.score
                self.score_colour = colours["yellow"]
            else:
                self.score_colour = colours["white"]
            self.highscore = int(scores["highscore"])
            scores_json_file.close()
            
        with open(os.path.join("config", "scores.json"), "w") as scores_json_file:
            json.dump(scores, scores_json_file)
            scores_json_file.close()
            
        self.load_sprites()
        self.text_loop = 30
        
        
    def load_sprites(self):
        self.all_sprites = pygame.sprite.Group()
        self.game_over_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "GAME OVER", colours["red"], False, self.game.GAME_WIDTH *.5, 80-40, True)
        self.coins_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "Coins - "  + str(self.player_coins), colours["white"], False, self.game.GAME_WIDTH *.5, 140-45, True)
        self.kills_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "Enemies - " + str(self.player_kills), colours["white"], False, self.game.GAME_WIDTH *.5, 165-45, True)
        self.height_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "Depth - " + str(int(self.player_height)), colours["white"], False, self.game.GAME_WIDTH *.5, 190-45, True)
        self.score_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "YOUR SCORE - " + str(int(self.score)), colours["blue"], False, self.game.GAME_WIDTH *.5, 240-40, True)

        self.highscore_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "HIGHSCORE - " + str(int(self.highscore)), colours["yellow"], False, self.game.GAME_WIDTH *.5, 50, True)

        self.restart_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"alphbeta.ttf"), 22, "> Press Enter to Restart <", colours["red"], False, self.game.GAME_WIDTH *.5, 180, True)
    def update(self):
        """Update the menu state."""
        self.game.check_inputs()

        if self.game.actions[pygame.K_RETURN]:
            self.game.restart()
            
    def render(self):
        """Render the menu state."""
        self.game.game_canvas.fill(colours["black"])
        
        self.score_timer += 1
        if self.score_timer > 120 and self.score_timer < 400:
            if self.total_player_coins > self.player_coins: self.player_coins += 0.5
            self.coins_txt.update(self.game.game_canvas, content = "Coins - "  + str(int(self.player_coins)))
        if self.score_timer == 120:
            pygame.mixer.find_channel(True).play(self.all_sounds["thing"])
            
        if self.score_timer > 200 and self.score_timer < 400:
            if self.total_player_kills > self.player_kills: self.player_kills += 0.2
            self.kills_txt.update(self.game.game_canvas, content = "Enemies - " + str(int(self.player_kills)))
        if self.score_timer == 200:
            pygame.mixer.find_channel(True).play(self.all_sounds["thing"])
            
        if self.score_timer > 280 and self.score_timer < 400:
            if self.total_player_height > self.player_height: self.player_height += 10
            self.height_txt.update(self.game.game_canvas, content = "Depth - " + str(int(self.player_height)))
        if self.score_timer == 280:
            pygame.mixer.find_channel(True).play(self.all_sounds["thing"])

        if self.score_timer >= 400:
            self.highscore_txt.update(self.game.game_canvas)
            self.score_txt.update(self.game.game_canvas, content = "YOUR SCORE - " + str(self.score), colour = self.score_colour, y = 120)
            self.text_loop -= 1
            if self.text_loop < 0:
                self.restart_txt.update(content = ">Press ENTER To Restart<")
                if self.text_loop < -30: self.text_loop = 30
            else:
                self.restart_txt.update(content = "> Press ENTER To Restart <")
        else:
            self.game_over_txt.update(self.game.game_canvas)
            self.score_txt.update(self.game.game_canvas, "YOUR SCORE - " + str(int(20*self.player_coins + 40*self.player_kills + self.player_height)))
