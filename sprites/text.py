import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, font_path: str, font_size: int, content: str, colour: tuple, anti_ailiasing: bool, x, y, is_centered: bool) -> None:
        super().__init__()
        self.font = pygame.font.Font(font_path, font_size)
        self.anti_aliasing = anti_ailiasing
        self.update(content = content, colour = colour, is_centered = is_centered, x = x, y = y)
    
    def update(self, content = None, colour = None, is_centered = None, x = None, y = None):
        if content != None: self.content = content
        if colour != None: self.colour = colour
        if is_centered != None: self.is_centered = is_centered
        if x != None: self.x = x
        if y != None: self.y = y

        self.image = self.font.render(self.content, self.anti_aliasing, self.colour)
        if self.is_centered:
            self.rect = self.image.get_rect(center = (self.x, self.y))
        else:
            self.rect = self.image.get_rect(topleft = (self.x, self.y))