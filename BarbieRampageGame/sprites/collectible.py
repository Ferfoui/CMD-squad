import pygame
import abc as abstract

from constants import *
import utils

class Collectible(pygame.sprite.Sprite, abstract.ABC):
    def __init__(self, x: int, y: int, image_path: str, assets: utils.Assets, tile_size: int, scale: float = 1, do_default_load_image: bool = True):
        """Crée un objet collectible

        Args:
            x (int): position en abscisse
            y (int): position en ordonnée
            image_path (str): chemin de l'image
            assets (utils.Assets): assets utilisés par le jeu
            tile_size (int): taille d'une tuile
            scale (float, optional): échelle de l'image. 1 par défaut.
            do_default_load_image (bool, optional): charge l'image et le rectangle avec la procédure par défaut, si False, il faut le faire manuellement. True par défaut.
            """
        super().__init__()
        
        self.size_factor = tile_size * SPRITE_SCALING
        self.x = x
        self.y = y
        self.y_velocity = 0
        
        if do_default_load_image:
            self.image = assets.get_scaled_image(image_path, scale * self.size_factor)
        
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
    
    def update(self, world):
        """Met à jour l'objet collectible

        Args:
            world (world.World): monde dans lequel se trouve l'objet
        """
        self.scroll(world.scroll.screen_scroll)

    def draw(self, screen: pygame.Surface):
        """Affiche l'objet sur l'écran

        Args:
            screen (pygame.Surface): surface sur laquelle dessiner l'objet
        """
        screen.blit(self.image, self.rect)
    
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
    def on_collect_action(self, player) -> any:
        """Action à effectuer lors de la collecte de l'objet
        """
        pass

class ItemBox(Collectible):
    def __init__(self, x: int, y: int, assets: utils.Assets, tile_size: int, scale: float = 1):
        """Crée une box d'item

        Args:
            x (int): position en abscisse
            y (int): position en ordonnée
            assets (utils.Assets): assets utilisés par le jeu
            tile_size (int): taille d'une tuile
            scale (float, optional): facteur de redimensionnement. 1 par défaut.
        """
        image_path = f"{COLLECTIBLES_TEXTURES_LOCATION}chest/"
        super().__init__(x, y, image_path, assets, tile_size, scale, False)

        # TODO: finir animation genre changer "joueur" etc et finir les on_collect_action
        # Valeur du temps pour l'animation de la box
        self.update_time = pygame.time.get_ticks()

        self.ANIMATION_TYPES = ['Close', 'Open']

        scale = 1.5 * self.size_factor
        # Dictionnaire dans lequel il y a les frames des différentes animations
        self.animation_dict = assets.load_animation(self.ANIMATION_TYPES, image_path, scale)
        # Index de la frame actuelle de l'animation
        self.frame_index = 0

        # Met la box en position fermée
        self.action = self.ANIMATION_TYPES[0]
        # Met l'image correspondant à son action
        self.image = self.animation_dict[self.action][self.frame_index]
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update_animation(self):
        """Met à jour l'animation de la box"""
        
        ANIMATION_COOLDOWN = 50
        # Met à jour l'image en fonction de la frame actuelle
        self.image = self.animation_dict[self.action][self.frame_index]

        # Vérifie si assez de temps est passé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

	    # Si l'animation est terminée, remise de la première image
        if self.frame_index >= len(self.animation_dict[self.action]):
            self.frame_index = 0
    
    def update(self, world):
        """Met à jour la box

        Args:
            world (world.World): monde dans lequel se trouve la box
        """
        super().update(world)
        self.update_animation()

    def on_collect_action(self, player):
        if pygame.sprite.collide_rect(player.rect, self.rect):
            self.action = self.ANIMATION_TYPES[1]

