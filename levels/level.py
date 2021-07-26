import pygame, os
from hub import loadImage
from tilemaps.tilemap import Tile_map


class Level:
    def __init__(self, state, tilemap, background, start_x, start_y) -> None:
        self.state = state
        self.tilemap = Tile_map(tilemap)
        if type(background) == pygame.Surface:
            self.background = background
        else:
            self.background = loadImage(background)
        self.tiles = self.tilemap.load_tiles()
        self.start_pos = self.start_pos_x, self.start_y = start_x, start_y

    def update(self):
        self.state.game.player.update()

    def render(self):
        self.state.game.game_canvas.blit(self.background, (0, 0))
        self.state.game.player.draw()
        self.tiles.draw(self.state.game.game_canvas)