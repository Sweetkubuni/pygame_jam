import pygame
from config.config import colours

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x , y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((8,20))
        self.image.fill(colours["green"])
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
        
        self.attacking = False
        self.attacking_down = False
        self.attack_timer = 0
        self.attack_sprite = None
        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}
        self.inputs = {"right": False, "left": False, "down": False, "jump": False, "attack": False}
        
        

    def level_init(self, all_animations, all_sounds, x, y):
        self.animations = [[all_animations["player idle"], True, (10,8)], # INDEX 0
                           [all_animations["player run"], True, (10,8)], # INDEX 1
                           [all_animations["player jump"], False, (10,8)], # INDEX 2
                           [all_animations["player fall"], False, (10,8)], # INDEX 3
                           [all_animations["player attack"], False, (6,8)], # INDEX 4
                           ]
        self.ani_timer = 0
        self.ani_frame = 0
        self.current_ani = self.animations[0] # set player idle as initial animation
        self.flip = False # horizontal flip

        self.sounds = {"jumpy": all_sounds["jumpy"]}

        self.x, self.y = x, y
        
    def update(self):
        # xL: Player movement controls
        self.speed_x = 0
        
        self.inputs = {"right": False, "left": False, "down": False, "jump": False, "attack": False}
        
        if self.game.actions[pygame.K_RIGHT]:
            self.speed_x += 1
            self.inputs["right"] = True
        if self.game.actions[pygame.K_LEFT]:
            self.speed_x += -1
            self.inputs["left"] = True
        if self.game.actions[pygame.K_DOWN]:
            self.inputs["down"] = True
        if self.game.actions[pygame.K_UP] or self.game.actions[pygame.K_SPACE]:
            self.inputs["jump"] = True
        if self.game.actions[pygame.K_z]:
            self.inputs["attack"] = True

            
        # Animation orientation
        if self.inputs["right"]:
            self.flip = False
            if self.grounded and not(self.attacking):
                self.change_animation(self.animations[1])
            
        if self.inputs["left"]:
            self.flip = True
            if self.grounded and not(self.attacking):
                self.change_animation(self.animations[1])

        # Attack
        if self.inputs["attack"] and not(self.attacking):
            self.attacking = True
            self.attack_timer = 61
            if self.inputs["down"]:
                self.attacking_down = True
                self.attack_sprite = pygame.sprite.Sprite()
                self.attack_sprite.rect = pygame.rect.Rect(self.rect.x+5, self.rect.y+22, 10, 10)
            elif self.flip: # atk left
                self.change_animation(self.animations[4])
                self.current_ani[2] = (10,8)
                self.attack_sprite = pygame.sprite.Sprite()
                self.attack_sprite.rect = pygame.rect.Rect(self.rect.x-13, self.rect.y+5, 10, 10)
            else: # atk right
                self.change_animation(self.animations[4])
                self.current_ani[2] = (12,8)
                self.attack_sprite = pygame.sprite.Sprite()
                self.attack_sprite.rect = pygame.rect.Rect(self.rect.x+13, self.rect.y+5, 10, 10)

        if self.attacking:
            self.attack_timer -= self.game.delta_time
            if self.attacking_down and self.attack_timer > 0:
                self.attack_sprite.rect.topleft = (self.rect.x-2, self.rect.y+20)
            elif self.flip and self.attack_timer > 0:
                self.attack_sprite.rect.topleft = (self.rect.x - 10, self.rect.y+5)
            elif self.attack_timer > 0:
                self.attack_sprite.rect.topleft = (self.rect.x + 10, self.rect.y+5)

        if self.attack_timer < 0:
            self.attack_sprite = None
            if self.attack_timer < -60:
                self.attacking = False
                self.attacking_down = False

        # Return to idle
        if self.speed_x == 0 and self.grounded and not(self.attacking):
            self.change_animation(self.animations[0])

        # Jump code
        if self.inputs["jump"] and self.grounded and self.jump_delay < 0:
            self.jumping = True
            pygame.mixer.find_channel(True).play(self.sounds["jumpy"])
            if not(self.attacking):
                self.change_animation(self.animations[2])
            self.grounded = False
            self.jump_delay =  60
            self.start_height = self.y
                

        self.jump_delay -= self.game.delta_time
        if self.jumping:
            self.speed_y = -100/30
            if not(self.inputs["jump"]) and self.jump_delay < 55:
                self.jumping = False
                if not(self.attacking):
                    self.change_animation(self.animations[3])
                self.grounded
                self.jump_delay =0
            if (self.start_height - self.y) >= self.jump_height:
                self.jumping = False
                if not(self.attacking):
                    self.change_animation(self.animations[3])
                self.grounded
                self.jump_delay = 0
        else:
            self.speed_y += self.gravity /30

        

        # xL: Applies the speed to the position
        self.x += self.speed_x * self.game.delta_time
        self.y += self.speed_y * self.game.delta_time

        # Collision direction from the player reference point
        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}
        
        self.rect.x = int(self.x)
        hit_list = pygame.sprite.spritecollide(self, self.game.state_stack[-1].current_level.tiles_and_blocks, False)

        for tile in hit_list:
            if self.speed_x > 0:
                self.rect.right = tile.rect.left
                self.speed_x = 0
                self.collision_directions["right"] = True
            elif self.speed_x < 0:
                self.rect.left = tile.rect.right
                self.speed_x = 0
                self.collision_directions["left"] = True
            self.x = self.rect.x

        self.rect.y = int(self.y)
        hit_list = pygame.sprite.spritecollide(self, self.game.state_stack[-1].current_level.tiles_and_blocks, False)

        collide_tolerance = 5
        for tile in hit_list:
            if abs(tile.rect.bottom - self.rect.top) < collide_tolerance:
                self.jumping = False
            if abs(tile.rect.top - self.rect.bottom) < collide_tolerance:
                self.grounded = True
            if self.speed_y > 0:
                self.rect.bottom = tile.rect.top
                self.speed_y = 0
                self.collision_directions["bottom"] = True
            elif self.speed_y < 0:
                self.rect.top = tile.rect.bottom
                self.speed_y = 0
                self.collision_directions["top"] = True
            self.y = self.rect.y

    def change_animation(self, new_ani):
        if self.current_ani != new_ani:
            self.previous_ani = self.current_ani
            self.ani_timer = 0
            self.ani_frame = 0
            self.current_ani = new_ani

    def draw(self):

        # applying offset to the animation
        temp_rect = self.game.state_stack[-1].current_level.camera.apply(self)
        temp_rect.x -= self.current_ani[2][0]
        temp_rect.y -= self.current_ani[2][1]
            
        if self.current_ani[0][0][1] == 0: # no animation
            self.game.game_canvas.blit(pygame.transform.flip(self.current_ani[0][0][0], self.flip, False), temp_rect)
        else:
            self.game.game_canvas.blit(pygame.transform.flip(self.current_ani[0][self.ani_frame][0], self.flip, False), temp_rect)
            if self.ani_timer < self.current_ani[0][self.ani_frame][1]:
                self.ani_timer += self.game.delta_time
            else:
                self.ani_timer = 0
                self.ani_frame += 1
            if self.ani_frame >= len(self.current_ani[0]):
                if self.current_ani[1] == True:
                    self.ani_timer, self.ani_frame = 0, 0
                else: self.change_animation(self.previous_ani)
        pygame.draw.rect(self.game.game_canvas, (0,60,200), self.game.state_stack[-1].current_level.camera.apply(self), width=1)
        if self.attack_sprite != None:
            pygame.draw.rect(self.game.game_canvas, (215,10,30), self.game.state_stack[-1].current_level.camera.apply(self.attack_sprite), width=1)
