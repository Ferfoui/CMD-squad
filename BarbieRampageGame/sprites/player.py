import pygame, os

from constants import *
import utils
import interface as gui

# Classe qui permet de créer le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets):
        """Initialise la classe Player

        Args:
            x (int): position en abscisses où le joueur va être créé
            y (int): position en ordonnées où le joueur va être créé
            tile_size (int): taille d'une tuile en pixel
            assets (utils.Assets): classe qui contient les assets du jeu
        """
        super().__init__()
        
        self.size_factor = tile_size * SPRITE_SCALING
        
        # Valeurs de départ pour la santé, les kills et les balles
        self.health = 100
        self.kills = 100
        self.bullets = 30
        
        # Variables pour l'état du joueur
        self.is_alive = True
        self.speed = 5 * self.size_factor
        
        self.flip = False # Variable qui permet de faire tourner le sprite du joueur quand il bouge dans l'autre sens
        self.direction = 1 # Direction du joueur (1 s'il est tourné vers la droite et -1 s'il est vers la gauche)
        self.vel_y = 0 # Vitesse du joueur sur l'axe vertical
        
        self.jump = False # Si le joueur saute
        
        self.in_air = True # Si le joueur est dans les airs
        
        self.is_running = False # Si le joueur est en train de courir

        # Valeur du temps pour l'animation du joueur
        self.update_time = pygame.time.get_ticks()
        
        #self.ANIMATION_TYPES = ['Idle', 'Run', 'Jump', 'Death']
        self.ANIMATION_TYPES = ['Idle', 'Run']
        
        scale = 1.5 * self.size_factor
        # Dictionnaire dans lequel il y a les frames des différentes animations du joueur
        self.animation_dict = self.load_animation(assets, self.ANIMATION_TYPES, f"{PLAYER_TEXTURES_LOCATION}default", scale)
        # Index de la frame actuelle du joueur
        self.frame_index = 0
        
        # Met le joueur en position Idle
        self.action = self.ANIMATION_TYPES[0]
        # Met l'image correspondant à son action
        self.image = self.animation_dict[self.action][self.frame_index]
        # Crée le rectangle du joueur
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Crée une hitbox approximative du joueur
        self.hitbox = self.rect.copy()
        self.hitbox.width = self.rect.width * 1/2
        self.hitbox.height = self.rect.height * 31/32
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom
        
        # Crée la hitbox exacte du joueur
        self.mask = pygame.mask.from_surface(self.image)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    

    def create_health_bar(self, x: int, y: int, assets: utils.Assets):
        self.health_bar = gui.HealthBar(x, y, 256, self.health, assets)

    def create_kill_counter(self, x: int, y: int, assets: utils.Assets):
        self.kill_counter = gui.KillCounter(x, y, 256, self.kills, assets)
    
    def create_bullet_counter(self, x: int, y: int, assets: utils.Assets):
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
            self.vel_y += GRAVITY * self.size_factor
            if self.vel_y > 10:
                self.vel_y = 10
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
        self.move_player_position(dx, dy, world, settings)
    
    def move_player_position(self, delta_x: int, delta_y: int, world, settings: utils.Settings):
        """Change la position du joueur

        Args:
            delta_x (int): distance de laquelle le joueur s'est déplacé sur l'axe horizontal
            delta_y (int): distance de laquelle le joueur s'est déplacé sur l'axe vertical
            world (World): monde dans lequel le joueur se déplace
            settings (Settings): classe qui contient les paramètres du jeu
        """
        self.rect.x += delta_x
        self.rect.y += delta_y
        
        #self.hitbox.center = self.rect.center
        
        self.update_scrolling(world, delta_x, settings)
    
    def check_collides(self, dx: int, dy: int, world) -> tuple[int, int]:
        
        for tile in world.obstacle_list:
            next_x_position = self.hitbox.x + dx
            next_y_position = self.hitbox.y + dy + 1
            
            # Vérifie les collisions sur l'axe horizontal
            if tile.rect.colliderect(next_x_position, self.hitbox.y, self.hitbox.width, self.hitbox.height):
                dx = 0
            # Vérifie les collisions sur l'axe vertical
            if tile.rect.colliderect(self.hitbox.x, next_y_position, self.hitbox.width, self.hitbox.height):
                # Vérifie la hitbox des deux masks en cas de collision entre rectangle
                # Vérifie si le joueur est en dessous d'une platforme
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.rect.top
                # Vérifie si le joueur touche le sol
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    self.jump = False
                    dy = tile.rect.top - self.rect.bottom
        
        return dx, dy
    
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


    def check_if_alive(self):
        """Vérifie si le joueur est vivant"""
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.is_alive = False

    def update(self):
        """Méthode qui doit être appelée à chaque frame pour mettre à jour les caractéristiques du joueur"""
        
        self.check_if_alive()
        
        self.hitbox.bottom = self.rect.bottom
        self.hitbox.centerx = self.rect.centerx

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
        #pygame.draw.rect(screen, COLOR_ORANGE, self.rect, 2)
        #pygame.draw.rect(screen, COLOR_RED, self.hitbox, 2)
