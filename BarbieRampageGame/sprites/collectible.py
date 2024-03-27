import pygame
import abc as abstract

from constants import *
import utils, world

class Collectible(pygame.sprite.Sprite, abstract.ABC):
    def __init__(self, x: int, y: int, image_path: str, assets: utils.Assets, tile_size: int, scale: float = 1):
        """Crée un objet collectible

        Args:
            x (int): position en abscisse
            y (int): position en ordonnée
            image_path (str): chemin de l'image
            assets (utils.Assets): assets utilisés par le jeu
            tile_size (int): taille d'une tuile
            scale (float, optional): échelle de l'image. 1 par défaut.
        """
        super().__init__()
        
        self.size_factor = tile_size * SPRITE_SCALING
        self.x = x
        self.y = y
        self.y_velocity = 0
        self.image = assets.get_scaled_image(image_path, scale * self.size_factor)
        
        self.rect = self.image.get_rect()
    
    def update(self, world: world.World):
        """Met à jour l'objet collectible

        Args:
            world (world.World): monde dans lequel se trouve l'objet
        """
        self.scroll(world.scroll.screen_scroll)
    
    def scroll(self, scroll_value: int):
        """Déplace l'objet en fonction du scroll du monde
        """
        self.x += scroll_value
    
    def apply_gravity(self):
        """Applique la gravité à l'objet

        Args:
            gravity (float): gravité appliquée
        """
        self.y_velocity += GRAVITY * self.size_factor
    
    @abstract.abstractmethod
    def on_collect_action(self) -> any:
        """Action à effectuer lors de la collecte de l'objet
        """
        pass

class ItemBox(Collectible):
    def __init__(self, x, y, image_path: str, assets: utils.Assets, tile_size: int, scale: float = 1):
        super().__init__(x, y, image_path, assets.Assets, tile_size, scale)
