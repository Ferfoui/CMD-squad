import pygame
import os
from Constants import *

### Interface ###

# Classe qui permet de gérer les boutons
class Button():
    def __init__(self, x: int, y: int, image: pygame.Surface, scale:int | float):
        """Initialise la classe Button

        Args:
            x (int): position en abscisses où le bouton va être créé
            y (int): position en ordonnées où le bouton va être créé
            image (pygame.Surface): image qui correspond au bouton
            scale (int or float): nombre par lequel on multiplie la taille de l'image pour obtenir la taille du bouton
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen: pygame.Surface) -> bool:
        """Affiche le bouton

        Args:
            screen (pygame.Surface): écran sur lequel le bouton doit être affiché

        Returns:
            bool: si l'utilisateur a clické dessus
        """
        action = False

		# position de la souris
        pos = pygame.mouse.get_pos()

		# vérifie si la souris a clické sur le bouton
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

		# affiche le bouton sur l'écran
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Classe qui permet de gérer le scrolling de l'écran
class Scroll():
    def __init__(self):
        self.THRESH = 200
        self.screen_scroll = 0
        self.bg_scroll = 0

    def set_screen_scroll(self, screen_scroll: int):
        self.screen_scroll = screen_scroll
        self.bg_scroll -= screen_scroll

### Sprites ###

# Classe qui permet de créer le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scroll: Scroll, speed:int | float, scale:int | float):
        """Initialise la classe Player

        Args:
            x (int): position en abscisses où le joueur va être créé
            y (int): position en ordonnées où le joueur va être créé
            scroll (Scroll): valeurs de scrolling dont le joueur a besoin
            speed (int or float): vitesse à laquelle se déplace le joueur (en pixel par frame)
            scale (int or float): nombre par lequel on multiplie la taille du Sprite pour obtenir la taille du joueur
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.scroll = scroll
        
        self.is_alive = True
        self.speed = speed
        self.health = 100

        # Variable qui permet de faire tourner le sprite du joueur quand il bouge dans l'autre sens
        self.flip = False
        self.move_left = False
        self.move_right = False
        # Direction du joueur (1 s'il est tourné vers la droite et -1 s'il est vers la gauche)
        self.direction = 1
        # Vitesse du joueur sur l'axe vertical
        self.vel_y = 0
        # Si le joueur saute
        self.is_jumping = False
        # Si le joueur veut sauter
        self.do_jump = False
        # Si le joueur est dans les airs
        self.in_air = True

        # Valeur absolue du temps pour l'animation du joueur
        self.update_time = pygame.time.get_ticks()
        
        # Dictionnaire dans lequel il y a les frames que va utiliser le joueur
        self.animation_dict = {}
        # Index de la frame actuelle du joueur
        self.frame_index = 0
        
        # Charge toutes les images du joueur
        #self.ANIMATION_TYPES = ['Idle', 'Run', 'Jump', 'Death']
        self.ANIMATION_TYPES = ['Idle']
        for animation in self.ANIMATION_TYPES:

            self.animation_dict[animation] = []

			# Compte le nombre d'image qu'il y a dans le dossier
            number_of_frames = len(os.listdir(f"{PLAYER_TEXTURES_LOCATION}default/{animation}"))
            for i in range(number_of_frames):
                # Charge l'image dans la mémoire
                img = pygame.image.load(f"{PLAYER_TEXTURES_LOCATION}default/{animation}/{i}.png").convert_alpha()
                # Converti l'image pour qu'elle soit de la taille voulue
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.animation_dict[animation].append(img)

        # Met le joueur en position Idle
        self.action = self.ANIMATION_TYPES[0]
        # Met l'image correspondant à son action
        self.image = self.animation_dict[self.action][self.frame_index]
        # Crée la hitbox du joueur
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def set_movement_right(self, do_move: bool):
        """Méthode qui définie si le joueur va aller à droite

        Args:
            do_move (bool): si le joueur va aller à droite
        """
        self.move_right = do_move

    def set_movement_left(self, do_move: bool):
        """Méthode qui définie si le joueur va aller à gauche

        Args:
            do_move (bool): si le joueur va aller à gauche
        """
        self.move_left = do_move
    
    def jump(self):
        """Fais sauter le joueur"""
        if not self.in_air:
            self.do_jump = True
            #self.update_action(self.ANIMATION_TYPES[2]) # "Jump"

    def move(self, world):
        """Méthode qui permet de mettre à jour la position du joueur

        Args:
            world (World): monde dans lequel le joueur se déplace
        """
        dx = 0
        dy = 0
        
        if self.is_alive:
            # Mouvements à droite et à gauche
            if self.move_right:
                dx += self.speed
                self.flip = False
                self.direction = 1
            if self.move_left:
                dx -= self.speed
                self.flip = True
                self.direction = -1
            
            # Sauts
            if self.do_jump == True and self.in_air == False:
                self.vel_y = -11
                self.do_jump = False
                self.is_jumping = True
                self.in_air = True
            elif self.in_air == False:
                self.is_jumping = False
            
            # Application de la gravité
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y
            
            # Vérifie les colisions
            for tile in world.obstacle_list:
                # Vérifie les collisions sur l'axe horizontal
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Vérifie les collisions sur l'axe vertical
                if tile[1].colliderect(self.rect.x, self.rect.y + dy + 1, self.width, self.height):
                    # Vérifie si le joueur est en dessous d'une platforme
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    # Vérifie si le joueur touche le sol
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom
        
            if self.is_jumping:
                #self.update_action(self.ANIMATION_TYPES[2]) # "Jump"
                pass
            elif dx != 0:
                #self.update_action(self.ANIMATION_TYPES[1]) # "Run"
                pass
            else:
                self.update_action(self.ANIMATION_TYPES[0]) # "Idle"
            
        
        # Met à jour la position du joueur
        self.rect.x += dx
        self.rect.y += dy
        
        # Met à jour le scrolling de l'écran en fonction de la position du joueur
        if self.rect.right > SCREEN_WIDTH - self.scroll.THRESH or self.rect.left < self.scroll.THRESH:
            self.rect.x -= dx
            self.scroll.set_screen_scroll(-dx)
        else:
            self.scroll.set_screen_scroll(0)
    
    def update_animation(self):
        """Met à jour l'animation du joueur"""
        ANIMATION_COOLDOWN = 100
        # Met à jour l'image en fonction de la frame actuelle
        self.image = self.animation_dict[self.action][self.frame_index]

        # Vérifie si assez de temps est passé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

	    # Si l'animation est terminée, remise de la première image
        if self.frame_index >= len(self.animation_dict[self.action]):
            if self.action == self.ANIMATION_TYPES[3]:
                self.frame_index = len(self.animation_dict[self.action]) - 1
            else:
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
            self.update_action(self.ANIMATION_TYPES[3]) # "Death"

    def update(self):
        """Méthode qui doit être appelée à chaque frame pour mettre à jour les caractéristiques du joueur"""
        
        self.check_if_alive()

        #self.update_animation()

    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher le joueur

        Args:
            screen (pygame.Surface): fenêtre sur laquelle le joueur doit être afficher
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


