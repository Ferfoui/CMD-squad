import pygame
import os
from Constants import *


# Création de la classe du Joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, scale):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.flip = False
        self.move_left = False
        self.move_right = False
        
        self.animation_dict = {}
        self.frame_index = 0
        
        # charge toutes les images du joueur
        # animation_types = ['Idle', 'Run', 'Jump', 'Death']
        animation_types = ['Idle']
        for animation in animation_types:

            self.animation_dict[animation] = []

			# compte le nombre d'image qu'il y a dans le dossier
            number_of_frames = len(os.listdir(f"{PLAYER_TEXTURES_LOCATION}default/{animation}"))
            for i in range(number_of_frames):
                img = pygame.image.load(f"{PLAYER_TEXTURES_LOCATION}default/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.animation_dict[animation].append(img)

        self.action = animation_types[0]
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        return

    def update(self):
        return

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)