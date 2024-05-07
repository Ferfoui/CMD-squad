import pygame

from enemy import IntelligentEnemy
import utils
from constants import*

class Boss(IntelligentEnemy):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets, texture_location: str, max_health: int = 200, speed: int = 1, scale: float = 1):
        super().__init__(x , y, tile_size, assets, texture_location, max_health, speed, scale)


class SuperDuperHyperMegaKenMonster(Boss):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets, scale: float = 1):
        ANIMATION_LIST = ['Idle', 'Attack1', 'Attack2', 'Dead']
        super().__init__(x, y, tile_size, assets, ENEMIES_TEXTURES_LOCATION + "boss/", 1000, 3, scale, ANIMATION_LIST)
        self.last_attack_time = pygame.time.get_ticks()
        self.ken_monster_could_attack = False
        self.ken_monster_is_attacking = False
        
        self.animation_cooldown = 50
        
        self.ATTACK_COOLDOWN = 1500
        self.damage_time = 1200
        self.attack_damage = 25
        self.special_attack_damage = 50

    def normal_attack(self, world):
        """ Méthode qui permet au boss de faire une attaque normale
        Args:
             world (World): monde dans lequel le boss se déplace
        """
        self.ATTACK_COOLDOWN = 1200
        
        self.ken_monster_could_attack = (pygame.time.get_ticks() - self.last_attack_time) > self.ATTACK_COOLDOWN

        if self.ken_monster_could_attack and self.is_alive:
            
            if self.player_in_attack_range(world):
                self.world = world
                self.start_attack()
                self.normal_attack_rect()
                
        

    def special_attack(self):
        pass

    def ai(self, world):
        """Méthode qui permet de déplacer l'ennemi vers le joueur

        Args:
            world (World): monde dans lequel Ken se déplace
        """
        if self.can_see_player(world):
            move_right = world.player.rect.x > (self.rect.right + 2 * self.size_factor)
            move_left = world.player.rect.right < (self.rect.x - 2 * self.size_factor)
            self.move(world, move_right, move_left)
            
            if self.player_in_attack_range(world):
                self.attack(world)
            elif not self.ken_monster_is_attacking:
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
    
    def start_attack(self):
        """Méthode qui permet de définir le début de l'attaque du boss
        """
        self.update_action('Attack')
        self.ken_monster_is_attacking = True
        self.last_attack_time = pygame.time.get_ticks()

    def normal_attack_rect(self):
        """Méthode qui permet de définir la zone d'attaque du boss
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
    
    def update(self):
        """Met à jour le boss
        """
        super().update()
        
        if self.ken_monster_is_attacking:
            if (pygame.time.get_ticks() - self.last_attack_time) > self.damage_time:
                
                if self.player_in_attack_range(self.world):
                    self.world.player.health -= self.attack_damage 
                
                self.ken_monster_is_attacking = False
    