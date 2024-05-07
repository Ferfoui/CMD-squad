import pygame

from enemy import IntelligentEnemy
import utils

class Boss(IntelligentEnemy):
    def __init__(self, x: int, y: int, tile_size: int, assets: utils.Assets, texture_location: str, max_health: int = 200, speed: int = 1, scale: float = 1):
        super().__init__(x , y, tile_size, assets, texture_location, max_health, speed, scale)

    def normal_attack(self):
        pass

    def special_attack(self):
        pass

    def ai(self, world):
        pass

