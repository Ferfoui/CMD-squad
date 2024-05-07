import pygame

from enemy import IntelligentEnemy
import utils

class Boss(IntelligentEnemy):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets, texture_location: str, max_health: int = 200, speed: int = 1, scale: float = 1, animation_list: list = None):
        super().__init__(x , y, tile_size, assets, texture_location, max_health, speed, scale)


class SuperDuperHyperMegaKenMonster(Boss):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets, scale: float = 1):
        ANIMATION_LIST = ['Idle', 'Attack1', 'Attack2', 'Dead']
        super().__init__(x, y, tile_size, assets, "enemies/ken/ken.png", 1000, 3, scale)

    def normal_attack(self):
        pass

    def special_attack(self):
        pass

    def ai(self, world):
        pass
    
    