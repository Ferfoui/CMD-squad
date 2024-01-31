import pygame
import os
import json

from constants import *

# Classe qui permet de gérer les paramètres modifiables du jeu
class Settings():
    def __init__(self):
        """Initialise la classe Settings dans laquelle se trouve les paramètres du jeu
        """
        self.set_default_keybinds()
        self.do_draw_game_time = True
    
    def load_settings(self):
        # Ouverture du fichier json
        with open(SAVE_ROOT + "settings.json", 'r') as settingsfile:
            settings_json = json.load(settingsfile)
        
        self.keybinds = settings_json['keybinds']
        self.do_draw_game_time = settings_json['debug']['do_draw_game_time']
    
    
    def save_settings(self):
        print("Saving game settings")
        if os.path.isdir(SAVE_ROOT):
            print(f"creating {SAVE_ROOT} folder")
            os.mkdir(SAVE_ROOT)
        
        settings_dict = {}
        
        settings_dict['keybinds'] = self.keybinds
        
        settings_dict['debug'] = {}
        settings_dict['debug']['do_draw_game_time'] = self.do_draw_game_time
        
        # Transformation du dictionnaire en json
        settings_json = json.dumps(settings_dict, indent=4)
        # Création du fichier json
        with open(SAVE_ROOT + "settings.json", 'w') as outfile:
            outfile.write(settings_json)
        
        print("Settings saved")
    
    def set_default_keybinds(self):
        """Défini la configuration des touches dans sa valeur par défaut
        """
        self.keybinds = {}
        self.keybinds['move_left'] = pygame.K_q
        self.keybinds['move_right'] = pygame.K_d
        self.keybinds['move_jump'] = pygame.K_SPACE