import pygame, os

from constants import *

# Classe pour les balles
class Bullet(pygame.sprite.Sprite):
    def __init__(self, size_factor: float, scale: float, x: int, y: int, direction: int, speed: int = 10, range: int = 400, damage: int = 20, bullet_type: str = "PinkBullet"):
        """Crée une nouvelle balle

        Args:
            size_factor (float): facteur de redimensionnement de la balle
            scale (float): nombre par lequel la taille de la texture va être multiplié
            x (int): position sur l'axe horizontal
            y (int): postion sur l'axe vertical
            direction (int): direction dans laquelle la balle va, 1 si c'est vers la droite et -1 si c'est vers la gauche
            speed (int, optional): vitesse de la balle. 10 par défaut.
            range (int, optional): distance maximale que la balle peut parcourir. 400 par défaut.
            damage (int, optional): dégâts infligés par la balle. 20 par défaut.
        """
        super().__init__()
        
        self.size_factor = size_factor
        
        self.direction = direction
        self.flip = direction < 0
        
        self.speed = speed * self.size_factor
        self.range = abs(range) * self.size_factor
        self.damage = damage
        
        self.ANIMATION_TYPES = ["bullet_start", "bullet_end"]
        
        self.animation = self.load_animation(self.ANIMATION_TYPES, f"{TEXTURES_ROOT}bullets/{bullet_type}", scale)
        self.frame_index = 0
        
        # Valeur du temps pour l'animation de la balle
        self.update_time = pygame.time.get_ticks()
        
        self.is_stopping = False
        self.continue_move = True
        
        self.relative_initial_x = x
    
        # Met la balle en position start
        self.action = self.ANIMATION_TYPES[self.frame_index]
        # Met l'image correspondant à son action
        self.image = self.animation[self.action][self.frame_index]
        # Crée le rectangle de la balle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Crée la hitbox de la balle
        self.mask = pygame.mask.from_surface(self.image)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        
    def load_animation(self, animation_types: list[str], texture_location: str, scale: float) -> dict[str, list[pygame.Surface]]:
        """Charge l'animation de la balle

        Args:
            animation_types (list[str]): noms des animations
            texture_location (str): position des textures
            scale (float): nombre par lequel la taille de la texture va être multiplié

        Returns:
            dict[str, list[pygame.Surface]]: dictionnaire de listes de frames
        """
        animation_dict = {}
        
        for animation in animation_types:
            animation_dict[animation] = []
			# Compte le nombre d'images qu'il y a dans le dossier
            number_of_frames = len(os.listdir(f"{texture_location}/{animation}"))
            for i in range(number_of_frames):
                # Charge l'image dans la mémoire
                img = pygame.image.load(f"{texture_location}/{animation}/{i:02}.png").convert_alpha()
                # Converti l'image pour qu'elle soit de la taille voulue
                img = pygame.transform.scale(img, (int(img.get_width() * scale * self.size_factor), int(img.get_height() * scale * self.size_factor)))
                animation_dict[animation].append(img)
        return animation_dict
    
    def move(self, world):
        """Fais bouger la balle
        
        Args:
            world (World): monde dans lequel la balle se trouve
        """
        dx = 0
        if self.continue_move and (not self.is_stopping):
            dx += self.speed * self.direction + world.scroll.screen_scroll
            dx = self.check_collides(dx, world)
        
        self.rect.x += dx
    
    def check_collides(self, dx: int, world) -> int:
        """Vérifie les collisions entre la balle et le joueur ou un ennemi

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            world (World): monde dans lequel la balle se trouve
        
        Returns:
            int: distance de déplacement sur l'axe horizontal ajustée en fonction des collisions
        """
        dx = self.check_collides_with_world(dx, world)
        dx = self.check_collides_with_entities(dx, world)
        
        return dx
    
    def check_collides_with_world(self, dx: int, world) -> int:
        """Vérifie les collisions entre la balle et les tuiles du monde

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            world (World): monde dans lequel la balle se trouve
        
        Returns:
            int: distance de déplacement sur l'axe horizontal ajustée en fonction des collisions avec les tuiles
        """
        for tile in world.obstacle_list:
            next_x_position = self.rect.x + dx
            
            # Vérifie les collisions sur l'axe horizontal
            if tile.rect.colliderect(next_x_position, self.rect.y, self.rect.width, self.rect.height):
                self.finish_animation()
                dx = next_x_position - tile.rect.x
            
        return dx
    
    def check_collides_with_entities(self, dx: int, world) -> int:
        """Vérifie les collisions entre la balle et les entités du monde

        Args:
            world (World): monde dans lequel la balle se trouve
        
        Returns:
            int: distance de déplacement sur l'axe horizontal ajustée en fonction des collisions avec les entités
        """
        # Cette méthode vérifie d'abord si la balle touche le rectangle du sprite puis si elle touche son masque pour éviter les faux positifs
        # On ne vérifie pas directement les masques car cela peut être très coûteux en ressources
        
        # Vérifie si la balle touche le rectangle de l'ennemi
        possibly_collided_enemies_list = pygame.sprite.spritecollide(self, world.enemy_group, False)
        
        # Si la balle touche le rectangle ennemi, on vérifie si elle touche le masque de l'ennemi
        if possibly_collided_enemies_list:
            possibly_collided_enemies_group = pygame.sprite.Group(possibly_collided_enemies_list)
            
            touched_enemies = pygame.sprite.spritecollide(self, possibly_collided_enemies_group, False, pygame.sprite.collide_mask)
        
            for enemy in touched_enemies:
                enemy.health -= self.damage
                self.finish_animation()
                dx = 0
        
        # Vérifie si la balle touche le rectangle du joueur
        if pygame.sprite.spritecollide(self, world.player_group, False):
            # Vérifie si la balle touche le masque du joueur
            if pygame.sprite.spritecollide(self, world.player_group, False, pygame.sprite.collide_mask):
                world.player.health -= self.damage
                self.finish_animation()
        
        return dx

    def finish_animation(self):
        """Met la balle en position end
        """
        #self.action = self.ANIMATION_TYPES[1]
        #self.frame_index = 0
        #self.image = self.animation[self.action][self.frame_index]
        #self.is_stopping = True
        self.continue_move = False
    
    def check_disappear(self) -> bool:
        """Vérifie si la balle doit disparaître
        
        Returns:
            bool: True si la balle doit disparaître, False sinon
        """
        return (self.rect.x < self.relative_initial_x - self.range) or (self.rect.x > self.relative_initial_x + self.range)

    def update(self, world):
        """Met à jour la balle
        
        Args:
            world (World): monde dans lequel la balle se trouve
        """
        if self.check_disappear() or (not self.continue_move):
            self.kill()
        else:
            self.update_animation()
            self.move(world)
    
    def update_animation(self):
        """Met à jour l'animation de la balle en fonction du temps
        """
        ANIMATION_COOLDOWN = 50
        # Met à jour l'image en fonction de la frame actuelle
        self.image = self.animation[self.action][self.frame_index]
        
        # Vérifie si assez de temps est passé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

	    # Si l'animation est terminée, remise de la première image
        if self.frame_index >= len(self.animation[self.action]):
            if self.action == self.ANIMATION_TYPES[1]:
                self.frame_index = len(self.animation[self.action]) - 1
                self.continue_move = False
            else:
                self.frame_index = 0
    
    def draw(self, screen: pygame.Surface):
        """Affiche la balle

        Args:
            screen (pygame.Surface): écran sur lequel la balle va être affichée
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
