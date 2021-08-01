import configparser
import csv
import math
import random
import time

def create_underground_dirt_area(width, height, dirt_key):
    area = []
    for i in range(0, height):
        area.append([dirt_key]*width)
    return area

def create_room(area, fw, fh, **kwargs):
    min_w = kwargs['min_w']
    max_w = kwargs['max_w']
    min_h = kwargs['min_h']
    max_h = kwargs['max_h']
    w = random.choice([i for i in range(min_w, max_w)])
    h = random.choice([i for i in range(min_h, max_h)])
    n_cols = int(math.ceil(fw/w))
    n_rows = int(math.ceil(fh/h))
    x = random.choice([i for i in range(0, n_cols - 1)])
    y = random.choice([i for i in range(0, n_rows - 1)])
    p_x = x * w;
    p_y = y * h;

    config = configparser.ConfigParser()
    config.read('settings.ini')

    world = config['world']
    p_h = p_y + h
    if p_h > int(world['depth_section_height']):
        p_h -= (p_h - int(world['depth_section_height']))
    p_w = p_x + w
    if p_w > int(world['field_width']):
        p_w -= (p_w - int(world['field_width']))
    for i in range(p_y, p_h):
        for j in range(p_x, p_w):
            area[i][j] = -1

    enemies = kwargs['enemies']
    gap = 0
    gap_width = 1
    for enemy_key in enemies:
        e_y = p_y
        e_x = p_x + (gap * gap_width)
        if e_x > int(world['field_width']):
            e_x -= (e_x - int(world['field_width']))
        if e_y > int(world['depth_section_height']):
            e_y -= (e_y - int(world['depth_section_height']))
        print(f'e_x:{e_x} e_y:{e_y}')
        area[e_y][e_x] = enemy_key
        gap += 1

def app():
    config = configparser.ConfigParser()
    config.read('settings.ini')

    world = config['world']
    field_width = int(world['field_width'])
    depth_height = int(world['depth_section_height'])
    sky_height = int(world['sky_height'])

    """
        this generates the starting area; so... no enemies!!!
    """

    with open('area_0.csv', 'w', newline='') as csvfile:
        areawriter = csv.writer(csvfile, delimiter=',')

        for i in range(0, sky_height):
            areawriter.writerow([-1]*field_width)

        areawriter.writerow([1]*field_width)

        for i in range(0, depth_height - sky_height - 1):
            areawriter.writerow([0]*field_width)

    num_enemies = int(world['num_enemies'])
    enemies = []
    for i in range(0, num_enemies):
        enemies.append(config[f'enemy_{i}'])
    sorted(enemies, key=lambda enemy: int(enemy['difficulty']))

    room = config['room']
    minimum_space_w = int(room['minimum_space_w'])
    minimum_space_h = int(room['minimum_space_h'])
    maximum_space_w = int(room['maximum_space_w'])
    maximum_space_h = int(room['maximum_space_h'])

    """
        the set of areas slowly introduces each new enemy;
        so,player can get use to it.

        1) gap region with just the single new enemy
        2) further down new enemy in large groups (1 to N) randomly
        3) last is new enemy mix with older previous experienced enemies
    """
    encountered = []
    area_counter = 1
    for enemy in enemies:
        # create fresh area
        area = create_underground_dirt_area(field_width, depth_height, 0)
        #get enemy key
        encountered.append(int(enemy['key_value']))
        # choose how many rooms we want in the dirt
        num_rooms = random.choice([i for i in range(int(world['min_rooms']), int(world['max_rooms']))])
        print({'min_w': minimum_space_w, 'min_h': minimum_space_h, 'max_w': maximum_space_w, 'max_h': maximum_space_h})
        for _ in range(0, num_rooms):
            create_room(area, field_width, depth_height, **{'min_w': minimum_space_w, 'min_h': minimum_space_h, 'max_w': maximum_space_w, 'max_h': maximum_space_h, 'enemies': encountered})
        with open(f'area_{area_counter}.csv', 'w', newline='') as csvfile:
            for row in area:
                areawriter = csv.writer(csvfile, delimiter=',')
                areawriter.writerow(row)
        area_counter += 1

    area_total = int(world['area_total'])

    while(area_counter < area_total):
        area_counter += 1
        # create fresh area
        area = create_underground_dirt_area(field_width, depth_height, 0)
        # choose how many rooms we want in the dirt
        num_rooms = random.choice([i for i in range(int(world['min_rooms']), int(world['max_rooms']))])
        print({'min_w': minimum_space_w, 'min_h': minimum_space_h, 'max_w': maximum_space_w, 'max_h': maximum_space_h})
        for _ in range(0, num_rooms):
            #choose random enemies to put into room
            num_rooms = random.choice([i for i in range(1, len(encountered))])
            rand_enemy_keys = []
            for _ in range(0, num_rooms):
                rand_enemy_keys.append(random.choice(encountered))
            create_room(area, field_width, depth_height, **{'min_w': minimum_space_w, 'min_h': minimum_space_h, 'max_w': maximum_space_w, 'max_h': maximum_space_h, 'enemies': rand_enemy_keys})
        with open(f'area_{area_counter}.csv', 'w', newline='') as csvfile:
            for row in area:
                areawriter = csv.writer(csvfile, delimiter=',')
                areawriter.writerow(row)



if __name__ == "__main__":
    print('...starting...')
    app()
    print('complete!')
