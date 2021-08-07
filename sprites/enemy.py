import pygame, random, math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, rect, image, offset, level_width, area_top, area_bottom) -> None:
        super().__init__()
        self.image = image
        self.rect = rect
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.offset = offset

        self.area_top, self.area_bottom = area_top, area_bottom

        self.level_width = level_width

        self.dead = False

        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}

    def move(self, tiles):
        self.x += self.speed_x
        self.y += self.speed_y

        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}

        self.rect.x = int(self.x)

        # Screen boundaries
        if self.rect.x < 0 and self.speed_x < 0:
            self.rect.left = 0
            self.collision_directions["left"] = True
            self.x = self.rect.x
        if self.rect.right > self.level_width and self.speed_x > 0:
            self.rect.right = self.level_width
            self.collision_directions["right"] = True
            self.x = self.rect.x
            
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

        # Move to another area different to current one -> kill it! (for now)
        if self.rect.top < self.area_top or self.area_bottom > self.area_bottom:
            self.dead = True
            
    def draw(self, layer):
        layer.blit(self.image, (self.rect.x-self.offset[0], self.rect.y-self.offset[1]))
        #pygame.draw.rect(layer, (0,60,200), self.rect, width=1)

    def check_dead(self, attack_sprite):
        if attack_sprite != None:
            if self.rect.colliderect(attack_sprite.rect):
                self.dead = True

class Ground_enemy(Enemy):
    def __init__(self, rect, image, offset, level_width, area_top, area_bottom) -> None:
        super().__init__(rect, image, offset, level_width, area_top, area_bottom)
        self.speed_x, self.speed_y = 0.5, 0

    def update(self, player):
        if self.collision_directions["left"] or self.collision_directions["right"]:
            self.speed_x *= -1
        # Gravity
        self.speed_y += 0.05

        if self.collision_directions["bottom"]:
            self.speed_y = 0


class Air_enemy(Enemy):
    def __init__(self, rect, image, offset, level_width, area_top, area_bottom) -> None:
        super().__init__(rect, image, offset, level_width, area_top, area_bottom)
        speed = 0.5
        angle = random.random()*6.28
        self.speed_x, self.speed_y = math.cos(angle)*speed, math.sin(angle)*speed

    def update(self, player):
        if self.collision_directions["left"] or self.collision_directions["right"]:
            self.speed_x *= -1
        if self.collision_directions["top"] or self.collision_directions["bottom"]:
            self.speed_y *= -1
            

class Follower_ground(Ground_enemy):
    def __init__(self, rect, image, offset, sight_distance, level_width, area_top, area_bottom) -> None:
        super().__init__(rect, image, offset, level_width, area_top, area_bottom)
        self.sight_distance = sight_distance
        self.wandering = True
        self.wandering_timer = 100
        self.speed = 0.6
        self.speed_x, self.speed_y = 0.6, 0

    def update(self, player):
        player_position = player_position_x, player_position_y = player.rect.center
        if abs(player_position_x - self.rect.x) < self.sight_distance and abs(player_position_y - self.rect.y) < self.sight_distance:
            self.wandering = False
            self.wandering_timer = 0
            if player_position_x > self.rect.x: # player is on the right side
                self.speed_x = self.speed
            elif player_position_x < self.rect.x: # player is on the left side
                self.speed_x = -self.speed
            else: self.speed_x = 0
        elif self.wandering_timer <= 0:
            self.wandering = True
            self.wandering_timer = 100
            self.speed_x = random.randint(-4,4)/10

        if self.wandering and self.wandering_timer > 0:
            self.wandering_timer -= 1

        # Gravity
        self.speed_y += 0.05
        if self.collision_directions["bottom"]:
            self.speed_y = 0
            
                
class Follower_air(Air_enemy):
    def __init__(self, rect, image, offset, sight_distance, level_width, area_top, area_bottom) -> None:
        super().__init__(rect, image, offset, level_width, area_top, area_bottom)
        self.sight_distance = sight_distance
        self.speed = 0.6

    def update(self, player):
        player_position = player_position_x, player_position_y = player.rect.center
        if player_position == self.rect.center:
            self.speed_x, self.speed_y = 0, 0
        if abs(player_position_x - self.rect.x) < self.sight_distance and abs(player_position_y - self.rect.y) < self.sight_distance:
            angle = math.atan2(player_position_y - self.rect.centery, player_position_x - self.rect.centerx)
            self.speed_x, self.speed_y = math.cos(angle)*self.speed, math.sin(angle)*self.speed
        else:
            super().update(player)
