import pygame
from config.config import colours
from sprites.tile import Tile

class Block(Tile):
    def __init__(self, tilemap, image, x, y, destructable, tile_id):
        super().__init__(tilemap, image, x, y, destructable)
        self.tile_id = tile_id
        self.x, self.y = float(x), float(y)
        self.speed_x, self.speed_y = 0, 0
        self.delete = False
    def update(self, player_rect):
        if self.rect.colliderect(player_rect) and self.rect.bottom > player_rect.top and not(self.delete):
            self.delete = True

    def draw(self):
        if not(self.delete):
            self.tilemap.level.state.game.game_canvas.blit(self.image, self.tilemap.level.camera.apply(self))
        
