import pygame
from config.config import colours
from sprites.tile import Tile

class Block(Tile):
    def __init__(self, tilemap, image, x, y, destructable, tile_id, all_animations, all_sounds):
        super().__init__(tilemap, image, x, y, destructable)
        self.tile_id = tile_id
        self.x, self.y = float(x), float(y)
        self.speed_x, self.speed_y = 0, 0
        self.delete = False
        self.sounds = {"explodeBrick": all_sounds["explodeBrick"]}
        
    def update(self, attack_sprite, previous_delete):
        if attack_sprite != None and not(previous_delete):
            if self.rect.colliderect(attack_sprite.rect) and not(self.delete):
                self.delete = True
            
    def draw(self, layer):
        if not(self.delete):
            layer.blit(self.image, self.rect)
        
