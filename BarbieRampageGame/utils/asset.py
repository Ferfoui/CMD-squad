import pygame

from constants import *

# Classe qui gère les assets du jeu
class Assets():
    def __init__(self, settings):
        """Initialise la classe assets dans laquelle se trouve toutes les images, les sons, les polices, etc...
        """
        ### Images ###
        # L'image de débuggage
        self.debug_img = self.load_image(f"{TEXTURES_ROOT}gui/debug.png", settings.screen_width // 2, settings.screen_height // 2)
        
        # Dictionnaire dans lequel se trouve les images qui se font charger de l'extérieur de la classe
        self.saved_external_images = {}
        
        ### Polices d'écriture ###
        self.default_font = pygame.font.Font(PS2P_FONT_LOCATION, 15)
        self.default_font_bigger = pygame.font.Font(PS2P_FONT_LOCATION, 22)

        ### Les sons ###
        self.weapon_cross_sound = pygame.mixer.Sound(WEAPON_CROSS_SOUND_LOCATION)

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
    
    def load_scaled_image(self, texture_location: str, scale: float) -> pygame.Surface:
        """Charge une image et la redimensionne

        Args:
            texture_location (str): position de la texture
            scale (float): facteur de redimensionnement

        Returns:
            pygame.Surface: image chargé
        """
        image = pygame.image.load(texture_location).convert_alpha()
        image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
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
    
    def get_image(self, name: str, texture_location: str, width: int, height: int = 0) -> pygame.Surface:
        """Renvoie l'image voulue et la sauvegarde pour ne pas avoir à la chargé plusieurs fois

        Args:
            name (str): nom de l'image
            texture_location (str): position de la texture
            width (int): largeur de l'image
            height (int or None): hauteur de l'image, si la hauteur n'est pas donnée ou qu'elle est égale à 0, les proportions de l'image seront automatiquement conservées

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
    
    def get_scaled_image(self, name: str, texture_location: str, scale: float) -> pygame.Surface:
        """Renvoie l'image voulue et la sauvegarde pour ne pas avoir à la chargé plusieurs fois

        Args:
            name (str): nom de l'image
            texture_location (str): position de la texture
            scale (float): facteur de redimensionnement

        Returns:
            pygame.Surface: image demandée
        """
        # Vérifie si l'image n'a pas déjà été sauvegardée
        if name in self.saved_external_images.keys():
            return self.saved_external_images[name]
        
        # Charge l'image et la sauvegarde
        self.saved_external_images[name] = self.load_scaled_image(texture_location, scale)
        
        return self.saved_external_images[name]
