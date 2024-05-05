import pygame
import os
import json

from constants import *

# Classe qui permet de gérer les paramètres modifiables du jeu
class Settings():
    def __init__(self):
        """Initialise la classe Settings dans laquelle se trouve les paramètres du jeu
        """
        self.SETTINGS_LOCATION = os.path.join(SAVE_ROOT, "settings.json")
        self.set_default_settings()
        
        self.load_settings()
        self.assets = None
    
    def set_default_settings(self):
        """Initialise les paramètres par défaut
        """
        self.do_draw_game_time = False
        self.do_draw_hitboxes = False
        
        self.screen_width = 700
        self.screen_height = int(self.screen_width * 0.8)
        
        self.volume = 0.5
        
        self.set_default_keybinds()
    
    def set_default_keybinds(self):
        """Défini la configuration des touches dans sa valeur par défaut
        """
        self.keybinds = {}
        self.keybinds['move_left'] = pygame.K_q
        self.keybinds['move_right'] = pygame.K_d
        self.keybinds['move_jump'] = pygame.K_SPACE
    
    
    def load_settings(self):
        """Charge les paramètres sauvegardés
        """
        # Charge les paramètres si le fichiers existe
        if os.path.exists(self.SETTINGS_LOCATION):
            print("Loading game settings")
            # Ouverture du fichier json
            with open(self.SETTINGS_LOCATION, 'r') as settingsfile:
                settings_json = json.load(settingsfile)
            
            try:
                # L'écran
                self.screen_width = settings_json['screensize']['width']
                self.screen_height = settings_json['screensize']['height']
                
                # Les touches
                self.keybinds = settings_json['keybinds']
                
                # Les autres paramètres
                self.volume = settings_json['sound']['volume']
                
                # Pour debug
                self.do_draw_game_time = settings_json['debug']['do_draw_game_time']
                self.do_draw_hitboxes = settings_json['debug']['do_draw_hitboxes']
                print("Settings have been loaded")
            
            except KeyError:
                print("Error while loading settings, using default settings for unknown keys")
        
        # Définit le nom de la résolution à partir de la largeur de l'écran
        # Cela permet de savoir quelle résolution est utilisée pour le menu des options
        self.resolution_name = list(RESOLUTION_OPTIONS.keys())[1]
        for name, resolution in RESOLUTION_OPTIONS.items():
            if self.screen_width == resolution[0]:
                self.resolution_name = name
                return
    
    def save_settings(self):
        """Sauvegarde les paramètres configurés par le joueur
        """
        print("Saving game settings")
        if not os.path.isdir(SAVE_ROOT):
            print(f"creating '{os.path.abspath(SAVE_ROOT)}' folder")
            os.mkdir(SAVE_ROOT)
        
        # Dictionnaire qui sera converti en json
        settings_dict = {}
        
        settings_dict['screensize'] = {'width': self.screen_width, 'height': self.screen_height}
        
        settings_dict['keybinds'] = self.keybinds
        
        settings_dict['sound'] = {}
        settings_dict['sound']['volume'] = self.volume
        
        settings_dict['debug'] = {}
        settings_dict['debug']['do_draw_game_time'] = self.do_draw_game_time
        settings_dict['debug']['do_draw_hitboxes'] = self.do_draw_hitboxes
        
        # Transformation du dictionnaire en json
        settings_json = json.dumps(settings_dict, indent=4)
        # Création du fichier json
        with open(self.SETTINGS_LOCATION, 'w') as outfile:
            outfile.write(settings_json)
        
        print("Settings have been saved")
    
    def set_assets(self, assets):
        """Défini les assets du jeu

        Args:
            assets (Assets): les assets du jeu
        """
        self.assets = assets
    
    def change_volume(self, volume: float):
        """Change le volume de la musique

        Args:
            volume (float): volume de la musique
        """
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)
        
        if self.assets:
            self.assets.set_volume(self.volume)
    