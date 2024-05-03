import pygame
import abc as abstract

from constants import *
import utils
import random
import weapon


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
        self.y_velocity = 0
        
        self.collected = False
        
        if do_default_load_image:
            self.image = assets.get_scaled_image(image_path, scale * self.size_factor)
        
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
    
    def update(self, world):
        """Met à jour l'objet collectible

        Args:
            world (world.World): monde dans lequel se trouve l'objet
        """
        self.scroll(world.scroll.screen_scroll)
        self.interact_with_world(world)
    
    def interact_with_world(self, world):
        """Fait interagir l'objet avec le monde

        Args:
            world (world.World): monde dans lequel se trouve l'objet
        """
        self.apply_gravity()
        
        for tile in world.obstacle_list:
            if pygame.sprite.collide_rect(self, tile):
                if self.y_velocity > 0:
                    self.y = tile.rect.top - self.rect.height
                    self.y_velocity = 0
                elif self.y_velocity < 0:
                    self.y = tile.rect.bottom
                    self.y_velocity = 0
        
        self.rect.y += self.y_velocity

    def draw(self, screen: pygame.Surface):
        """Affiche l'objet sur l'écran

        Args:
            screen (pygame.Surface): surface sur laquelle dessiner l'objet
        """
        screen.blit(self.image, self.rect)
    
    def scroll(self, scroll_value: int):
        """Déplace l'objet en fonction du scroll du monde
        """
        self.rect.x += scroll_value
    
    def apply_gravity(self):
        """Applique la gravité à l'objet

        Args:
            gravity (float): gravité appliquée
        """
        self.y_velocity += GRAVITY * self.size_factor
    
    @abstract.abstractmethod
    def on_collect_action(self, player) -> any:
        """Action à effectuer lors de la collecte de l'objet
        
        Args:
            player (Player): joueur qui collecte l'objet
        """
        pass

class ItemBox(Collectible):
    def __init__(self, x: int, y: int, assets: utils.Assets, tile_size: int, item_type: str, scale: float = 1, animation_cooldown: int = 200):
        """Crée une box d'item

        Args:
            x (int): position en abscisse
            y (int): position en ordonnée
            assets (utils.Assets): assets utilisés par le jeu
            tile_size (int): taille d'une tuile
            item_type (str): type de ce qui est contenu dans la box
            scale (float, optional): facteur de redimensionnement. 1 par défaut.
        """
        image_path = f"{COLLECTIBLES_TEXTURES_LOCATION}box/{item_type}/"
        super().__init__(x, y, image_path, assets, tile_size, scale, False)

        # Valeur du temps pour l'animation de la box
        self.update_time = pygame.time.get_ticks()

        self.ANIMATION_TYPES = ['Close', 'Open']
        self.animation_cooldown = animation_cooldown
        
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
        self.rect.x = x
        self.rect.y = y

    def update_animation(self):
        """Met à jour l'animation de la box"""

        # Met à jour l'image en fonction de la frame actuelle
        self.image = self.animation_dict[self.action][self.frame_index]

        # Vérifie si assez de temps est passé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            # Si l'animation est terminée, remise de la première image
            if self.frame_index >= len(self.animation_dict[self.action]):
                if self.action == self.ANIMATION_TYPES[1]:
                    self.frame_index = len(self.animation_dict[self.action]) - 1
                    
                else:
                    self.frame_index = 0
    
    def update(self, world):
        """Met à jour la box

        Args:
            world (world.World): monde dans lequel se trouve la box
        """
        super().update(world)
        self.update_animation()

    def on_collect_action(self, player):
        """Méthode qui permet au joueur d'interagir avec la box

        Args:
            player (Player): Joueur qui interagit avec la box
        """
        if (not self.collected) and pygame.sprite.collide_rect(player, self):
            self.action = self.ANIMATION_TYPES[1]
            self.frame_index = 0
            self.add_item_to_player(player)
            self.collected = True
    
    @abstract.abstractmethod
    def add_item_to_player(self, player):
        """Ajoute un item au joueur

        Args:
            player (Player): joueur auquel ajouter l'item
        """

class AmmoBox(ItemBox):
    def __init__(self, x: int, y: int, assets: utils.Assets, tile_size: int, scale: float = 1):
        """Crée une box de balles

        Args:
            x (int): position en abscisse
            y (int): position en ordonnée
            assets (utils.Assets): assets utilisés par le jeu
            tile_size (int): taille d'une tuile
            scale (float, optional): facteur de redimensionnement. 1 par défaut.
        """
        super().__init__(x, y, assets, tile_size, "Bullet", scale)
    
    def add_item_to_player(self, player):
        """Ajoute des balles au joueur

        Args:
            player (Player): joueur auquel ajouter les balles
        """
        player.add_bullets(10)

class HealthBox(ItemBox):
    def __init__(self, x: int, y: int, assets: utils.Assets, tile_size: int, scale: float = 1):
        """Crée une box de vie

        Args:
            x (int): position en abscisse
            y (int): position en ordonnée
            assets (utils.Assets): assets utilisés par le jeu
            tile_size (int): taille d'une tuile
            scale (float, optional): facteur de redimensionnement. 1 par défaut.
        """
        super().__init__(x, y, assets, tile_size, "Health", scale)
    
    def add_item_to_player(self, player):
        """Ajoute de la vie au joueur

        Args:
            player (Player): joueur auquel ajouter la vie
        """
        player.add_health(25)

class WeaponCrate(ItemBox):
    def __init__(self, x: int, y: int, assets: utils.Assets, tile_size: int, scale: float = 1):
        """Crée une caisse d'armes

        Args:
            x (int): position en abscisse
            y (int): position en ordonnée
            assets (utils.Assets): assets utilisés par le jeu
            tile_size (int): taille d'une tuile
            scale (float, optional): facteur de redimensionnement. 1 par défaut.
        """
        super().__init__(x, y, assets, tile_size, "Weapon", scale, animation_cooldown=100)
        self.assets = assets
        self.tile_size = tile_size
    
    def add_item_to_player(self, player):
        """Donne une arme au joueur

        Args:
            player (Player): joueur à qui donner une arme
        """
        self.weapons = [weapon.Arb4rb13, weapon.GunP450]
        random_weapon = random.choice(self.weapons)
        player.set_weapon(random_weapon(self.assets, self.tile_size, 1))
    