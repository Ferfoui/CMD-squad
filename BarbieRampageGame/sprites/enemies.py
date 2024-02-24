import pygame

from constants import *
import utils

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: float, assets: utils.Assets, texture_location: str):
        """Crée un ennemi

        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            scale (float): facteur de redimensionnement
            assets (utils.Assets): classe qui contient les assets du jeu
            texture_location (str): position de la texture
        """
        super().__init__()

        self.is_alive = True
        self.health = 100
        self.direction = 1

        self.image = assets.load_scaled_image(texture_location, scale)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher l'opps 

        Args:
            screen (Surface): fenêtre sur laquelle l'ennemi doit être affiché
        """
        screen.blit(self.image, self.rect)

class Dummy(Enemy):
    def __init__(self, x: int, y: int, scale: float, assets: utils.Assets):
        """Crée un mannenequin d'entrainement

        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            scale (float): facteur de redimensionnement
            assets (utils.Assets): classe qui contient les assets du jeu
        """
        super().__init__(x, y, scale, assets, ENEMIES_TEXTURES_LOCATION + "dummy.png")
