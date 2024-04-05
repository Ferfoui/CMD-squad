import pygame, math, random

from constants import *
from . import Entity
import utils

class Enemy(Entity):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets, texture_location: str, max_health = 100, speed: int = 1, scale: float = 1):
        """Crée un ennemi

        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            tile_size (int): taille des tuiles
            assets (utils.Assets): classe qui contient les assets du jeu
            texture_location (str): position de la texture
            max_health (int, optional): vie maximale de l'ennemi. 100 par défaut.
            speed (int, optional): vitesse de l'ennemi. 1 par défaut.
            scale (float, optional): facteur de redimensionnement. 1 par défaut.
        """
        self.texture_location = texture_location
        super().__init__(x, y, max_health, tile_size, assets, speed, scale)
        
        self.size_factor = tile_size * SPRITE_SCALING
        
        self.relative_initial_x = x
        
        # Variable pour la hitbox
        self.mask = pygame.mask.from_surface(self.image)
        
    def define_entity_rect(self, x: int, y: int, assets: utils.Assets, scale: float) -> pygame.Rect:
        """Méthode qui crée le rectangle de l'ennemi

        Args:
            x (int): position en x
            y (int): position en y
            assets (utils.Assets): classe contenant les assets
            scale (float): facteur de redimensionnement
        
        Returns:
            pygame.Rect: rectangle de l'ennemi
        """
        self.image = assets.load_scaled_image(self.texture_location, scale * self.size_factor)

        rect = self.image.get_rect()
        rect.center = (x, y)
        
        # Crée la hitbox exacte de l'ennemi
        self.mask = pygame.mask.from_surface(self.image)
        
        return rect
    
    def get_head_y(self) -> int:
        """Récupère la position de la tête de l'ennemi

        Returns:
            int: position de la tête de l'ennemi
        """
        return self.rect.y + (self.rect.height // 4)
        
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
                offset_between_tile = tile.rect.left - self.hitbox.x
                dx = offset_between_tile - self.hitbox.width  * self.direction
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
            self.vel_y = self.apply_gravity(self.vel_y)
            dy += self.vel_y
            
            # Vérifie les collisions
            dx, dy = self.check_collides(dx, dy, world)
        
        self.move_entity_position(dx, dy, world)
    
    def apply_gravity_recursively(self, y_velocity: float, iterations: int, gravity_factor: float = 1) -> float:
        """Méthode qui applique la gravité à l'ennemi
        
        Args:
            y_velocity (float): vitesse de déplacement sur l'axe vertical
            iterations (int): nombre d'itérations à appliquer sur la gravité
            gravity_factor (int, optional): facteur de gravité. 1 par défaut.
        """
        if iterations > 0:
            y_velocity += self.apply_gravity(y_velocity, gravity_factor) + self.apply_gravity_recursively(y_velocity, iterations - 1, gravity_factor)
        else:
            y_velocity += self.apply_gravity(y_velocity, gravity_factor)
        
        return y_velocity
    
    def move_entity_position(self, dx: int, dy: int, world):
        """Méthode qui permet de déplacer la position de l'ennemi

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
        """
        super().move_entity_position(dx, dy, world)
        
        self.relative_initial_x += world.scroll.screen_scroll
    
    def ai(self, world):
        """Méthode qui permet de déplacer l'ennemi de manière autonome

        Args:
            world (World): monde dans lequel l'ennemi se déplace
        """
        self.move(world)
    
    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher l'opps 

        Args:
            screen (Surface): fenêtre sur laquelle l'ennemi doit être affiché
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
        if self.display_debug:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
            pygame.draw.rect(screen, (0, 0, 255), self.rect, 1)

class MovingEnemy(Enemy):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets, texture_location: str, max_health = 100, speed: int = 1, scale: float = 1):
        """Crée un ennemi qui peut se déplacer

        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            tile_size (int): taille des tuiles
            assets (utils.Assets): classe qui contient les assets du jeu
            texture_location (str): position de la texture
            max_health (int, optional): vie maximale de l'ennemi. 100 par défaut.
            speed (int, optional): vitesse de l'ennemi. 1 par défaut.
            scale (float, optional): facteur de redimensionnement. 1 par défaut.
        """
        super().__init__(x, y, tile_size, assets, texture_location, max_health, speed, scale)

        self.is_running = False
    
    def move(self, world, move_right: bool = False, move_left: bool = False):
        """Méthode qui permet de déplacer l'ennemi

        Args:
            world (World): Monde dans lequel l'ennemi se déplace
            move_right (bool, optional): si l'ennemi doit se déplacer vers la droite. False par défaut.
            move_left (bool, optional): si l'ennemi doit se déplacer vers la gauche. False par défaut.
        """
        dx = 0
        dy = 0
        self.is_running = False
        
        if self.is_alive:
            
            if move_left:
                dx -= self.speed
                self.is_running = True
                self.flip = True
                self.direction = -1
            if move_right:
                dx += self.speed
                self.is_running = True
                self.flip = False
                self.direction = 1
            
            # Application de la gravité
            self.vel_y = self.apply_gravity(self.vel_y)
            dy += self.vel_y
            
            # Vérifie les collisions
            dx, dy = self.check_collides(dx, dy, world)
        
        self.move_entity_position(dx, dy, world)

