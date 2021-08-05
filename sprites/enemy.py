import pygame, random, math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos_x, start_pos_y, image) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(x = start_pos_x, y = start_pos_y)
        self.x = float(start_pos_x)
        self.y = float(start_pos_y)

        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}

    def move(self, tiles):
        self.x += self.speed_x
        self.y += self.speed_y

        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}

        self.rect.x = int(self.x)
        hit_list = pygame.sprite.spritecollide(self, tiles, False)
        for hit in hit_list:
            if self.speed_x > 0:
                self.rect.right = hit.rect.left
                self.collision_directions["right"] = True
            elif self.speed_x < 0:
                self.rect.left = hit.rect.right
                self.collision_directions["left"] = True
            self.x = self.rect.x
        
        self.rect.y = int(self.y)
        hit_list = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hit_list:
            if self.speed_y > 0:
                self.rect.bottom = tile.rect.top
                self.collision_directions["bottom"] = True
            elif self.speed_y < 0:
                self.rect.top = tile.rect.bottom
                self.collision_directions["top"] = True
            self.y = self.rect.y
            
    def draw(self, layer):
        pygame.draw.rect(layer, (0,60,200), self.rect, width=1)

    
class Ground_enemy(Enemy):
    def __init__(self, start_pos_x, start_pos_y, image) -> None:
        super().__init__(start_pos_x, start_pos_y, image)
        self.speed_x, self.speed_y = 0.5, 0.5

    def update(self, player):
        if self.collision_directions["left"] or self.collision_directions["right"]:
            self.speed_x *= -1
        # Gravity
        self.speed_y += 0.05

        if self.collision_directions["bottom"]:
            self.speed_y = 0


class Air_enemy(Enemy):
    def __init__(self, start_pos_x, start_pos_y, image) -> None:
        super().__init__(start_pos_x, start_pos_y, image)
        speed = 0.5
        angle = random.random()*6.28
        self.speed_x, self.speed_y = math.cos(angle)*speed, math.sin(angle)*speed

    def update(self, player):
        if self.collision_directions["left"] or self.collision_directions["right"]:
            self.speed_x *= -1
        if self.collision_directions["top"] or self.collision_directions["bottom"]:
            self.speed_y *= -1
            

class Follower_ground(Ground_enemy):
    def __init__(self, start_pos_x, start_pos_y, image, sight_distance) -> None:
        super().__init__(start_pos_x, start_pos_y, image)
        self.sight_distance = sight_distance
        self.wandering = True
        self.wandering_timer = 1000

    def update(self, player):
        player_position = player_position_x, player_position_y = player.rect.center
        if abs(player_position_x - self.rect.x) < self.sight_distance:
            self.wandering = False
            self.wandering_timer = 0
            if player_position_x > self.rect.x: # player is on the right side
                self.speed_x = 0.5
            elif player_position_x < self.rect.x: # player is on the left side
                self.speed_x = -0.5
            else: self.speed_x = 0
        elif self.wandering_timer <= 0:
            self.wandering = True
            self.wandering_timer = 1000
            self.speed_x = random.randint(-6,6)/10

        if self.wandering and self.wandering_timer > 0:
            self.wandering_timer -= 1
                
        if self.collision_directions["left"] or self.collision_directions["right"]:
            self.speed_x *= -1
                
class Follower_air(Air_enemy):
    def __init__(self, start_pos_x, start_pos_y, image, sight_distance) -> None:
        super().__init__(start_pos_x, start_pos_y, image)
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
