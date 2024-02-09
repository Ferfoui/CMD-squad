#Création des différentes armes du jeu

import pygame
from utils import Assets

from constants import *
import utils

# La classe qui crée les armes
class Weapon():
    def __init__(self, weapon_name, texture_path, assets: utils.Assets, weapon_width, x, y):
        self.is_grab = False
        self.flip = False
        self.weapon_texture = self.init_textures(weapon_name, texture_path, assets, weapon_width)
        self.rect = self.weapon_texture.get_rect()
        self.rect.center = (x,y)

    def draw(self,screen: pygame.Surface):
        screen.blit(self.weapon_texture,self.rect)    
    
    def init_textures(self, name, texture_path, assets: utils.Assets, weapon_width: int) -> pygame.Surface:
        return assets.get_image(name, texture_path, weapon_width, 0)
    
    def shoot(self, direction: int):
        pass

class ARB4RB13(Weapon):
    def __init__(self, assets: Assets, weapon_width, x, y):
        super().__init__("AR-B4RB13", TEXTURES_ROOT + "weapons/AR_B4RB13.png", assets, weapon_width, x, y)