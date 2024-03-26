import pygame
import utils, world

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image_path: str, assets: utils.Assets, scale: float = 1):
        """Crée un objet collectible

        Args:
            x (int): position en abscisse
            y (int): position en ordonnée
            image_path (str): chemin de l'image
            assets (utils.Assets): assets utilisés par le jeu
            scale (float, optional): échelle de l'image. 1 par défaut.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.image = assets.get_scaled_image(image_path, scale)
    
    def update(self, world: world.World):
        """Met à jour l'objet collectible

        Args:
            world (world.World): monde dans lequel se trouve l'objet
        """
        self.scoll(world.scroll.screen_scroll)
    
    def scroll(self, scroll_value: int):
        """Déplace l'objet en fonction du scroll du monde
        """
        self.y += scroll_value
    

class ItemBox(Collectible):
    def __init__(self, x, y, image_path: str, assets: utils.Assets, scale: float = 1):
        super().__init__(x, y, image_path, assets.Assets, scale)
