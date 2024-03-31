#Création des différentes armes du jeu

import pygame
import abc as abstract

from .bullets import Bullet 
from constants import *
import utils

# La classe qui crée les armes
class Weapon(abstract.ABC):
    #TODO: Rendre l'arme obtensible, faire fonctionner les balles, faire en sorte que les armes fassent des dégâts
    def __init__(self, weapon_name: str, texture_path: str, assets: utils.Assets, tile_size: int, scale: float, x: int = 0, y: int = 0):
        """Créé une nouvelle arme

        Args:
            weapon_name (str): nom de l'arme
            texture_path (str): position de la texture
            assets (utils.Assets): classe des assets
            tile_size (int): taille des tuiles
            scale (float): facteur de redimensionnement
            x (int): position sur l'axe horizontal
            y (int): position sur l'axe vertical
        """
        self.size_factor = tile_size * SPRITE_SCALING
        
        self.bullets_consuming = 1
        
        self.is_grab = False
        self.flip = False
        self.weapon_texture = self.init_texture(weapon_name, texture_path, assets, scale)
        self.rect = self.weapon_texture.get_rect()
        #self.rect.center = (x, y)
        
        self.shoot_position_right, self.shoot_position_left = self.get_shoot_coordinates()
    
    @abstract.abstractmethod
    def get_shoot_coordinates(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Récupère les coordonnées relatives du canon de l'arme, cette méthode doit être implémentée dans les classes filles de Weapon

        Returns:
            tuple[int, int]: coordonnées du canon de l'arme quand il est tourné vers la droite
            tuple[int, int]: coordonnées du canon de l'arme quand il est tourné vers la gauche
        """
        return (self.rect.x, self.rect.y), (self.rect.right, self.rect.y)
    
    def init_texture(self, name: str, texture_path: str, assets: utils.Assets, scale: float) -> pygame.Surface:
        """Initialise la texture de l'arme

        Args:
            name (str): nom de l'arme
            texture_path (str): position de la texture
            assets (utils.Assets): classe des assets
            scale (float): facteur de redimensionnement de la texture

        Returns:
            pygame.Surface: image de l'arme
        """
        return assets.get_scaled_image(name, texture_path, scale * self.size_factor)

    def draw(self, screen: pygame.Surface):
        """Affiche l'arme sur l'écran

        Args:
            screen (pygame.Surface): écran
        """
        screen.blit(pygame.transform.flip(self.weapon_texture, self.flip, False), self.rect) 
    
    def shoot(self, direction: int, bullet_group: pygame.sprite.Group) -> int:
        """Tire une munition

        Args:
            direction (int): direction dans laquelle la balle va, 1 si c'est vers la droite et -1 si c'est vers la gauche
            bullet_group (pygame.sprite.Group): groupe dans lequel la balle va être ajoutée
        
        Returns:
            int: nombre de munitions consommées
        """
        relative_shoot_position = self.shoot_position_right if direction == 1 else self.shoot_position_left
        
        absolute_shoot_position = (self.rect.x + relative_shoot_position[0], self.rect.y + relative_shoot_position[1])
        
        bullet = Bullet(self.size_factor, 1, absolute_shoot_position[0], absolute_shoot_position[1], direction)
        bullet_group.add(bullet)
        
        return self.bullets_consuming
        

class Arb4rb13(Weapon):
    def __init__(self, assets: utils.Assets, tile_size: int, scale: float, x: int = 0, y: int = 0):
        """Crée une nouvelle arme de type AR-BARB13

        Args:
            assets (utils.Assets): classe des assets
            tile_size (int): taille des tuiles
            scale (float): facteur de redimensionnement
            x (int): position de l'axe horizontal
            y (int): position de l'axe vertical
        """
        super().__init__("AR-B4RB13", WEAPONS_TEXTURES_LOCATION + "AR_B4RB13.png", assets, tile_size, scale, x, y)
    
    def get_shoot_coordinates(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Récupère les coordonnées relatives du canon de l'arme

        Returns:
            tuple[int, int]: coordonnées du canon de l'arme quand il est tourné vers la droite
            tuple[int, int]: coordonnées du canon de l'arme quand il est tourné vers la gauche
        """
        position_factor = 0.343
        
        right_shoot = self.rect.width, int(self.rect.height * position_factor)
        left_shoot = 0, int(self.rect.height * position_factor)
        
        return right_shoot, left_shoot
