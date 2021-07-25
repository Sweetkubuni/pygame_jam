import pygame, os, csv
from sprites.tile import Tile


class Tile_map:
    def __init__(self, csv_filepath, tile_image_paths: dict):
        self.csv_filepath = csv_filepath
        self.tile_image_paths: dict = tile_image_paths
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0

    def read_csv(self):
        tilemap = []
        with open(os.path.join(self.csv_filepath), "r", newline="") as map_csv_file:
            reader = csv.reader(map_csv_file)
            tilemap = [[int(tile) for tile in row] for row in reader]
        return tilemap
    
    def load_tiles(self):
        tiles = pygame.sprite.Group()
        tile_map_template = self.read_csv()
        x, y = 0, 0
        for row in tile_map_template:
            x = 0
            for tile in row:
                for tile_key in self.tile_image_paths:
                    if tile == tile_key:
                        tiles.add(Tile(self.tile_image_paths[tile_key], x * self.tile_size, y * self.tile_size))
                x += 1
            y += 1
        self.width, self.height = x * self.tile_size, y * self.tile_size
        return tiles