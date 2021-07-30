import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, tilemap, image, x, y, destructable):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.tilemap = tilemap
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.destructable = destructable

    def draw(self):
        self.tilemap.level.state.game.game_canvas.blit(self.image, self.tilemap.level.camera.apply(self))
