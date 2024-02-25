import pygame

from constants import *
import utils

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, tile_size: int, scale: float, assets: utils.Assets, texture_location: str):
        """Crée un ennemi

        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            tile_size (int): taille des tuiles
            scale (float): facteur de redimensionnement
            assets (utils.Assets): classe qui contient les assets du jeu
            texture_location (str): position de la texture
        """
        super().__init__()
        
        self.size_factor = tile_size * SPRITE_SCALING

        # Varibles de l'etat de l'ennemi
        self.is_alive = True
        self.health = 100
        self.direction = 1
        
        self.flip = False
        
        # Variables pour le déplacement
        self.vel_y = 0
        self.in_air = False

        self.image = assets.load_scaled_image(texture_location, scale * self.size_factor)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Variable pour la hitbox
        self.hitbox = self.set_hitbox()
        self.mask = pygame.mask.from_surface(self.image)
    
    def set_hitbox(self) -> pygame.Rect:
        """Définit la hitbox de l'ennemi

        Args:
            x (int): position de la hitbox sur l'axe des abscisses
            y (int): position de la hitbox sur l'axe des ordonnées
            width (int): largeur de la hitbox
            height (int): hauteur de la hitbox
        
        Returns:
            pygame.Rect: la hitbox de l'ennemi
        """
        hitbox = self.rect.copy()
        return hitbox
        
    def check_collides_with_world(self, dx: int, dy: int, world) -> tuple[int, int]:
        """Vérifie les collisions de l'ennemi avec les obstacles du monde

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
            world (World): monde dans lequel le joueur se déplace
        
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
                # Vérifie si l'ennemi est en dessous d'une platforme
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.rect.top
                # Vérifie si l'ennemi touche le sol
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    self.jump = False
                    dy = tile.rect.top - self.rect.bottom
        
        return dx, dy
    
    def check_collides(self, dx: int, dy: int, world) -> tuple[int, int]:
        """Vérifie les collisions de l'ennemi

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
            world (World): monde dans lequel le joueur se déplace
        
        Returns:
            tuple[int, int]: les distances de déplacement ajustées en fonction des collisions
        """
        dx, dy = self.check_collides_with_world(dx, dy, world)
        return dx, dy
    
    def move(self, world):
        """Méthode qui permet de déplacer l'ennemi

        Args:
            world (World): monde dans lequel l'ennemi se déplace
        """
        dx = 0
        dy = 0
        if self.is_alive:
            
            # Application de la gravité
            self.vel_y += GRAVITY * self.size_factor
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y
            
            # Vérifie les collisions
            dx, dy = self.check_collides(dx, dy, world)
        
        self.move_enemy_position(dx, dy, world)
    
    def move_enemy_position(self, dx: int, dy: int, world):
        """Méthode qui permet de déplacer la position de l'ennemi

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
        """
        self.rect.x += dx + world.scroll.screen_scroll
        self.rect.y += dy
    
    def update(self):
        """Méthode qui permet de mettre à jour l'ennemi"""
        self.hitbox.bottom = self.rect.bottom
        self.hitbox.centerx = self.rect.centerx
    
    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher l'opps 

        Args:
            screen (Surface): fenêtre sur laquelle l'ennemi doit être affiché
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Dummy(Enemy):
    def __init__(self, x: int, y: int, tile_size: int, scale: float, assets: utils.Assets):
        """Crée un mannenequin d'entraînement

        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            tile_size (int): taille des tuiles
            scale (float): facteur de redimensionnement
            assets (utils.Assets): classe qui contient les assets du jeu
        """
        super().__init__(x, y, tile_size, scale, assets, ENEMIES_TEXTURES_LOCATION + "dummy.png")
    
