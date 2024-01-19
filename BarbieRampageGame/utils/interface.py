import pygame

from constants import *

# Classe qui permet de gérer les boutons
class Button():
    def __init__(self, x: int, y: int, image: pygame.Surface, clicked_image: pygame.Surface, scale):
        """Initialise la classe Button

        Args:
            x (int): position en abscisses où le bouton va être créé
            y (int): position en ordonnées où le bouton va être créé
            image (Surface): image qui correspond au bouton
            clicked_image (Surface): image qui va s'afficher quand on clicke sur le bouton
            scale (int or float): nombre par lequel on multiplie la taille de l'image pour obtenir la taille du bouton
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.clicked_image = pygame.transform.scale(clicked_image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.do_draw_clicked_img = False
        # Le temps pour pouvoir changer l'image pendant un certain temps
        self.update_time = pygame.time.get_ticks()

    def draw(self, screen: pygame.Surface) -> bool:
        """Affiche le bouton

        Args:
            screen (pygame.Surface): écran sur lequel le bouton doit être affiché

        Returns:
            bool: si l'utilisateur a clické dessus
        """
        RESET_CLICKED_IMG_TIME = 200
        action = False

		# Position de la souris
        pos = pygame.mouse.get_pos()

		# Vérifie si la souris a clické sur le bouton
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                self.set_clicked_img()

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                
        # Vérifie si le bouton a été clické depuis assez longtemps pour remettre l'image par defaut
        if pygame.time.get_ticks() - self.update_time > RESET_CLICKED_IMG_TIME:
            self.do_draw_clicked_img = False

        # Affiche le bouton à l'écran en fonction de s'il a été clické ou non
        if self.do_draw_clicked_img:
            screen.blit(self.clicked_image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
    def set_clicked_img(self):
        self.do_draw_clicked_img = True
        self.update_time = pygame.time.get_ticks()

# Classe qui gère les assets du jeu
class Assets():
    def __init__(self):
        """Initialise la classe assets dans laquelle se trouve toutes les images, les sons, les polices, etc...
        """
        ### Images ###
        # L'image du chargement du début
        self.cmd_img = self.load_image_keep_proportion(f"{ASSETS_ROOT}casadojomojo.png", SCREEN_WIDTH // 2)
        # L'image de débuggage
        self.debug_img = self.load_image(f"{TEXTURES_ROOT}debug.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Dictionnaire dans lequel se trouve les images qui se font charger de l'extérieur de la classe
        self.saved_external_images = {}
                
        ### Polices d'écriture ###
        self.default_font = pygame.font.Font(PS2P_FONT_LOCATION, 15)

    def load_image(self, texture_location: str, width: int, height: int) -> pygame.Surface:
        """Charge une image

        Args:
            texture_location (str): position de la texture
            width (int): largeur de l'image
            height (int): hauteur de l'image

        Returns:
            pygame.Surface: image chargé
        """
        image = pygame.image.load(texture_location).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image

    def load_image_keep_proportion(self, texture_location: str, width: int) -> pygame.Surface:
        """Charge une image en gardant les proportions

        Args:
            texture_location (str): position de la texture
            width (int): largeur de l'image

        Returns:
            pygame.Surface: image chargé
        """
        image = pygame.image.load(texture_location).convert_alpha()
        image = pygame.transform.scale(image, (width, width * image.get_height() // image.get_width()))
        return image
    
    def get_image(self, name: str, texture_location: str, width: int, height) -> pygame.Surface:
        """Renvoie l'image voulue et la sauvegarde pour ne pas avoir à la chargé plusieurs fois

        Args:
            name (str): nom de l'image
            texture_location (str): position de la texture
            width (int): largeur de l'image
            height (int | None): hauteur de l'image, si la hauteur n'est pas donnée, les proportions de l'image seront automatiquement conservées

        Returns:
            pygame.Surface: image demandée
        """
        # Vérifie si l'image n'a pas déjà été sauvegardée
        if name in self.saved_external_images.keys():
            return self.saved_external_images[name]
        
        # Charge l'image et la sauvegarde
        if height > 0:
            self.saved_external_images[name] = self.load_image(texture_location, width, height)
        else:
            self.saved_external_images[name] = self.load_image_keep_proportion(texture_location, width)
        
        return self.saved_external_images[name]
