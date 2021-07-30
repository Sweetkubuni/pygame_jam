import pygame

class Camera:
    def __init__(self, level, target, width, height) -> None:
        self.level = level
        
        self.width = width
        self.height = height
        self.target = target
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def apply(self, sprite):
        return sprite.rect.move(self.rect.topleft)

    def update(self, **kwargs):
        self.target = kwargs.get("new_target", self.target)
        
        x = -self.target.rect.x + self.width/2
        y = -self.target.rect.y + self.height/2
        #print("target x: " + str(self.target.rect.x) + " target y: " + str(self.target.rect.y) + " | camera x: " + str(x) + " camera y: " + str(y))
        #print()

        self.rect = pygame.Rect(x, y, self.width, self.height)
