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
        self.jump = False

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
            self.vel_y = self.apply_gravity(self.vel_y)
            dy += self.vel_y
            
            # Vérifie les collisions
            dx, dy = self.check_collides(dx, dy, world)
        
        self.move_enemy_position(dx, dy, world)
    
    def apply_gravity(self, y_velocity: float, gravity_factor: float = 1) -> float:
        """Méthode qui applique la gravité à l'ennemi
        
        Args:
            y_velocity (float): vitesse de déplacement sur l'axe vertical
            gravity_factor (int, optional): facteur de gravité. 1 par défaut.
        """
        y_velocity += GRAVITY * gravity_factor * self.size_factor
        if y_velocity > 10:
            y_velocity = 10
        
        return y_velocity
    
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
    
    def move_enemy_position(self, dx: int, dy: int, world):
        """Méthode qui permet de déplacer la position de l'ennemi

        Args:
            dx (int): distance de déplacement sur l'axe horizontal
            dy (int): distance de déplacement sur l'axe vertical
        """
        self.rect.x += dx + world.scroll.screen_scroll
        self.rect.y += dy
    
    def ai(self, world):
        """Méthode qui permet de déplacer l'ennemi de manière autonome

        Args:
            world (World): monde dans lequel l'ennemi se déplace
        """
        self.move(world)
    
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

class MovingEnemy(Enemy):
    def __init__(self, x: int, y: int, tile_size: int, scale: float, assets: utils.Assets, texture_location: str, speed: int):
        """Crée un ennemi qui peut se déplacer

        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            tile_size (int): taille des tuiles
            scale (float): facteur de redimensionnement
            assets (utils.Assets): classe qui contient les assets du jeu
            texture_location (str): position de la texture
            speed (int): vitesse de l'ennemi
        """
        super().__init__(x, y, tile_size, scale, assets, texture_location)
        
        self.speed = speed * self.size_factor
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
        
        self.move_enemy_position(dx, dy, world)

class IntelligentEnemy(MovingEnemy):
    def __init__(self, x: int, y: int, tile_size: int, scale: float, assets: utils.Assets, texture_location: str, speed: int):
        """Crée un ennemi intelligent

        Args:
            x (int): position de l'ennemi sur l'axe des abscisses
            y (int): position de l'ennemi sur l'axe des ordonnées
            tile_size (int): taille des tuiles
            scale (float): facteur de redimensionnement
            assets (utils.Assets): classe qui contient les assets du jeu
            texture_location (str): position de la texture
            speed (int): vitesse de l'ennemi
        """
        super().__init__(x, y, tile_size, scale, assets, texture_location, speed)
    
    def ai(self, world):
        return super().ai(world)
    
    def can_see_player(self, world) -> bool:
        """Métode qui permet de vérifier si l'ennemi peut voir le joueur

        Args:
            world (World): monde dans lequel l'ennemi se déplace

        Returns:
            bool: si l'ennemi peut voir le joueur
        """
        line = ((self.rect.centerx, self.rect.top), (world.player.rect.centerx, world.player.rect.top))
        sight_distance = 20 * self.size_factor
        dx = self.x - world.player.x
        dy = self.y - world.player.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance <= sight_distance:
            for tile in world.obstacle_list:
                if tile.rect.collidepoint(line[1]):
                    return False
            return True
        
        return False
    
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
        
        self.move_enemy_position(dx, dy, world)
    
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
        super().__init__(x, y, tile_size, scale, assets, ENEMIES_TEXTURES_LOCATION + "dummy.png", speed)

    def ai(self, world):
        """Méthode qui permet de déplacer l'ennemi vers le joueur

        Args:
            world (World): _description_
        """
        move_right = world.player.rect.x > self.rect.right + 3 * self.size_factor
        move_left = world.player.rect.right < self.rect.x - 3 * self.size_factor
        
        self.move(world, move_right, move_left)