class IntelligentEnemy(MovingEnemy):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets, texture_location: str, max_health = 100, speed: int = 1, scale: float = 1):
        """Crée un ennemi intelligent

        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            tile_size (int): taille des tuiles
            assets (utils.Assets): classe qui contient les assets du jeu
            texture_location (str): position de la texture
            max_health (int, optional): vie maximale de l'ennemi. 100 par défaut.
            speed (int, optional): vitesse de l'ennemi. 1 par défaut.
            scale (float, optional): facteur de redimensionnement. 1 par défaut.
        """
        super().__init__(x, y, tile_size, assets, texture_location, max_health, speed, scale)
        self.viewline = None
        
        self.moving_around_direction = 1
        
        self.moving_time = pygame.time.get_ticks()
        
        self.MOVEMENT_CHANGING_DELAY = 3000
    
    def ai(self, world):
        return super().ai(world)
    
    def can_see_player(self, world) -> bool:
        """Métode qui permet de vérifier si l'ennemi peut voir le joueur

        Args:
            world (World): monde dans lequel l'ennemi se déplace

        Returns:
            bool: si l'ennemi peut voir le joueur
        """
        sight_distance = 500 * self.size_factor
        dx = self.rect.x - world.player.rect.x
        dy = self.rect.y - world.player.rect.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance <= sight_distance:
            self.viewline = ((self.rect.centerx, self.get_head_y()), (world.player.rect.centerx, world.player.get_head_y()))
            
            for tile in world.obstacle_list:
                if tile.rect.clipline(self.viewline[0], self.viewline[1]):
                    return False
            return True
        
        self.viewline = None
        
        return False
        
    def move_around(self, world, distance: int = 400):
        """Méthode qui permet de faire déplacer l'ennemi autour d'un point

        Args:
            world (World): monde dans lequel l'ennemi se déplace
            distance (int, optional): distance autour du point. 100 par défaut.
        """
        last_moving_around_direction = self.moving_around_direction
    
        scaled_distance = distance * self.size_factor
        
        # Vérifie si l'ennemi est à la bonne distance
        if self.rect.x < (self.relative_initial_x - scaled_distance):
            self.moving_around_direction = 1
        elif self.rect.x > (self.relative_initial_x + scaled_distance):
            self.moving_around_direction = -1

        # Vérifie si l'ennemi doit changer de direction de manière aléatoire
        elif pygame.time.get_ticks() - self.moving_time > self.MOVEMENT_CHANGING_DELAY:
            random_list = [self.moving_around_direction] * 30 + [-self.moving_around_direction]
            self.moving_around_direction = random.choice(random_list)
        
        # Vérifie si la direction de l'ennemi a changé
        if last_moving_around_direction != self.moving_around_direction:
            self.moving_time = pygame.time.get_ticks()
        
        self.move(world, self.moving_around_direction == 1, self.moving_around_direction == -1)
    
    def move(self, world, move_right: bool = False, move_left: bool = False):
        """Méthode qui permet de déplacer l'ennemi

        Args:
            world (World): monde dans lequel l'ennemi se déplace
            move_right (bool, optional): si l'ennemi doit se déplacer vers la droite. False par défaut.
            move_left (bool, optional): si l'ennemi doit se déplacer vers la gauche. False par défaut.
        """
        dx = 0
        dy = 0
        self.is_running = False
        
        if self.is_alive:
            
            if move_left:
                dx -= self.speed
                self.is_running = True
                self.flip = True
                self.direction = -1
            if move_right:
                dx += self.speed
                self.is_running = True
                self.flip = False
                self.direction = 1
            
            # Vérifie si l'ennemi doit sauter
            if (not self.jump) and (not self.in_air) and \
                (self.predict_collides(dx, dy, world) or self.predict_void(dx, dy, world)):
                
                self.vel_y = -14 * self.size_factor
                self.jump = True
                self.in_air = True
            
            # Application de la gravité
            self.vel_y = self.apply_gravity(self.vel_y)
            dy += self.vel_y
            
            # Vérifie les collisions
            dx, dy = self.check_collides(dx, dy, world)
        
        self.move_entity_position(dx, dy, world)
    
    def predict_collides(self, dx: int, dy: int, world) -> bool:
        """Vérifie si l'ennemi va rentrer en collision avec un obstacle

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
            world (World): monde dans lequel le joueur se déplace
        
        Returns:
            bool: si l'ennemi va rentrer en collision avec un obstacle dans le prochain déplacement
        """
        next_x_position = self.hitbox.x + dx
        next_y_position = self.hitbox.y + dy
        
        for tile in world.obstacle_list:
            
            # Vérifie les collisions sur l'axe horizontal
            if tile.rect.colliderect(next_x_position, next_y_position, self.hitbox.width, self.hitbox.height):
                return True
        
        return False
    
    def predict_void(self, dx, dy, world) -> bool:
        """Vérifie si l'ennemi va tomber dans le vide

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
            world (World): monde dans lequel le joueur se déplace
        
        Returns:
            bool: si l'ennemi va tomber dans le vide dans le prochain déplacement
        """
        next_x_position = self.hitbox.x + dx
        next_y_position = self.hitbox.y + dy + self.apply_gravity(self.vel_y)
        
        tile_collide = True
        for tile in world.obstacle_list:
            
            # Vérifie si l'ennemi va tomber dans un vide de 5 fois sa taille
            if tile.rect.colliderect(next_x_position, next_y_position, self.hitbox.width, self.hitbox.height * 5):
                tile_collide = False
                break
        
        return tile_collide
    
    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        
        if self.display_debug and self.viewline:
            pygame.draw.line(screen, (255, 0, 0), self.viewline[0], self.viewline[1])

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
        super().__init__(x, y, tile_size, assets, ENEMIES_TEXTURES_LOCATION + "ken.png", speed = 2, scale = scale)
    
    def ai(self, world):
        """Méthode qui permet de déplacer Ken vers le joueur
        
        Args:
            world (World): monde dans lequel Ken se déplace
        """
        if self.can_see_player(world):
            move_right = world.player.rect.x > (self.rect.right + 2 * self.size_factor)
            move_left = world.player.rect.right < (self.rect.x - 2 * self.size_factor)
            self.move(world,move_right,move_left)
        else:
            self.move_around(world)

    def attackRect(self):
        """Méthode qui permet de définir la zone d'attaque de Ken
        """
        width = int(self.rect.width * 0.8)
        height = int(self.rect.height * 0.23)
        
        if not self.flip:
            x = self.rect.right
        else:
            x = self.rect.left - width
        
        y = self.rect.y + self.rect.height * 0.4
        
        attack_rect = pygame.Rect(x, y, width, height)
        
        return attack_rect
    
    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        
        #pygame.draw.rect(screen, COLOR_ORANGE, self.attackRect(), 2)