### Monde ###

class World():
    def __init__(self, tile_size: int):
        """Initialise la classe World

        Args:
            tile_size (int): longueur des côtés des tuiles
        """
        self.tile_size = tile_size
        self.obstacle_list = []

        # Charge toutes les images
        self.img_dict = {}
        for tile_name in TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES:
            img = pygame.image.load(f'{TILES_TEXTURES_LOCATION}{tile_name}.png').convert_alpha()
            img = pygame.transform.scale(img, (tile_size, tile_size * img.get_height() // img.get_width()))
            self.img_dict[tile_name] = img

    def process_data(self, data, scroll: Scroll) -> Player:
        """Méthode qui génére le monde en fonction des données données

        Args:
            data (list): données du monde
            scroll (Scroll): valeurs de scrolling utilisés par les objets dans le monde

        Returns:
            Player: joueur créé dans le monde
        """
        self.scroll = scroll
        
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                # Si c'est un objet comme un bloc ou une entité
                if tile in TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES:
                    img = self.img_dict[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * self.tile_size
                    img_rect.y = y * self.tile_size
                    tile_data = (img, img_rect)
                    if tile in OBSTACLES_TILE_TYPES:
                        self.obstacle_list.append(tile_data)
                # Si c'est un personnage comme le joueur ou un ennemi
                elif tile in PLAYER_AND_ENEMIES_TILE_TYPES:
                    # Si c'est le point de spawn du joueur
                    if tile == PLAYER_AND_ENEMIES_TILE_TYPES[0]:
                        player = Player(x * self.tile_size, y * self.tile_size, self.scroll, 5, 2)
        
        return player
    
    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher le monde

        Args:
            screen (pygame.Surface): fenêtre sur laquelle le monde doit être afficher
        """
        for tile in self.obstacle_list:
            tile[1][0] += self.scroll.screen_scroll
            screen.blit(tile[0], tile[1])


