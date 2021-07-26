import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16,32))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x, self.y = float(x), float(y) # xL: For more presice movement, we use floats instead of rect's int
        self.speed_x, self.speed_y = 0, 0 # xL: more floats
    def update(self, game_actions, tiles):
        
        # xL: Player movement controls
        self.speed_x, self.speed_y = 0, 0
        
        if game_actions[pygame.K_RIGHT]:
            self.speed_x += 1
        if game_actions[pygame.K_LEFT]:
            self.speed_x += -1
        if game_actions[pygame.K_UP]:
            self.speed_y += -1
        if game_actions[pygame.K_DOWN]:
            self.speed_y += 1
        # xL: Player's jump botton
        if game_actions[pygame.K_z]:
            pass

        # xL: Applies the speed to the position
        self.x += self.speed_x
        self.y += self.speed_y
        
        # xL: Check collisions horizontally and then vertically
        self.rect.x = int(self.x)
        hit_list = pygame.sprite.spritecollide(self, tiles, False)

        for tile in hit_list:
            if self.speed_x > 0:
                self.rect.right = tile.rect.left
                self.speed_x = 0
            elif self.speed_x < 0:
                self.rect.left = tile.rect.right
                self.speed_x = 0
            self.x = self.rect.x
            
        self.rect.y = int(self.y)
        hit_list = pygame.sprite.spritecollide(self, tiles, False)
        
        for tile in hit_list:
            if self.speed_y > 0:
                self.rect.bottom = tile.rect.top
                self.speed_y = 0
            elif self.speed_y < 0:
                self.rect.top = tile.rect.bottom
                self.speed_y = 0
            self.y = self.rect.y
