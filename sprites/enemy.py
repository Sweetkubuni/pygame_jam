import pygame, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos_x, start_pos_y, image, game) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(x = start_pos_x, y = start_pos_y)
        self.x = float(start_pos_x)
        self.y = float(start_pos_y)

        self.game = game

    def draw(self, layer):
        
        pygame.draw.rect(layer, (0,60,200), self.rect, width=1)

    
class Ground_enemy(Enemy):
    def __init__(self, start_pos_x, start_pos_y, image, game) -> None:
        super().__init__(start_pos_x, start_pos_y, image, game)
        self.speed_x, self.speed_y = 0.5, 0.5

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
    def __init__(self, start_pos_x, start_pos_y, image, game) -> None:
        super().__init__(start_pos_x, start_pos_y, image, game)
        self.speed = 5
        self.direction_vector = pygame.math.Vector2(0, 1)
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

class Follower_ground(Ground_enemy):
    def __init__(self, start_pos_x, start_pos_y, image, sight_distance, game) -> None:
        super().__init__(start_pos_x, start_pos_y, image, game)
        self.sight_distance = sight_distance

    def update(self, tiles, player):
        player_position = player_position_x, player_position_y = player.rect.center
        if ( abs(player_position_x - self.rect.x) > self.sight_distance
          or abs(player_position_y - self.rect.y) > self.sight_distance):
            super().update()
        else:
            self.move(tiles, player_position)
    
    def move(self, tiles, player_position):
        potition_vector_self = pygame.math.Vector2(self.x, self.y)
        potition_vector_player = pygame.math.Vector2(player_position)

        direction_vector = potition_vector_player - potition_vector_self
        super().move(tiles, direction_vector.normalize())

class Follower_air(Air_enemy):
    def __init__(self, start_pos_x, start_pos_y, image, sight_distance, game) -> None:
        super().__init__(start_pos_x, start_pos_y, image, game)
        self.sight_distance = sight_distance

    def update(self, tiles, player):
        player_position = player_position_x, player_position_y = player.rect.center
        if ( abs(player_position_x - self.rect.x) > self.sight_distance
          or abs(player_position_y - self.rect.y) > self.sight_distance):
            super().update()
        else:
            self.move(tiles, player_position)
    
    def move(self, tiles, player_position):
        potition_vector_self = pygame.math.Vector2(self.x, self.y)
        potition_vector_player = pygame.math.Vector2(player_position)

        self.direction_vector = potition_vector_player - potition_vector_self
        self.direction_vector.normalize_ip()
        super().move(tiles)
