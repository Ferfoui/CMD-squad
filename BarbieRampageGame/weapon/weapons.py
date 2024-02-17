#Création des différentes armes du jeu

import pygame

from .bullets import Bullet 
from constants import *
import utils

# La classe qui crée les armes
class Weapon():
    #TODO: Rendre l'arme obtensible, faire fonctionner les balles, faire en sorte que les armes fassent des dégâts
    def __init__(self, weapon_name: str, texture_path: str, assets: utils.Assets, weapon_width: int, x: int, y: int):
        """Créé une nouvelle arme

        Args:
            weapon_name (str): nom de l'arme
            texture_path (str): position de la texture
            assets (utils.Assets): classe des assets
            weapon_width (int): largeur de l'arme
            x (int): position sur l'axe horizontal
            y (int): position sur l'axe vertical
        """
        self.is_grab = False
        self.flip = False
        self.weapon_texture = self.init_texture(weapon_name, texture_path, assets, weapon_width)
        self.rect = self.weapon_texture.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen: pygame.Surface):
        """Affiche l'arme sur l'écran

        Args:
            screen (pygame.Surface): écran
        """
        screen.blit(self.weapon_texture,self.rect)    
    
    def init_texture(self, name: str, texture_path: str, assets: utils.Assets, weapon_width: int) -> pygame.Surface:
        """Initialise la texture de l'arme

        Args:
            name (str): nom de l'arme
            texture_path (str): position de la texture
            assets (utils.Assets): classe des assets
            weapon_width (int): largeur de l'arme

        Returns:
            pygame.Surface: image de l'arme
        """
        return assets.get_image(name, texture_path, weapon_width)
    
    def shoot(self, direction: int, bullet_group):
        """Tire une munition

        Args:
            direction (int): direction dans laquelle la balle va, 1 si c'est vers la droite et -1 si c'est vers la gauche
        """
        
        bullet = Bullet(1, self.rect.x, self.rect.y, direction)
        bullet_group.add(bullet)
        

class Arb4rb13(Weapon):
    def __init__(self, assets: utils.Assets, weapon_width: int, x: int, y: int):
        """Crée une nouvelle arme de type AR-BARB13

        Args:
            assets (utils.Assets): classe des assets
            weapon_width (int): largeur de l'arme
            x (int): position de l'axe horizontal
            y (int): position de l'axe vertical
        """
        super().__init__("AR-B4RB13", TEXTURES_ROOT + "weapons/AR_B4RB13.png", assets, weapon_width, x, y)