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
        self.tiles_and_blocks = self.tilemap.load_tiles_and_blocks(self.state.all_animations, self.state.all_sounds)
        self.start_pos = self.start_pos_x, self.start_y = start_x, start_y
        self.camera = Camera(self, self.state.game.player, self.state.game.GAME_WIDTH, self.state.game.GAME_HEIGHT)
        self.particles = []
        self.state.game.player.level_init(self.state.all_animations, self.state.all_sounds, 32, 141)

    def update(self):
        self.state.game.player.update()
        self.camera.update()
        
        block_remove_list = []
        for tile in self.tiles_and_blocks.sprites():
            if tile.destructable: # The tile is a block
                tile.update(self.state.game.player.rect)
                if tile.delete:
                    pygame.mixer.find_channel(True).play(tile.sounds["explodeBrick"])
                    block_remove_list.append(tile)
                    self.particles.append(Particle(self.tilemap, pygame.Rect(tile.x, tile.y, 10,10), self.state.all_animations["break particle"], False, (0,0), 2, 34, [1.047,2.094], 1.8))
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
