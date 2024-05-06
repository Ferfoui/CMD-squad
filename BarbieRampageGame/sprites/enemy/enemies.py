import pygame

from constants import *
from .enemy import Enemy, IntelligentEnemy
import utils

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
        super().__init__(x, y, tile_size, assets, ENEMIES_TEXTURES_LOCATION + "dummy.png", scale = scale)

class IntelligentDummy(IntelligentEnemy):
    def __init__(self, x: int, y: int, tile_size: int, scale: float, assets: utils.Assets, speed: int):
        """Crée un mannequin d'entraînement intelligent
        
        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            tile_size (int): taille des tuiles
            scale (float): facteur de redimensionnement
            assets (utils.Assets): classe qui contient les assets du jeu
            speed (int): vitesse de l'ennemi
        """
        super().__init__(x, y, tile_size, assets, ENEMIES_TEXTURES_LOCATION + "dummy.png", speed = speed, scale = scale)

    def ai(self, world):
        """Méthode qui permet de déplacer l'ennemi vers le joueur

        Args:
            world (World): _description_
        """
        if self.can_see_player(world):
            move_right = world.player.rect.x > (self.rect.right + 3 * self.size_factor)
            move_left = world.player.rect.right < (self.rect.x - 3 * self.size_factor)
            self.move(world, move_right, move_left)
        else:
            self.move_around(world)

class KenEnemy(IntelligentEnemy):
    def __init__(self, x: int, y: int, tile_size: int, scale: float, assets: utils.Assets):
        """Crée un ennemi Ken

        Args:
            x (int): position de Ken sur l'axe des abscisses
            y (int): position de Ken sur l'axe des ordonnées
            tile_size (int): taille des tuiles
            scale (float): facteur de redimensionnement
            assets (utils.Assets): classe qui contient les assets du jeu
        """
        ANIMATION_LIST = ['Idle', 'Attack', 'Dead']
        super().__init__(x, y, tile_size, assets, ENEMIES_TEXTURES_LOCATION + "ken/", speed = 2, scale = scale, animation_list = ANIMATION_LIST)
        
        self.last_attack_time = pygame.time.get_ticks()
        self.ken_could_attack = False
        self.ken_is_attacking = False
        
        self.animation_cooldown = 50
        
        self.ATTACK_COOLDOWN = 1500
        self.damage_time = 1000
    
    def ai(self, world):
        """Méthode qui permet de déplacer Ken vers le joueur
        
        Args:
            world (World): monde dans lequel Ken se déplace
        """
        if self.can_see_player(world):
            move_right = world.player.rect.x > (self.rect.right + 2 * self.size_factor)
            move_left = world.player.rect.right < (self.rect.x - 2 * self.size_factor)
            self.move(world, move_right, move_left)
            
            if self.player_in_attack_range(world):
                self.attack(world)
            elif not self.ken_is_attacking:
                self.update_action('Idle')
        else:
            self.move_around(world)
    
    def player_in_attack_range(self, world) -> bool:
        """Méthode qui permet de vérifier si le joueur est dans la zone d'attaque de Ken
        
        Args:
            world (World): monde dans lequel Ken se déplace
        
        Returns:
            bool: si le joueur est dans la zone d'attaque de Ken
        """
        attack_rect = self.attack_rect()

        return attack_rect.colliderect(world.player.rect)
        
    def attack(self, world):
        """Méthode qui permet à Ken d'attaquer le joueur
        
        Args:
            world (World): monde dans lequel Ken se déplace
        """
        
        self.ATTACK_COOLDOWN = 1200
        
        ken_could_attack = (pygame.time.get_ticks() - self.last_attack_time) > self.ATTACK_COOLDOWN

        if ken_could_attack and self.is_alive:
            
            if self.player_in_attack_range(world):
                self.world = world
                self.start_attack()
    
    def start_attack(self):
        """Méthode qui permet de définir le début de l'attaque de Ken
        """
        self.update_action('Attack')
        self.ken_is_attacking = True
        self.last_attack_time = pygame.time.get_ticks()

    def attack_rect(self):
        """Méthode qui permet de définir la zone d'attaque de Ken
        """
        width = int(self.rect.width * 1.2)
        height = int(self.rect.height * 0.3)
        
        if not self.flip:
            x = self.rect.right - self.rect.width * 0.2
        else:
            x = self.rect.left - width + self.rect.width * 0.2
        
        y = self.rect.y + self.rect.height * 0.4
        
        attack_rect = pygame.Rect(x, y, width, height)
        
        return attack_rect
    
    def check_if_alive(self) -> bool:
        """Vérifie si Ken est vivant"""
        if self.health <= 0 or self.rect.y > self.death_level:
            self.health = 0
            self.speed = 0
            self.is_alive = False
            self.update_action('Dead')
        
        return self.is_alive

    def update(self):
        """Met à jour Ken
        """
        super().update()
        
        if self.ken_is_attacking:
            if (pygame.time.get_ticks() - self.last_attack_time) > self.damage_time:
                
                if self.player_in_attack_range(self.world):
                    self.world.player.health -= 15
                
                self.ken_is_attacking = False
    
    def draw(self, screen: pygame.Surface):
        """Affiche Ken à l'écran

        Args:
            screen (pygame.Surface): écran sur lequel Ken est affiché
        """
        super().draw(screen)