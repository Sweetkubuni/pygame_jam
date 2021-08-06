import pygame, os
from tilemaps.app_single_output import app

def loadImage(image_path, size = None):
    if size != None:
        return pygame.transform.scale(pygame.image.load(image_path).convert(), size)
    return pygame.image.load(image_path)

if __name__ == "__main__":
    from game import Game
    game = Game()
    while game.running:
        app()
        game.new()
