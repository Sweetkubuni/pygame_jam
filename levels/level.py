import pygame, os, random

from hub import loadImage
from tilemaps.tilemap import Tile_map
from camera import Camera
from sprites.particle import Particle
from sprites.coin import Coin
from config.config import colours
from sprites.text import Text
from states.gameover import Game_over


class Level:
    def __init__(self, state, tilemap, background, start_x, start_y) -> None:
        self.state = state
        self.tilemap = Tile_map(self, tilemap)
        self.background = background
        self.current_area = 0
        self.areas, width, height = self.tilemap.load_tiles_and_blocks(self.state.all_animations, self.state.all_sounds, self.state.game)
        # 0 -> Tiles and blocks, 1 -> Enemies
        self.start_x, self.start_y = start_x, start_y
        self.level_surface = pygame.Surface((width, height))
        
        self.particles = []
        self.state.game.player.level_init(self.state.all_animations, self.state.all_sounds, width)
      
        self.camera = Camera(self.state.game.player, self.state.game.GAME_WIDTH, self.state.game.GAME_HEIGHT, self.level_surface)
        self.camera_surface = pygame.Surface((self.state.game.GAME_WIDTH, self.state.game.GAME_HEIGHT))

        self.current_fps = Text(self.camera_surface, os.path.join(self.state.game.font_directory,"alphbeta.ttf"), 22, str(self.state.game.clock.get_fps()).split(".")[0], colours["black"], False, 20, 20, False)
        
    def update(self):
        # CURRENT AREA UPDATE --------------------------------------------------
        self.state.game.player.update(self.areas[self.current_area][0])
        self.state.game.player.check_dead(self.areas[self.current_area][1].sprites())

        if self.state.game.player.dead and self.state.game.player.dead_timer < 0:
            #print("you died")
            game_over = Game_over(self.state.game, self.state.game.player.coins, self.state.game.player.kills, self.state.game.player.y)
            game_over.enter_state()
        self.camera.update(self.state.game.player)

        enemy_remove_list = []
        for enemy in self.areas[self.current_area][1]:
            if(abs(self.state.game.player.rect.y - enemy.rect.y) < 500):
                enemy.move(self.areas[self.current_area][0])
                enemy.update(self.state.game.player)
                enemy.check_dead(self.state.game.player.attack_sprite)
            if enemy.dead:
                enemy_remove_list.append(enemy)
                self.state.game.player.kills += 1
                self.particles.append(Coin(pygame.Rect(enemy.rect.centerx-6, enemy.rect.y-6, 13, 15), self.state.all_animations["coin"], 450, 1.57, 1.5, self.state.all_sounds, self.state.game))
                self.particles.append(Coin(pygame.Rect(enemy.rect.centerx-6, enemy.rect.y-6, 13, 15), self.state.all_animations["coin"], 450, 1.37, 1.3, self.state.all_sounds, self.state.game))
                self.particles.append(Coin(pygame.Rect(enemy.rect.centerx-6, enemy.rect.y-6, 13, 15), self.state.all_animations["coin"], 450, 1.77, 1, self.state.all_sounds, self.state.game))
        enemy_remove_list.sort(reverse=True)
        for enemy in enemy_remove_list:
            self.areas[self.current_area][1].remove(enemy)
            
        block_remove_list = []
        for tile in self.areas[self.current_area][0].sprites():
            if(abs(self.state.game.player.rect.y - tile.rect.y) < 500):
                if tile.destructable: # The tile is a block
                    tile.update(self.state.game.player.attack_sprite, len(block_remove_list))
                    if tile.delete:
                        self.state.game.player.attack_timer = -30
                        pygame.mixer.find_channel(True).play(tile.sounds["explodeBrick"])
                        block_remove_list.append(tile)
                        self.particles.append(Particle(self.tilemap, pygame.Rect(tile.rect.centerx-5, tile.rect.centery-5, 10,10), self.state.all_animations["break particle"], False, (0,0), 2, 34, [1.047,2.094], 1.8))
                        if random.random() < 0.33:
                            self.particles.append(Coin(pygame.Rect(tile.rect.centerx-6, tile.rect.y-2, 13, 15), self.state.all_animations["coin"], 450, 1.57, 1.3, self.state.all_sounds, self.state.game))
        block_remove_list.sort(reverse=True)
        for block in block_remove_list:
            self.areas[self.current_area][0].remove(block)

        # NEXT AREA UPDATE --------------------------------------------------
        if self.state.game.player.y > 30*16*(self.current_area + 0.5):
            self.state.game.player.update(self.areas[self.current_area+1][0])
            self.state.game.player.check_dead(self.areas[self.current_area+1][1].sprites())

            if self.state.game.player.dead and self.state.game.player.dead_timer < 0:
                #print("you died")
                game_over = Game_over(self.state.game, self.state.game.player.coins, self.state.game.player.kills, self.state.game.player.y)
                game_over.enter_state()
            self.camera.update(self.state.game.player)

            enemy_remove_list = []
            for enemy in self.areas[self.current_area+1][1]:
                enemy.move(self.areas[self.current_area+1][0])
                enemy.update(self.state.game.player)
                enemy.check_dead(self.state.game.player.attack_sprite)
                if enemy.dead:
                    enemy_remove_list.append(enemy)
                    self.state.game.player.kills += 1
                    self.particles.append(Coin(pygame.Rect(enemy.rect.centerx-6, enemy.rect.y-6, 13, 15), self.state.all_animations["coin"], 450, 1.57, 1.5, self.state.all_sounds, self.state.game))
                    self.particles.append(Coin(pygame.Rect(enemy.rect.centerx-6, enemy.rect.y-6, 13, 15), self.state.all_animations["coin"], 450, 1.37, 1.3, self.state.all_sounds, self.state.game))
                    self.particles.append(Coin(pygame.Rect(enemy.rect.centerx-6, enemy.rect.y-6, 13, 15), self.state.all_animations["coin"], 450, 1.77, 1, self.state.all_sounds, self.state.game))
            enemy_remove_list.sort(reverse=True)
            for enemy in enemy_remove_list:
                self.areas[self.current_area+1][1].remove(enemy)
                
            block_remove_list = []
            for tile in self.areas[self.current_area+1][0].sprites():
                if tile.destructable: # The tile is a block
                    tile.update(self.state.game.player.attack_sprite, len(block_remove_list))
                    if tile.delete:
                        self.state.game.player.attack_timer = -30
                        pygame.mixer.find_channel(True).play(tile.sounds["explodeBrick"])
                        block_remove_list.append(tile)
                        self.particles.append(Particle(self.tilemap, pygame.Rect(tile.rect.centerx-5, tile.rect.centery-5, 10,10), self.state.all_animations["break particle"], False, (0,0), 2, 34, [1.047,2.094], 1.8))
                        if random.random() < 0.33:
                            self.particles.append(Coin(pygame.Rect(tile.rect.centerx-6, tile.rect.y-2, 13, 15), self.state.all_animations["coin"], 450, 1.57, 1.3, self.state.all_sounds, self.state.game))
            block_remove_list.sort(reverse=True)
            for block in block_remove_list:
                self.areas[self.current_area+1][0].remove(block)

        # CHANGE AREA BY 1 PLACE --------------------------------------------------
        if self.state.game.player.y > 30*16*(self.current_area + 1.5):
            self.current_area += 1
        
        # PARTICLES ALL AREAS --------------------------------------------------
        particle_remove_list = []
        i = 0
        for particle in self.particles:
            particle.update(self.areas[self.current_area][0], self.state.game.player, len(particle_remove_list))
            if particle.timer >= particle.max_timer:
                particle_remove_list.append(i)
                if particle.pick_up:
                    pygame.mixer.find_channel(True).play(particle.sounds["coin"])
                    #print("coin +1")
                    self.state.game.player.coins += 1
            i += 1
        particle_remove_list.sort(reverse=True)
        for i in particle_remove_list:
            self.particles.pop(i)


    def render(self):
        self.level_surface.fill(colours["dark brown"], rect=self.camera.rect)
        self.level_surface.blit(self.background, (0, 0))
        
        for tile in self.areas[self.current_area][0].sprites():
            if (abs(self.state.game.player.rect.y - tile.rect.y) < 300) and (abs(self.state.game.player.rect.x - tile.rect.x) < 300):
                tile.draw(self.level_surface)
        for enemy in self.areas[self.current_area][1]:
            if (abs(self.state.game.player.rect.y - enemy.rect.y) < 300) and (abs(self.state.game.player.rect.x - enemy.rect.x) < 300):
                enemy.draw(self.level_surface)

        for tile in self.areas[self.current_area+1][0].sprites():
            tile.draw(self.level_surface)
        for enemy in self.areas[self.current_area+1][1]:
            enemy.draw(self.level_surface)

        self.state.game.player.draw(self.level_surface)
        
        for particle in self.particles:
           particle.draw(self.level_surface)

        self.camera_surface.blit(self.level_surface, (0,0), area=(self.camera.rect.x, self.camera.rect.y, self.camera.width, self.camera.height))

        # UI
        self.current_fps.update(content=str(self.state.game.clock.get_fps()).split(".")[0])
        
        self.state.game.game_canvas.blit(self.camera_surface, (0,0))
