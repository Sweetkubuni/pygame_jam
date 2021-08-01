import pygame, os, random

from hub import loadImage
from tilemaps.tilemap import Tile_map
from camera import Camera
from sprites.particle import Particle
from sprites.coin import Coin

class Level:
    def __init__(self, state, tilemap, background, start_x, start_y) -> None:
        self.state = state
        self.tilemap = Tile_map(self, tilemap)
        if type(background) == pygame.Surface:
            self.background = background
        else:
            self.background = loadImage(background)
        self.tiles_and_blocks, self.enemies = self.tilemap.load_tiles_and_blocks(self.state.all_animations, self.state.all_sounds, self.state.game)
        self.start_pos = self.start_pos_x, self.start_y = start_x, start_y
        self.camera = Camera(self, self.state.game.player, self.state.game.GAME_WIDTH, self.state.game.GAME_HEIGHT)
        self.particles = []
        self.state.game.player.level_init(self.state.all_animations, self.state.all_sounds, 32, 141)

    def update(self):
        self.state.game.player.update()
        self.camera.update()

        enemy_remove_list = []
        i = 0
        for enemy in self.enemies:
            if(abs(self.state.game.player.rect.y - enemy.rect.y) < 500):
                enemy.update()
        
        block_remove_list = []
        for tile in self.tiles_and_blocks.sprites():
            if(abs(self.state.game.player.rect.y - tile.rect.y) < 500):
                if tile.destructable: # The tile is a block
                    tile.update(self.state.game.player.attack_sprite, len(block_remove_list))
                    if tile.delete:
                        self.state.game.player.attack_timer = -30
                        pygame.mixer.find_channel(True).play(tile.sounds["explodeBrick"])
                        block_remove_list.append(tile)
                        self.particles.append(Particle(self.tilemap, pygame.Rect(tile.rect.centerx-5, tile.rect.centery-5, 10,10), self.state.all_animations["break particle"], False, (0,0), 2, 34, [1.047,2.094], 1.8))
                        if random.random() < 0.33:
                            self.particles.append(Coin(pygame.Rect(tile.rect.centerx-6, tile.rect.y-2, 13, 15), self.state.all_animations["coin"], 1050, 1.57, 1.3, self.state.all_sounds, self.state.game))
        block_remove_list.sort(reverse=True)
        for block in block_remove_list:
            self.tiles_and_blocks.remove(block)


        particle_remove_list = []
        i = 0
        for particle in self.particles:
            particle.update(self.state.game.player, len(particle_remove_list))
            if particle.timer >= particle.max_timer:
                particle_remove_list.append(i)
                if particle.pick_up:
                    pygame.mixer.find_channel(True).play(particle.sounds["coin"])
                    print("coin +1")
            i += 1
        particle_remove_list.sort(reverse=True)
        for i in particle_remove_list:
            self.particles.pop(i)


    def render(self):
        self.state.game.game_canvas.blit(self.background, (0, 0))
        self.state.game.player.draw()
        for tile in self.tiles_and_blocks.sprites():
            if(abs(self.state.game.player.rect.y - tile.rect.y) < 500):
                tile.draw()
        for enemy in self.enemies:
            if(abs(self.state.game.player.rect.y - enemy.rect.y) < 500):
                enemy.draw()
        for particle in self.particles:
           particle.draw()
