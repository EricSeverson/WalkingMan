#!/usr/bin/env python
"""Module to help build an RPG with a dynamic map"""

import sys

import pygame



class Player(pygame.sprite.Sprite):
    """Class for the main character""" 
    def __init__(self, images, direction='up'):
        pygame.sprite.Sprite.__init__(self)
        self.hero_origin = [160, 0]
        self.images = images
        self.image = images.subsurface(self.hero_origin, (32, 32))
        self.direction = 'up'
        self.rect = self.image.get_rect(center=pygame.display.get_surface().get_rect().center)
        self.hero_width = 32

    def update(self, key=None):
        self.hero_origin[0] += self.hero_width
        if self.hero_origin[0] == self.images.get_rect().width - 32 or self.hero_origin[0] == 0:
            self.hero_width *= -1
        self.image = self.images.subsurface(self.hero_origin, (32, 32))
        if key == pygame.K_RIGHT:
            self.image = pygame.transform.rotate(self.image, -90)
        elif key == pygame.K_LEFT:
            self.image = pygame.transform.rotate(self.image, 90)
        elif key == pygame.K_DOWN:
            self.image = pygame.transform.rotate(self.image, 180)

class Tile(pygame.sprite.Sprite):
    """Class to keep track of separate map tiles"""
    def __init__(self, image, origin):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft=origin)

    def update(self, key):
        if key == pygame.K_RIGHT:
            self.rect.x -= 3
        elif key == pygame.K_LEFT:
            self.rect.x += 3
        elif key == pygame.K_UP:
            self.rect.y += 3
        elif key == pygame.K_DOWN:
            self.rect.y -= 3
