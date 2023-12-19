import pygame
from Constants import *


# Création de la classe du Joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.rect = pygame.Rect(x, y, 64, 128)
        self.flip = False
        self.move_left = False
        self.move_right = False

    def move(self):
        return

    def update(self):
        return

    def draw(self, screen):
        #screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)