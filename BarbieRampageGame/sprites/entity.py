import pygame
import abc as abstract

from constants import *
import utils

class Entity(pygame.sprite.Sprite, abstract.ABC):
    def __init__(self, x: int, y: int, max_health: int, tile_size: int, assets: utils.Assets, speed: int = 1, scale: float = 1):
        """Classe abstraite qui définit les entités du jeu

        Args:
            x (int): position en abscisses où l'entité doit être créée
            y (int): position en ordonnées où l'entité doit être créée
            max_health (int): vie maximale de l'entité
            tile_size (int): taille d'une tuile
            assets (utils.Assets): classe contenant les assets
            speed (int, optional): vitesse de l'entité. 1 par défaut.
        """
        super().__init__()
        
        self.size_factor = tile_size * SPRITE_SCALING
        
        self.health = max_health
        
        # Variables pour l'état de l'entité
        self.is_alive = True
        self.health = 100
        self.direction = 1
        
        self.flip = False
        
        # Variables pour le déplacement
        self.speed = speed * self.size_factor
        self.vel_y = 0
        self.in_air = False
        self.jump = False

        self.rect = self.define_entity_rect(x, y, assets, scale)
        
        self.hitbox = self.define_entity_hitbox(self.rect)

    @abstract.abstractmethod
    def define_entity_rect(self, x: int, y: int, assets: utils.asset, scale) -> pygame.Rect:
        """Méthode qui crée le rectangle de l'entité
        
        Args:
            x (int): position en x
            y (int): position en y
            assets (utils.asset): classe contenant les assets
            scale (float, optional): facteur de redimensionnement
        
        Returns:
            pygame.Rect: rectangle de l'entité
        """
        return pygame.Rect(x, y, self.size_factor * scale, self.size_factor * scale)
    
    def define_entity_hitbox(self, entity_rect: pygame.Rect) -> pygame.Rect:
        """Méthode qui crée une hitbox approximative de l'entité
        
        Args:
            entity_rect (pygame.Rect): rectangle de l'entité
        
        Returns:
            pygame.Rect: hitbox de l'entité
        """
        return entity_rect.copy()

    def apply_gravity(self, y_velocity: float, gravity_factor: float = 1) -> float:
        """Méthode qui applique la gravité à l'entité
        
        Args:
            y_velocity (float): vitesse de déplacement sur l'axe vertical
            gravity_factor (int, optional): facteur de gravité. 1 par défaut.
        """
        y_velocity += GRAVITY * gravity_factor * self.size_factor
        
        return y_velocity
    
    def check_collides_with_world(self, dx: int, dy: int, world) -> tuple[int, int]:
        """Vérifie les collisions de l'entité avec les obstacles du monde

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
            world (World): monde dans lequel l'entité se déplace
        
        Returns:
            tuple[int, int]: les distances de déplacement ajustées en fonction des collisions
        """
        for tile in world.obstacle_list:
            next_x_position = self.hitbox.x + dx
            next_y_position = self.hitbox.y + dy + 1
            
            # Vérifie les collisions sur l'axe horizontal
            if tile.rect.colliderect(next_x_position, self.hitbox.y, self.hitbox.width, self.hitbox.height):
                dx = 0
            # Vérifie les collisions sur l'axe vertical
            if tile.rect.colliderect(self.hitbox.x, next_y_position, self.hitbox.width, self.hitbox.height):
                # Vérifie si l'entité est en dessous d'une platforme
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.rect.top
                # Vérifie si l'entité touche le sol
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    self.jump = False
                    dy = tile.rect.top - self.rect.bottom
        
        return dx, dy
    
    def check_collides(self, dx: int, dy: int, world) -> tuple[int, int]:
        """Vérifie les collisions de l'entité

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
            world (World): monde dans lequel l'entité se déplace
        
        Returns:
            tuple[int, int]: les distances de déplacement ajustées en fonction des collisions
        """
        dx, dy = self.check_collides_with_world(dx, dy, world)
        return dx, dy
    
    def move_entity_position(self, dx: int, dy: int, world):
        """Méthode qui permet de déplacer la position de l'entité

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
        """
        self.rect.x += dx + world.scroll.screen_scroll
        self.rect.y += dy
    
    def check_if_alive(self) -> bool:
        """Vérifie si l'entité est vivante"""
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.is_alive = False
        
        return self.is_alive
    
    def update(self, *args, **kwargs):
        """Met à jour l'entité"""
        self.check_if_alive()
        self.update_hitbox()

    def update_hitbox(self):
        """Met à jour la hitbox de l'entité"""
        self.hitbox.bottom = self.rect.bottom
        self.hitbox.centerx = self.rect.centerx

