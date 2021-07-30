import pygame, os
from hub import loadImage
from tilemaps.tilemap import Tile_map
from camera import Camera
from sprites.particle import Particle

class Level:
    def __init__(self, state, tilemap, background, start_x, start_y) -> None:
        self.state = state
        self.tilemap = Tile_map(self, tilemap)
        if type(background) == pygame.Surface:
            self.background = background
        else:
            self.background = loadImage(background)
        self.tiles_and_blocks = self.tilemap.load_tiles_and_blocks()
        self.start_pos = self.start_pos_x, self.start_y = start_x, start_y
        self.camera = Camera(self, self.state.game.player, self.state.game.GAME_WIDTH, self.state.game.GAME_HEIGHT)
        self.particles = []

    def update(self):
        self.state.game.player.update()
        self.camera.update()
        
        block_remove_list = []
        for tile in self.tiles_and_blocks.sprites():
            if tile.destructable: # The tile is a block
                tile.update(self.state.game.player.rect)
                if tile.delete:
                    block_remove_list.append(tile)
                    self.particles.append(Particle(self.tilemap, tile.rect, self.state.all_animations["leaf particle"], True, (0,0), 2, 60, [1.047,2.094], 2))
            for block in block_remove_list:
                self.tiles_and_blocks.remove(block)


        particle_remove_list = []
        i = 0
        for particle in self.particles:
            if particle.timer >= particle.max_timer:
                particle_remove_list.append(i)
            i += 1
        particle_remove_list.sort(reverse=True)
        for i in particle_remove_list:
            self.particles.pop(i)


    def render(self):
        self.state.game.game_canvas.blit(self.background, (0, 0))
        self.state.game.player.draw()
        for tile in self.tiles_and_blocks.sprites():
            tile.draw()
        for particle in self.particles:
           particle.draw()
