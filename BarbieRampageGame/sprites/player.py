import pygame, os

from constants import *
from . import Entity
import utils, weapon
import interface as gui

# Classe qui permet de créer le joueur
class Player(Entity):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets):
        """Initialise la classe Player

        Args:
            x (int): position en abscisses où le joueur va être créé
            y (int): position en ordonnées où le joueur va être créé
            tile_size (int): taille d'une tuile en pixel
            assets (utils.Assets): classe qui contient les assets du jeu
        """
        #self.ANIMATION_TYPES = ['Idle', 'Run', 'Jump', 'Death']
        self.ANIMATION_TYPES = ['Idle', 'Run']
        super().__init__(x, y, 100, tile_size, assets, speed = 5, scale = 1.5)
        
        # Valeurs de départ pour les kills et les balles
        self.kills = 100
        self.bullets = 30
        
        # Classe contenant l'arme du joueur
        self.weapon_holder = WeaponHolder()
        
        # Variables pour l'état du joueur
        self.is_running = False # Si le joueur est en train de courir

        # Valeur du temps pour l'animation du joueur
        self.update_time = pygame.time.get_ticks()
        
        # Crée la hitbox exacte du joueur
        self.mask = pygame.mask.from_surface(self.image)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def define_entity_rect(self, x: int, y: int, assets: utils.Assets, scale) -> pygame.Rect:
        """Méthode qui crée le rectangle et qui charge les animations du joueur

        Args:
            x (int): position en x
            y (int): position en y
            assets (utils.asset): classe contenant les assets
            scale (float, optional): facteur de redimensionnement

        Returns:
            pygame.Rect: rectangle de l'entité
        """
        # Dictionnaire dans lequel il y a les frames des différentes animations du joueur
        self.animation_dict = self.load_animation(assets, self.ANIMATION_TYPES, f"{PLAYER_TEXTURES_LOCATION}default", scale * self.size_factor)
        # Index de la frame actuelle du joueur
        self.frame_index = 0
        
        # Met le joueur en position Idle
        self.action = self.ANIMATION_TYPES[0]
        # Met l'image correspondant à son action
        self.image = self.animation_dict[self.action][self.frame_index]
        # Crée le rectangle du joueur
        rect = self.image.get_rect()
        rect.center = (x, y)
        
        # Crée la hitbox exacte du joueur
        self.mask = pygame.mask.from_surface(self.image)
        
        return rect

    def define_entity_hitbox(self, entity_rect: pygame.Rect) -> pygame.Rect:
        """Méthode qui crée la hitbox de l'entité

        Args:
            entity_rect (pygame.Rect): rectangle de l'entité

        Returns:
            pygame.Rect: hitbox de l'entité
        """
        hitbox = entity_rect.copy()
        # Redimensionne la hitbox pour qu'elle colle à la taille du joueur
        hitbox.width = entity_rect.width * 1/2
        hitbox.height = entity_rect.height * 31/32
        hitbox.centerx = entity_rect.centerx
        hitbox.bottom = entity_rect.bottom
        
        return hitbox

    def create_health_bar(self, x: int, y: int, assets: utils.Assets):
        """Crée la barre de vie du joueur

        Args:
            x (int): position en abscisses où la barre de vie va être créée
            y (int): position en ordonnées où la barre de vie va être créée
            assets (utils.Assets): classe qui contient les assets du jeu
        """
        self.health_bar = gui.HealthBar(x, y, 256, self.health, assets)

    def create_kill_counter(self, x: int, y: int, assets: utils.Assets):
        """Crée le compteur de kills du joueur

        Args:
            x (int): position en abscisses où le compteur de kills va être créé
            y (int): position en ordonnées où le compteur de kills va être créé
            assets (utils.Assets): classe qui contient les assets du jeu
        """
        self.kill_counter = gui.KillCounter(x, y, 256, self.kills, assets)
    
    def create_bullet_counter(self, x: int, y: int, assets: utils.Assets):
        """Crée le compteur de balles du joueur

        Args:
            x (int): position en abscisses où le compteur de balles va être créé
            y (int): position en ordonnées où le compteur de balles va être créé
            assets (utils.Assets): classe qui contient les assets du jeu
        """
        self.bullet_counter = gui.BulletCounter(x, y, 64, self.bullets, assets)
    
    def load_animation(self, assets: utils.Assets, animation_types: list[str], texture_location: str, scale) -> dict[str, list[pygame.Surface]]:
        """Méthode qui permet de charger les animations du joueur

        Args:
            assets (utils.Assets): classe qui contient les assets du jeu
            animation_types (list[str]): liste qui contient les noms des animations
            texture_location (str): chemin vers les textures
            scale (int or float): nombre par lequel on multiplie la taille du Sprite pour obtenir la taille du joueur

        Returns:
            dict[str, list[Surface]]: dictionnaire qui contient les listes d'images à afficher pour animer le joueur
        """
        animation_dict = {}
        
        for animation in animation_types:
            animation_dict[animation] = []
			# Compte le nombre d'image qu'il y a dans le dossier
            number_of_frames = len(os.listdir(f"{texture_location}/{animation}"))
            for i in range(number_of_frames):
                # Charge l'image et la redimensionne
                img = assets.load_scaled_image(f"{texture_location}/{animation}/{i:02}.png", scale)
                # Ajoute l'image à la liste des images de l'animation
                animation_dict[animation].append(img)
        
        return animation_dict
    
    def get_head_y(self) -> int:
        """Renvoie la position en ordonnées de la tête du joueur"""
        return self.rect.top + self.rect.height // 6

    def move(self, world, settings: utils.Settings):
        """Méthode qui permet de mettre à jour la position du joueur

        Args:
            world (World): monde dans lequel le joueur se déplace
            settings (Settings): classe qui contient les paramètres du jeu
        """
        dx, dy = 0, 0
        self.is_running = False
        
        # Les touches entrées par l'utilisateur
        input_key = pygame.key.get_pressed()
        
        if self.is_alive:
            # Mouvement à gauche
            if input_key[settings.keybinds['move_left']]:
                dx -= self.speed
                self.is_running = True
                self.flip = True
                self.direction = -1
            # Mouvement à droite
            if input_key[settings.keybinds['move_right']]:
                dx += self.speed
                self.is_running = True
                self.flip = False
                self.direction = 1
                # Ne pas faire courir Barbie si on appuie en même temps sur la touche pour aller à droite et à gauche
                if dx == 0:
                    self.is_running = False

            # Sauts
            if input_key[settings.keybinds['move_jump']] and self.jump == False and self.in_air == False:
                self.vel_y = -14 * self.size_factor
                self.jump = True
                self.in_air = True
            
            # Application de la gravité
            self.vel_y = super().apply_gravity(self.vel_y)
            dy += self.vel_y
            
            # Vérifie les colisions
            dx, dy = self.check_collides(dx, dy, world)

            # Si le joueur à un mouvement vertical alors il est dans les airs
            if abs(dy) > 0:
                self.in_air = True
        
            # Tuer le joueur s'il sort de l'écran par le bas
            if self.rect.top + dy > settings.screen_height:
                self.health = 0
                self.vel_y = 0

        # Met à jour la position du joueur
        self.move_entity_position(dx, dy, world, settings)
    
    def move_entity_position(self, delta_x: int, delta_y: int, world, settings: utils.Settings):
        """Change la position du joueur

        Args:
            delta_x (int): distance de laquelle le joueur s'est déplacé sur l'axe horizontal
            delta_y (int): distance de laquelle le joueur s'est déplacé sur l'axe vertical
            world (World): monde dans lequel le joueur se déplace
            settings (Settings): classe qui contient les paramètres du jeu
        """
        self.rect.x += delta_x
        self.rect.y += delta_y
        
        self.update_scrolling(world, delta_x, settings)
        
        self.weapon_holder.move(delta_x + world.scroll.screen_scroll, delta_y, self.direction)
    
    def update_scrolling(self, world, dx: int, settings: utils.Settings):
        """Met à jour le scrolling en fonction de la position du joueur par rapport à l'écran

        Args:
            world (World): monde dans lequel le joueur se déplace
            dx (int): distance de laquelle le joueur s'est déplacé sur l'axe horizontal
            settings (Settings): classe qui contient les paramètres du jeu
        """
        
        right_thresh_position = settings.screen_width - world.scroll.thresh
        left_thresh_position = world.scroll.thresh
        
        # Taille du monde en pixel
        world_size = (world.level_length * world.tile_size) - settings.screen_width
        
        # Si le joueur est proche de la bordure droite ou gauche, faire défiler l'écran
        if ((self.rect.right > right_thresh_position) and (world.scroll.bg_scroll < world_size))\
				or ((self.rect.left < left_thresh_position) and (world.scroll.bg_scroll > abs(dx))):
            world.scroll.set_screen_scroll(-dx)
        # Remet le scrolling du monde à son état initial s'il faut le
        elif not (world.scroll.bg_scroll > abs(dx)):
            world.scroll.set_screen_scroll(world.scroll.bg_scroll)
        else:
            world.scroll.set_screen_scroll(0)
        
        self.rect.x += world.scroll.screen_scroll
    
    def update_animation(self):
        """Met à jour l'animation du joueur"""
        
        # Met l'animation qui correspond à ce que le joueur fait
        #if not self.is_alive:
        #    self.update_action(self.ANIMATION_TYPES[3]) # "Death"
        #elif self.jump == True:
        #    self.update_action(self.ANIMATION_TYPES[2]) # "Jump"
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

    def update_action(self, new_action: str):
        """Met à jour l'action que le joueur est en train d'effectuer

        Args:
            new_action (str): nom de l'action qu'il fait (dans la liste ANIMATION_TYPES)
        """
        # Vérifie si la nouvelle action est différente de celle d'avant
        if new_action != self.action:
            self.action = new_action
            # Remet à zéro les variables de l'animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        """Méthode qui doit être appelée à chaque frame pour mettre à jour les caractéristiques du joueur"""
        super().update()

        self.health_bar.hp = self.health
        self.kill_counter.kl = self.kills
        self.bullet_counter.bl = self.bullets

        self.update_animation()

    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher le joueur

        Args:
            screen (Surface): fenêtre sur laquelle le joueur doit être affiché
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        self.weapon_holder.draw(screen)
        
        #pygame.draw.rect(screen, COLOR_ORANGE, self.rect, 2)
        #pygame.draw.rect(screen, COLOR_RED, self.hitbox, 2)

