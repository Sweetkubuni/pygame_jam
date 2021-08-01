import pygame, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos_x, start_pos_y, width, height) -> None:
        super().__init__()
        self.rect = pygame.Rect(start_pos_x, start_pos_y, width, height)
        self.x = float(start_pos_x)
        self.y = float(start_pos_y)
    
class Ground_enemy(Enemy):
        def __init__(self, start_pos_x, start_pos_y, width, height) -> None:
            super().__init__(start_pos_x, start_pos_y, width, height)
            self.speed_x, self.speed_y = 5, 5

        def update(self, tiles):
            self.x += self.speed_x
            self.y += self.speed_y

            self.rect.x = int(self.x)
            hit_list = pygame.sprite.spritecollide(self, tiles, False)
            for hit in hit_list:
                if self.speed_x > 0:
                    self.rect.right = hit.rect.left
                elif self.speed_x < 0:
                    self.rect.left = hit.rect.right
                self.speed_x *= -1
                self.x = self.rect.x
            
            self.rect.y = int(self.y)
            hit_list = pygame.sprite.spritecollide(self, tiles, False)
            for hit in hit_list:
                self.rect.bottom = hit.rect.top
                self.y = self.rect.y

class Air_enemy(Enemy):
    def __init__(self, start_pos_x, start_pos_y, width, height) -> None:
        super().__init__(start_pos_x, start_pos_y, width, height)
        self.speed = 5
        self.direction_vector = pygame.math.Vector2(random.randrange(0, 1), random.randrange(0, 1))
        self.direction_vector.normalize_ip()

    def update(self, tiles):
        self.x += self.direction_vector.x * self.speed
        self.y += self.direction_vector.y * self.speed

        self.rect.x = int(self.x)
        hit_list = pygame.sprite.spritecollide(self, tiles, False)
        for hit in hit_list:
            if self.direction_vector.x > 0:
                self.rect.right = hit.rect.left
            elif self.direction_vector.x < 0:
                self.rect.left = hit.rect.right
            self.direction_vector.reflect_ip()
            self.x = self.rect.x
        
        self.rect.y = int(self.y)
        hit_list = pygame.sprite.spritecollide(self, tiles, False)
        for hit in hit_list:
            if self.direction_vector.y > 0:
                self.rect.bottom = hit.rect.top
            elif self.direction_vector.y < 0:
                self.rect.top = hit.rect.bottom
            self.direction_vector.reflect_ip()
            self.y = self.rect.y