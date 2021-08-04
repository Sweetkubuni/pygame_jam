import pygame

class Camera:
    def __init__(self, player, width, height, level_surface) -> None:
        self.player_rect = player.rect
        self.level_width, self.level_height = level_surface.get_width(), level_surface.get_height()

        self.width, self.height = width, height

        self.rect = pygame.Rect(self.player_rect.centerx - width//2, self.player_rect.centery - height//2, width, height)

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.level_width: self.rect.right = self.level_width
            
        self.x, self.y = int(self.rect.x), int(self.rect.y)
        
        self.speed_x, self.speed_y = 0, 0

    def update(self, player):
        if player.grounded:
            self.rect.centery = player.rect.centery
            
        self.rect.centerx = player.rect.centerx

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.level_width: self.rect.right = self.level_width

