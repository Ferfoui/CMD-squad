import pygame
import json

# Classe qui permet de gérer les paramètres modifiables du jeu
class Settings():
    def __init__(self):
        """Initialise la classe Settings dans laquelle se trouve les paramètres du jeu
        """
        self.set_default_keybinds()
        self.do_draw_game_time = True
    
    def load_settings(self, file_path: str):
        pass
    
    def save_settings(self, file_path: str):
        pass
    
    def set_default_keybinds(self):
        """Défini la configuration des touches dans sa valeur par défaut
        """
        self.keybinds = {}
        self.keybinds['move_left'] = pygame.K_q
        self.keybinds['move_right'] = pygame.K_d
        self.keybinds['move_jump'] = pygame.K_SPACE