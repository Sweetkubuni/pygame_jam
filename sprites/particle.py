import pygame, math

class Particle():
    def __init__(self, tilemap, rect, animation: list, loop: bool, offset: tuple, particle_num: int, max_timer: int, interval: list, speed: float):

        self.tilemap = tilemap
        self.rect = rect
        self.max_timer = max_timer

        self.ani_timer = 0
        self.ani_frame = 0

        self.animation = [animation, loop, offset]  # [[animation], Loop boolean, (x,y render offset)]
        
        self.particles = []

        for i in range(particle_num):
            try:
                angle = interval[0] + (interval[1] - interval[0])*i/(particle_num-1)
            except ZeroDivisionError: angle = interval[0]
            sprite = pygame.sprite.Sprite()
            sprite.rect = self.rect
            sprite.rect.topleft = self.rect.topleft
            self.particles.append([sprite, rect.x, rect.y, speed*math.cos(angle), speed*-math.sin(angle)])
            
            i += 1
            
        self.timer = 0

    def draw(self):
        for particle in self.particles:           
            particle[1] += particle[3]
            particle[2] += particle[4]
            # pseudo gravity
            particle[4] += 0.05

            particle[0].rect.x, particle[0].rect.y = particle[1], particle[2]

            self.tilemap.level.state.game.game_canvas.blit(self.animation[0][self.ani_frame][0], self.tilemap.level.camera.apply(particle[0]))
            #pygame.draw.rect(layer, (250,0,0), self.rect)
            
        self.timer += 1

        if self.ani_timer < self.animation[0][self.ani_frame][1]:
            self.ani_timer += 1
        else:
            self.ani_timer = 0
            self.ani_frame += 1
        if self.ani_frame >= len(self.animation[0]):
            self.ani_timer, self.ani_frame = 0, 0
