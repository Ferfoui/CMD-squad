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

### Sprites ###

# Classe qui permet de créer le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed:int | float, scale:int | float):
        """Initialise la classe Player

        Args:
            x (int): position en abscisses où le joueur va être créé
            y (int): position en ordonnées où le joueur va être créé
            speed (int or float): vitesse à laquelle se déplace le joueur (en pixel par frame)
            scale (int or float): nombre par lequel on multiplie la taille du Sprite pour obtenir la taille du joueur
        """
        pygame.sprite.Sprite.__init__(self)
        self.is_alive = True
        self.speed = speed
        self.flip = False
        self.move_left = False
        self.move_right = False
        
        self.animation_dict = {}
        self.frame_index = 0
        
        # charge toutes les images du joueur
        # animation_types = ['Idle', 'Run', 'Jump', 'Death']
        animation_types = ['Idle']
        for animation in animation_types:

            self.animation_dict[animation] = []

			# compte le nombre d'image qu'il y a dans le dossier
            number_of_frames = len(os.listdir(f"{PLAYER_TEXTURES_LOCATION}default/{animation}"))
            for i in range(number_of_frames):
                img = pygame.image.load(f"{PLAYER_TEXTURES_LOCATION}default/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.animation_dict[animation].append(img)

        self.action = animation_types[0]
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def set_movement_right(self, doMove: bool):
        """Méthode qui définie si le joueur va aller à droite

        Args:
            doMove (bool): si le joueur va aller à droite
        """
        self.move_right = doMove

    def set_movement_left(self, doMove: bool):
        """Méthode qui définie si le joueur va aller à gauche

        Args:
            doMove (bool): si le joueur va aller à gauche
        """
        self.move_left = doMove

    def move(self):
        """Méthode qui permet de mettre à jour la position du joueur
        """
        dx = 0
        dy = 0
        
        if self.is_alive:
            if self.move_right:
                dx += self.speed
            if self.move_left:
                dx -= self.speed
        
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        """Méthode qui doit être appelée à chaque frame pour mettre à jour les caractéristiques du joueur
        """
        self.move()

    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher le joueur sur la fenêtre voulue

        Args:
            screen (pygame.Surface): fenêtre sur laquelle le joueur doit être afficher
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)