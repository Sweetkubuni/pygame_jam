import pygame, math

class Camera:
    def __init__(self, player, width, height, level_surface, game) -> None:
        self.player_rect = player.rect
        self.level_width, self.level_height = level_surface.get_width(), level_surface.get_height()

        self.width, self.height = width, height

        self.game = game

        self.rect = pygame.Rect(self.player_rect.centerx - width//2, self.player_rect.centery - height//2, width, height)

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.level_width:
            self.rect.right = self.level_width

        self.x, self.y = int(self.rect.x), int(self.rect.y)
        
        self.speed_x, self.speed_y = 0, 0

    def easeOutExpo(self, t, b, c, d):
        #       time, starting point, change, duration
        if d != 0:
            return c * ( -math.pow( 2, -10 * t/d ) + 1 ) + b

    def update(self, player):
        if not(player.grounded): chasing_speed = 0
        else: chasing_speed = 6

        offset = 20 + player.speed_y*20

        if abs(self.rect.centery - (player.rect.centery - offset)) < 2:
            self.rect.centery = player.rect.centery - offset

        if offset > 100: offset = 100

        self.speed_y = ((player.rect.centery - (self.rect.centery - offset))/(player.rect.centery - offset)) * self.easeOutExpo(abs(self.rect.centery - (player.rect.centery - offset)), chasing_speed, 0.5, 8)
            
        self.y += self.speed_y * self.game.delta_time

        self.rect.y = int(self.y)
            
        self.rect.centerx = player.rect.centerx

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.level_width: self.rect.right = self.level_width

