import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, font_path: str, font_size: int, content: str, colour: tuple, center_x, center_y) -> None:
        super().__init__()
        self.font = pygame.font.Font(font_path, font_size)
        self.image = self.font.render(content, True, colour)
        self.rect = self.image.get_rect(center = (center_x, center_y))