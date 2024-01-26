import os

import pygame
from constants import *
import utils

# Classe du menu de démarrage
class StartMenu(utils.Menu):
    def __init__(self, assets: utils.Assets):
        """Initialise le menu de démarrage

        Args:
            assets (Assets): classe qui contient les assets
        """
        super().__init__(COLOR_WHITE_AZURE)
        
        # Ajoute l'image au milieu de l'écran
        self.add_image(assets.cmd_img, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, True)
        # Ajoute le bouton de démarrage
        self.add_text_button("start", "PRESS ENTER TO START :3", assets.default_font, COLOR_HOT_PINK, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.96, 1, True)


class DeathMenu(utils.Menu):
    def __init__(self, assets: utils.Assets):
        """Initialise le menu de démarrage

        Args:
            assets (Assets): classe qui contient les assets
        """
        super().__init__(COLOR_DARK)
        
        #self.death_animation = self.load_death_animation(f"{TEXTURES_ROOT}background/falling/", f"{TEXTURES_ROOT}background/grounding/")
        
        # Ajoute le bouton de démarrage
        self.add_text_button("respawn", "PRESS ENTER TO RESPAWN T^T", assets.default_font, COLOR_HOT_PINK, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.96, 1, True)
        
    def load_death_animation(self, falling_texture_location, grounding_texture_location):
        animation_dict = {}
        
        scale = 2
        
        animation_dict['falling'] = []
		# Compte le nombre d'image qu'il y a dans le dossier
        falling_number_of_frames = len(os.listdir(falling_texture_location))
        for i in range(falling_number_of_frames):
            # Charge l'image dans la mémoire
            img = pygame.image.load(f"{falling_texture_location}{i}.png").convert_alpha()
            # Converti l'image pour qu'elle soit de la taille voulue
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            animation_dict['falling'].append(img)
            
        animation_dict['grounding'] = []
        # Compte le nombre d'image qu'il y a dans le dossier
        falling_number_of_frames = len(os.listdir(falling_texture_location))
        for i in range(falling_number_of_frames):
            # Charge l'image dans la mémoire
            img = pygame.image.load(f"{grounding_texture_location}{i}.png").convert_alpha()
            # Converti l'image pour qu'elle soit de la taille voulue
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            animation_dict['grounding'].append(img)

        return animation_dict

