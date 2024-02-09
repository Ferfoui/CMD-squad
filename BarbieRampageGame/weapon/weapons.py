#Création des différentes armes du jeu

import pygame
import os
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
        super().__init__("AR-B4RB13", TEXTURES_ROOT+"weapons/AR_B4RB13.png", assets, weapon_width, x, y)
        
class Bullet():
    def __init__(self,scale):
        self.animation = self.load_animation(["bullet_start","bullet_end"],TEXTURES_ROOT+"weapons/bullets",scale)
        self.index = 0
        self.image = self.animation["bullet_start"][0]
    
    def load_animation(self, animation_types: list[str], texture_location: str, scale) -> dict[str, list[pygame.Surface]]:
        animation_dict = {}
        for animation in animation_types:
            animation_dict[animation] = []
			# Compte le nombre d'images qu'il y a dans le dossier
            number_of_frames = len(os.listdir(f"{texture_location}/{animation}"))
            for i in range(number_of_frames):
                # Charge l'image dans la mémoire
                img = pygame.image.load(f"{texture_location}/{animation}/{i:02}.png").convert_alpha()
                # Converti l'image pour qu'elle soit de la taille voulue
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                animation_dict[animation].append(img)
        return animation_dict
        
    def shoot(self, direction: int):
        pass
    
    def draw(self, screen: pygame.Surface):
        screen.blit()