class WeaponHolder():
    def __init__(self):
        """Classe qui permet de gérer l'arme que le joueur a équipé
        """

        self.weapon = None
        
        self.direction = 1
    
    def set_weapon(self, weapon: weapon.Weapon, coordinates: tuple[int, int]):
        """Équipe une nouvelle arme au joueur

        Args:
            weapon (weapon.Weapon): arme à équiper
            coordinates (tuple[int, int]): coordonnées de l'arme
        """
        self.x = coordinates[0]
        self.y = coordinates[1]
        
        self.weapon = weapon
    
    def move(self, delta_x: int, delta_y: int, direction: int):
        """Fait bouger l'arme que le joueur a équipé

        Args:
            delta_x (int): distance de laquelle l'arme doit être déplacée sur l'axe horizontal
            delta_y (int): distance de laquelle l'arme doit être déplacée sur l'axe vertical
            direction (int): direction dans laquelle le joueur regarde, 1 si c'est vers la droite et -1 si c'est vers la gauche
        """
        self.direction = direction
        
        if self.weapon != None:
            self.weapon.rect.x += delta_x
            self.weapon.rect.y += delta_y
            
            self.weapon.flip = self.direction != 1
    
    def shoot(self, bullet_group: pygame.sprite.Group, bullet_count: int) -> int:
        """Fait tirer l'arme que le joueur a équipé

        Args:
            bullet_group (pygame.sprite.Group): groupe de sprites dans lequel les balles vont être ajoutées
            bullet_count (int): nombre de balles que le joueur a

        Returns:
            int: nouveau nombre de balles après le tir
        """
        if self.weapon != None and bullet_count > 0:
            bullets_consuming = self.weapon.shoot(self.direction, bullet_group)
            bullet_count -= bullets_consuming
        
        if bullet_count < 0:
            bullet_count = 0
        
        return bullet_count
    
    def draw(self, screen: pygame.Surface):
        """Affiche l'arme que le joueur a équipé

        Args:
            screen (pygame.Surface): écran sur lequel l'arme doit être affichée
        """
        if self.weapon != None:
            self.weapon.draw(screen)
