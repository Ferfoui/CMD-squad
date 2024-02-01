import os
import random

import pygame
from constants import *
import utils

# Classe du menu de démarrage
class StartMenu(utils.Menu):
    def __init__(self, assets: utils.Assets, settings: utils.Settings):
        """Initialise le menu de démarrage

        Args:
            assets (Assets): classe qui contient les assets du jeu
            settings (Settings): classe qui contient les paramètres du jeu
        """
        super().__init__(COLOR_WHITE_AZURE)
        
        cmd_img = assets.get_image("cmd_img", ASSETS_ROOT + "casadojomojo.png", settings.screen_width // 2, 0)
        # Ajoute l'image au milieu de l'écran
        self.add_image(cmd_img, settings.screen_width // 2, settings.screen_height // 2, True)
        # Ajoute le bouton de démarrage
        self.add_text_button("start", "PRESS ENTER TO START :3", assets.default_font, COLOR_HOT_PINK, settings.screen_width//2, settings.screen_height * 0.96, 1, True)


class DeathMenu(utils.Menu):
    def __init__(self, assets: utils.Assets, settings: utils.Settings):
        """Initialise le menu de mort

        Args:
            assets (Assets): classe qui contient les assets du jeu
            settings (Settings): classe qui contient les paramètres du jeu
        """
        super().__init__(COLOR_DARK)
        
        # Valeur du temps pour l'animation
        self.update_time = pygame.time.get_ticks()
        
        self.death_animation = self.load_death_animation(f"{TEXTURES_ROOT}deathscreen/falling/", f"{TEXTURES_ROOT}deathscreen/landing/")
        self.frame_index = 0
        self.barbie_head_rect = self.death_animation['falling'][0].get_rect()
        
        # Intervalle en pourcent pour le positionnement aléatoire de la tête sur l'axe horizontal
        self.RANDOM_RANGE = (20, 70)
        
        self.reset_animation(settings.screen_width)
        
        # L'état actuel de l'animation
        self.head_actual_state = 'falling'
        
        # Ajoute le bouton de respawn
        self.add_text_button('respawn', "PRESS ENTER TO RESPAWN T^T", assets.default_font_bigger, COLOR_HOT_PINK, settings.screen_width//2, settings.screen_height * 0.9, 1, True)
    
    
    def load_death_animation(self, falling_texture_location: str, landing_texture_location: str) -> dict[str, list[pygame.Surface]]:
        """Charge l'animation de la tête qui tombe

        Args:
            falling_texture_location (str): position des textures qui représentent la tête qui tombe
            landing_texture_location (str): position des textures qui représentent la tête qui attérrit

        Returns:
            dict[str, list[pygame.Surface]]: dictionnaire qui contient les listes d'image de l'animation
        """
        animation_dict = {}
        
        scale = 2.5
        
        animation_dict['falling'] = []
		# Compte le nombre d'image qu'il y a dans le dossier
        falling_number_of_frames = len(os.listdir(falling_texture_location))
        for i in range(falling_number_of_frames):
            # Charge l'image dans la mémoire
            img = pygame.image.load(f"{falling_texture_location}{i}.png").convert_alpha()
            # Converti l'image pour qu'elle soit de la taille voulue
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            animation_dict['falling'].append(img)
            
        animation_dict['landing'] = []
        # Compte le nombre d'image qu'il y a dans le dossier
        falling_number_of_frames = len(os.listdir(landing_texture_location))
        for i in range(falling_number_of_frames):
            # Charge l'image dans la mémoire
            img = pygame.image.load(f"{landing_texture_location}{i}.png").convert_alpha()
            # Converti l'image pour qu'elle soit de la taille voulue
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            animation_dict['landing'].append(img)

        return animation_dict

    
    def update_death_animation(self) -> pygame.Surface:
        """Met à jour l'animation de mort (la tête qui tombe)

        Returns:
            pygame.Surface: image à afficher pour l'animation
        """
        
        ANIMATION_COOLDOWN = 50
        
        self.move_barbie_head()
        
        # Met à jour l'image en fonction de la frame actuelle
        image = self.death_animation[self.head_actual_state][self.frame_index]
        
        # Vérifie si assez de temps est passé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Si l'animation est terminée, remise de la première image
        if self.frame_index >= len(self.death_animation[self.head_actual_state]):
            if self.head_actual_state == 'landing':
                self.frame_index = len(self.death_animation[self.head_actual_state]) - 1
            else:
                self.frame_index = 0
        
        return image
    
    
    def move_barbie_head(self):
        """Fais bouger la tête de Barbie en fonction de la gravité et des obstacles
        """
        dy = 0
        
        dy += self.head_vel_y
        
        if self.barbie_head_rect.bottom + dy > self.buttons_to_draw['respawn'].rect.top:
            dy = self.buttons_to_draw['respawn'].rect.top - self.barbie_head_rect.bottom
            self.head_actual_state = 'landing'
            self.head_vel_y = 0
        else:
            self.head_vel_y += GRAVITY

        self.barbie_head_rect.y += dy
        

    def draw(self, screen: pygame.Surface, do_draw_background: bool) -> list[str]:
        """Affiche les images et les boutons à l'écran, renvoie les noms des boutons qui ont été cliqués et affiche l'animation de la tête de Barbie qui tombe

        Args:
            screen (pygame.Surface): écran sur lequel le menu doit s'afficher
            do_draw_background (bool): si la couleur d'arrière-plan doit être affichée

        Returns:
            list[str]: noms des boutons qui ont été cliqués
        """
        clicked_buttons = super().draw(screen, do_draw_background)
        
        head_img = self.update_death_animation()
        
        screen.blit(head_img, self.barbie_head_rect)
        
        return clicked_buttons
    
    
    def reset_animation(self, screen_width: int):
        """Remet les paramètres par défaut à l'animation du menu
        
        Args:
            screen_width (int): hauteur de l'écran en pixel
        """
        self.frame_index = 0
        self.head_actual_state = 'falling'
        
        # Vitesse de la tête sur l'axe des abscisses
        self.head_vel_y = 14
        
        # Positionnement de la tête de Barbie avec la position des abscisses aléatoire
        random_postion = random.randint(self.RANDOM_RANGE[0], self.RANDOM_RANGE[1]) / 100
        self.barbie_head_rect.bottomleft = (screen_width * random_postion, 0)
        
