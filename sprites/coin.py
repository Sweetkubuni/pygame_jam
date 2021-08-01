import pygame, math

class Coin(pygame.sprite.Sprite):
    def __init__(self, rect, animation, max_timer, angle, speed, all_sounds, game):
        super().__init__()
        self.rect = rect
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        
        self.speed_x, self.speed_y = speed*math.cos(angle), speed*-math.sin(angle)
        self.game = game

        self.pick_up = False

        self.timer = 0
        self.max_timer = max_timer

        self.animations = [[animation, True, (-2,-2)]]
        self.ani_timer = 0
        self.ani_frame = 0
        self.current_ani = self.animations[0]
        self.flip = False

        self.sounds = {"coin": all_sounds["coin"]}
        
    def update(self, player_sprite, previous_delete):

        self.timer += self.game.delta_time

        if self.rect.colliderect(player_sprite.rect) and not(self.pick_up):
            self.pick_up = True
            self.timer = self.max_timer

        # pseudo gravity
        self.speed_y += 0.05 * self.game.delta_time
        
        self.x += self.speed_x * self.game.delta_time
        self.y += self.speed_y * self.game.delta_time       
        
        self.rect.x = int(self.x)
        hit_list = pygame.sprite.spritecollide(self, self.game.state_stack[-1].current_level.tiles_and_blocks, False)

        for tile in hit_list:
            if self.speed_x > 0:
                self.rect.right = tile.rect.left
                self.speed_x = 0
            elif self.speed_x < 0:
                self.rect.left = tile.rect.right
                self.speed_x = 0
            self.x = self.rect.x

        self.rect.y = int(self.y)
        hit_list = pygame.sprite.spritecollide(self, self.game.state_stack[-1].current_level.tiles_and_blocks, False)

        for tile in hit_list:
            if self.speed_y > 0:
                self.rect.bottom = tile.rect.top
                self.speed_x, self.speed_y = 0, 0
            elif self.speed_y < 0:
                self.rect.top = tile.rect.bottom
                self.speed_x, self.speed_y = 0, 0
            self.y = self.rect.y
            
    def draw(self):
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
        #pygame.draw.rect(self.game.game_canvas, (0,60,200), self.game.state_stack[-1].current_level.camera.apply(self), width=1)
