#Création des différentes armes du jeu

import pygame

from constants import *
import utils

# La classe qui crée les armes
class Weapon():
    def __init__(self, weapon_name, texture_path, assets: utils.Assets, weapon_width):
        self.is_grab = False
        self.flip = False
        self.weapon_texture = self.init_texture(weapon_name, texture_path, assets, weapon_width)
        
    
    def init_textures(name, texture_path, assets: utils.Assets, weapon_width: int):
        return assets.get_images(name, texture_path, weapon_width, 0)

class ARB4RB13():
    def __init__(self):
        
