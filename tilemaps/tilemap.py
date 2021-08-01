import pygame, os, csv
from sprites.tile import Tile
from sprites.block import Block
from sprites.enemy import Ground_enemy, Air_enemy, Follower_ground, Follower_air
from config.config import tile_keys
from hub import loadImage

from sprites.enemy import *

class Tile_map:
    def __init__(self, level, csv_filepath):
        self.csv_filepath = csv_filepath
        self.level = level
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0

    def read_csv(self):
        tilemap = []
        with open(os.path.join(self.csv_filepath), "r", newline="") as map_csv_file:
            reader = csv.reader(map_csv_file)
            tilemap = [[int(tile) for tile in row] for row in reader]
        return tilemap
    
    def load_tiles_and_blocks(self, all_animations, all_sounds, game):
        tiles_and_blocks = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        tile_map_template = self.read_csv()
        x, y = 0, 0
        for row in tile_map_template:
            x = 0
            for tile in row:
                # -----------------------ENEMIES --------------------------------
                if tile == 30: # Ground enemy -> Gumba
                    enemies.add(Ground_enemy(x * self.tile_size, y * self.tile_size, loadImage(os.path.join(game.image_directory, "ground.png")), game))
                if tile == 31: # Air enemy -> Flyer
                    enemies.add(Air_enemy(x * self.tile_size, y * self.tile_size, loadImage(os.path.join(game.image_directory, "fly.png")), game))
                if tile == 32: # Ground enemy -> Follower
                    enemies.add(Follower_ground(x * self.tile_size, y * self.tile_size, loadImage(os.path.join(game.image_directory, "ground_follow.png")), 100, game))
                if tile == 33:
                    enemies.add(Follower_air(x * self.tile_size, y * self.tile_size, loadImage(os.path.join(game.image_directory, "fly_follow.png")), 100, game))
                for tile_key in tile_keys:
                    if tile == tile_key:
                        if tile == 0 or tile == 1: # Dirt and grass are destructable
                            # I'm passing the Block object , the tile_id as "tile" so each block has unique properties and interactions
                            tiles_and_blocks.add(Block(self, tile_keys[tile_key], x * self.tile_size, y * self.tile_size, True, tile, all_animations, all_sounds))
                        else:
                            tiles_and_blocks.add(Tile(self, tile_keys[tile_key], x * self.tile_size, y * self.tile_size, False))
                x += 1
            y += 1
        self.width, self.height = x * self.tile_size, y * self.tile_size
        return tiles_and_blocks, enemies
