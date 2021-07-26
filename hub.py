import pygame, os


def loadImage(image_path, size = None):
    print(image_path)
    if size != None:
        return pygame.transform.scale(pygame.image.load(image_path).convert(), size)
    return pygame.image.load(image_path)

assets = os.path.join("assets", "images", "tiles")

tile_keys = {
    0: loadImage(os.path.join(assets, "dirt.jpg")),
    1: loadImage(os.path.join(assets, "grass.jpg")),
    2: loadImage(os.path.join(assets, "block.png")),
    3: loadImage(os.path.join(assets, "brick.png")),
    4: loadImage(os.path.join(assets, "mushroom.png"))
}
if __name__ == "__main__":
    
    from game import Game
    game = Game()
    while game.running:
        game.new()