#!/usr/bin/env python

"""
Program and Art made by Eric Severson

Program was made to test some of my ideas on movement within a game.

The map is grid based, whereas the movement is not.
"""

import sys

import pygame

import RPGDynamic


def setup():
    """
    Creates the map using a pixel map, where specific colors map to specific tiles.

    returns hero sprite, the map, and sprite group of water tiles
    """

    tiles = pygame.image.load('Images/MapTiles.png')
    tile_size = (32, 32)
    # Distinct Tiles used to build map
    water_tile = tiles.subsurface((0, 0), tile_size)
    grass_tile = tiles.subsurface((32, 0), tile_size)
    red_flower_tile = tiles.subsurface((64, 0), tile_size)
    yellow_flower_tile = tiles.subsurface((96, 0), tile_size)
    bridge_tile = tiles.subsurface((0, 32), tile_size)
    dirt_tile = tiles.subsurface((128, 0), tile_size)

    pix_map = pygame.image.load('Images/Maps/GrassyLakes.png')
    game_map = pygame.Surface((32*pix_map.get_width(), 32*pix_map.get_height()))
    hero = RPGDynamic.Player(pygame.image.load('Images/Hero.png'), tile_size)
    all_tiles = pygame.sprite.Group()
    water_group = pygame.sprite.Group()

    # Populate the map with tiles. Water tiles are sprites.
    for i in range(pix_map.get_height()):
        for j in range(pix_map.get_width()):
            curr_color = pix_map.get_at((j, i))
            # Water tile
            if curr_color.r == 0 and curr_color.g == 0 and curr_color.b == 255:
                water_sprite = RPGDynamic.Tile(water_tile, (j*32, i*32))
                game_map.blit(water_sprite.image, water_sprite.rect)
                water_group.add(water_sprite)
                all_tiles.add(water_sprite)
            # Grass tile
            elif curr_color.r == 0 and curr_color.g == 255 and curr_color.b == 0:
                game_map.blit(grass_tile, (j*32, i*32))
            # Red flower tile
            elif curr_color.r == 255 and curr_color.g == 0 and curr_color.b == 0:
                game_map.blit(red_flower_tile, (j*32, i*32))
            # Yellow flower tile
            elif curr_color.r == 255 and curr_color.g == 255 and curr_color.b == 0:
                game_map.blit(yellow_flower_tile, (j*32, i*32))
            # Dirt tile
            elif curr_color.r == 78 and curr_color.g == 42 and curr_color.b == 20:
                game_map.blit(dirt_tile, (j*32, i*32))
            # Bridge tile
            elif curr_color.r == 162 and curr_color.g == 98 and curr_color.b == 60:
                game_map.blit(bridge_tile, (j*32, i*32))
    return hero, game_map, water_group

def game_loop(hero, game_map, water_group):
    # Start at the origin
    map_x, map_y = 0, 0
    map_left = True
    map_right = False
    map_top = True
    map_bot = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                hero.update(event.key)
                next_x, next_y = map_x, map_y
                curr_direction = None
                if event.key == pygame.K_RIGHT:
                    next_x = map_x - 3
                    curr_direction = 'right'
                elif event.key == pygame.K_LEFT:
                    next_x = map_x + 3
                    curr_direction = 'left'
                elif event.key == pygame.K_UP:
                    next_y = map_y + 3
                    curr_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    next_y = map_y - 3
                    curr_direction = 'down'
                # Keep track of attemted movement to test for collision 
                x_movement = next_x - map_x
                y_movement = next_y - map_y
                collided = False
                for tile in water_group.sprites():
                    # Test attempted y_movement with current water_tile
                    if curr_direction == 'up' or curr_direction == 'down':
                        if tile.rect.colliderect(pygame.Rect((hero.rect.x, hero.rect.y - y_movement), (hero.rect.width, hero.rect.height))):
                            collided = True
                            break
                    # Test attempted x_movement with current water_tile
                    elif curr_direction == 'left' or curr_direction == 'right':
                        if tile.rect.colliderect(pygame.Rect((hero.rect.x - x_movement, hero.rect.y), (hero.rect.width, hero.rect.height))):
                            collided = True
                            break
                # if no collision, try to move the screen
                else:
                    # move the screen only on the axi that the hero is centered on
                    if hero.rect.centery == screen.get_rect().centery: 
                        map_y = next_y
                    if hero.rect.centerx == screen.get_rect().centerx:    
                        map_x = next_x
                    # if map is at an edge the stop moving the screen
                    if map_x < -1*game_map.get_width() + screen.get_width():
                        map_x = -1*game_map.get_width() + screen.get_width()
                        map_right = True
                    elif map_x > 0:
                        map_x = 0
                        map_left = True
                    elif map_y < -1*game_map.get_height() + screen.get_height():
                        map_y = -1*game_map.get_height() + screen.get_height()
                        map_bot = True
                    elif map_y > 0:
                        map_y = 0
                        map_top = True
                    # if hero isnt at an edge
                    else: 
                        # if hero is centered on an axis, then update the water tiles
                        if hero.rect.centery == screen.get_rect().centery:
                            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                                water_group.update(event.key)
                        if hero.rect.centerx == screen.get_rect().centerx:
                            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                water_group.update(event.key)
                    # if map is at an edge, move him, 
                    # then check to see if hero becomes centered with the screen
                    if map_right:
                        hero.rect.x -= x_movement
                        if hero.rect.centerx < screen.get_rect().centerx:
                            hero.rect.centerx = screen.get_rect().centerx
                            map_right = False
                    if map_left:
                        hero.rect.x -= x_movement
                        if hero.rect.centerx > screen.get_rect().centerx:
                            hero.rect.centerx = screen.get_rect().centerx
                            map_left = False
                    if map_top:
                        hero.rect.y -= y_movement
                        if hero.rect.centery > screen.get_rect().centery:
                            hero.rect.centery = screen.get_rect().centery
                            map_top = False
                    if map_bot:
                        hero.rect.y -= y_movement
                        if hero.rect.centery < screen.get_rect().centery:
                            hero.rect.centery = screen.get_rect().centery
                            map_bot = False
                    # if hero reaches the end of the screen, then keep him at the edge
                    if hero.rect.x < 0:
                        hero.rect.x = 0
                    elif hero.rect.right > screen.get_rect().width:
                        hero.rect.right = screen.get_rect().width
                    elif hero.rect.y < 0:
                        hero.rect.y = 0
                    elif hero.rect.bottom > screen.get_rect().height:
                        hero.rect.bottom = screen.get_rect().height

        screen.fill((0, 0, 0))
        screen.blit(game_map, (map_x, map_y))
        screen.blit(hero.image, hero.rect)
        pygame.display.flip()

# main program
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.key.set_repeat(10, 10)
    hero, game_map, water_group = setup()
    game_loop(hero, game_map, water_group)
