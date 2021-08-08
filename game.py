import pygame, time, os, sys
from config.config import options, colours
from states.mainmenu import Main_menu
from sprites.player import Player
from levels.level import Level

class Game:
    """The game object, used to control the game."""
    def __init__(self) -> None:
        """Initializing the game."""
        pygame.init()
        pygame.display.set_caption(options["window_title"])
        self.scale = options["scale"]
        self.SCREEN_SIZE = self.SCREEN_WIDTH, self.SCREEN_HEIGHT = options["game_width"], options["game_height"]
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH*self.scale, self.SCREEN_HEIGHT*self.scale))
        self.GAME_SIZE = self.GAME_WIDTH, self.GAME_HEIGHT = options["game_width"], options["game_height"]
        self.game_canvas = pygame.Surface(self.GAME_SIZE)
        self.clock = pygame.time.Clock()
        self.MAX_FPS = options["fps"]
        self.running, self.playing = True, True
        self.actions = pygame.key.get_pressed()
        self.delta_time, self.previous_time = 0, 0
        self.state_stack = []
        self.player = Player(self, 100, 188)

        pygame.mixer.init()
        pygame.mixer.set_num_channels(5) # a maximum of 5 sounds can be playing at the same time

    def new(self):
        """Starting a new game"""
        self.setup_directories()
        self.load_first_state()
        self.game_loop()

    def restart(self):
        self.__init__
        self.new()

    def game_loop(self) -> None:
        """The main game loop, used to update the game based on inputs and then rendering it on the screen."""
        while self.playing:
            self.get_delta_time()
            self.check_inputs()
            self.update()
            self.render()

    def update(self) -> None:
        """Updates the needed opponents according to the current game state with respect for the imputs recived."""
        self.state_stack[-1].update()

    def render(self):
        """Renders the needed opponents according to the current game state."""
        self.state_stack[-1].render()

        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH*self.scale, self.SCREEN_HEIGHT*self.scale)), (0, 0))
        pygame.display.update()
        self.clock.tick(self.MAX_FPS)

    def check_inputs(self) -> None:
        """Checking for inputs from the user."""
        self.actions = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shut_down()
                pygame.display.quit()
                pygame.quit()
                sys.exit()

    def load_first_state(self) -> None:
        """Loading the first state of the game."""
        self.state_stack = [Main_menu(self)]

    def get_delta_time(self) -> None:
        """Getting the time used between frames. Used to calculate movement so its universal across frame rates."""
        now = time.time()
        self.delta_time = now - self.previous_time
        self.delta_time *= self.MAX_FPS
        self.previous_time = now

    def setup_directories(self) -> None:
        self.sprite_directory = os.path.join("sprites")
        self.state_directory = os.path.join("states")
        self.tilemap_directory = os.path.join("tilemaps")
        # Assets
        self.asset_directory = os.path.join("assets")
        self.font_directory = os.path.join(self.asset_directory, "fonts")
        self.image_directory = os.path.join(self.asset_directory, "images")
        self.tile_directory = os.path.join(self.image_directory, "tiles")
        self.animation_directory = os.path.join(self.asset_directory, "animations")
        self.sound_directory = os.path.join(self.asset_directory, "sounds")
        
    def shut_down(self) -> None:
        """Completley shutting down the game."""
        self.playing = False
        self.running = False
