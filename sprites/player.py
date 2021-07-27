import pygame
from config.config import colours

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x , y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((16,32))
        self.image.fill(colours["red"])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x, self.y = float(x), float(y) # xL: For more presice movement, we use floats instead of rect's int
        self.speed_x, self.speed_y = 0, 0 # xL: more floats
        self.grounded = False
        self.jump_height = 80;
        self.gravity  = 10
        self.jumping = False
        self.jump_delay = -1;
        self.start_height = 0;
    def update(self):
        # xL: Player movement controls
        self.speed_x = 0
        if self.game.actions[pygame.K_RIGHT]:
            self.speed_x += 1
        if self.game.actions[pygame.K_LEFT]:
            self.speed_x += -1
        if self.game.actions[pygame.K_UP] or self.game.actions[pygame.K_SPACE]:
            if self.grounded and self.jump_delay < 0:
                self.jumping = True
                self.grounded = False
                self.jump_delay =  60
                self.start_height = self.y

        if self.game.actions[pygame.K_DOWN]:
            self.speed_y += 1
        # xL: Player's jump botton
        if self.game.actions[pygame.K_z]:
            pass

        self.jump_delay -= self.game.delta_time
        if self.jumping:
            self.speed_y = -100/30
            if (self.start_height - self.y) >= self.jump_height:
                self.jumping = False
        else:
            self.speed_y += self.gravity /30

        # xL: Applies the speed to the position
        self.x += self.speed_x * self.game.delta_time
        self.y += self.speed_y * self.game.delta_time

        self.rect.x = int(self.x)
        hit_list = pygame.sprite.spritecollide(self, self.game.state_stack[-1].current_level.tiles, False)

        for tile in hit_list:
            if self.speed_x > 0:
                self.rect.right = tile.rect.left
                self.speed_x = 0
            elif self.speed_x < 0:
                self.rect.left = tile.rect.right
                self.speed_x = 0
            self.x = self.rect.x

        self.rect.y = int(self.y)
        hit_list = pygame.sprite.spritecollide(self, self.game.state_stack[-1].current_level.tiles, False)

        collide_tolerance = 5
        for tile in hit_list:
            if abs(tile.rect.bottom - self.rect.top) < collide_tolerance:
                self.jumping = False
            if abs(tile.rect.top - self.rect.bottom) < collide_tolerance:
                self.grounded = True
            if self.speed_y > 0:
                self.rect.bottom = tile.rect.top
                self.speed_y = 0
            elif self.speed_y < 0:
                self.rect.top = tile.rect.bottom
                self.speed_y = 0
            self.y = self.rect.y

    def draw(self):
        self.game.game_canvas.blit(self.image, self.game.state_stack[-1].current_level.camera.apply(self))
