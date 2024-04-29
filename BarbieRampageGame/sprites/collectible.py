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
    def on_collect_action(self, player) -> any:
        """Action à effectuer lors de la collecte de l'objet
        """
        pass

class ItemBox(Collectible):
    def __init__(self, x, y, image_path: str, assets: utils.Assets, tile_size: int, scale: float = 1):
        super().__init__(x, y, image_path, assets.Assets, tile_size, scale)

        # TODO: finir animation genre changer "joueur" etc et finir les on_collect_action
        # Valeur du temps pour l'animation de la box
        self.update_time = pygame.time.get_ticks()

        self.ANIMATION_TYPES = ['Open']

        scale = 1.5 * self.size_factor
        # Dictionnaire dans lequel il y a les frames des différentes animations
        self.animation_dict = assets.load_animation(self.ANIMATION_TYPES, f"{COLLECTIBLES_TEXTURES_LOCATION}chest", scale)
        # Index de la frame actuelle de l'animation
        self.frame_index = 0

        # Met la box en position Open
        self.action = self.ANIMATION_TYPES[0]
        # Met l'image correspondant à son action
        self.image = self.animation_dict[self.action][self.frame_index]

    def update_animation(self):
        """Met à jour l'animation du joueur"""
        
        if self.is_running == True:
            self.update_action(self.ANIMATION_TYPES[1]) # "Run"
        else:
            self.update_action(self.ANIMATION_TYPES[0]) # "Idle"
            
        ANIMATION_COOLDOWN = 50
        # Met à jour l'image en fonction de la frame actuelle
        self.image = self.animation_dict[self.action][self.frame_index]

        # Vérifie si assez de temps est passé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

	    # Si l'animation est terminée, remise de la première image
        if self.frame_index >= len(self.animation_dict[self.action]):
            #if self.action == self.ANIMATION_TYPES[3]:
            #    self.frame_index = len(self.animation_dict[self.action]) - 1
            #else:
                self.frame_index = 0


    def on_collect_action(self, player):
        if pygame.sprite.collide_rect(player.rect):
            self








