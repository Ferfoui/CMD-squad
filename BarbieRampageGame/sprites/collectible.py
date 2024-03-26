import pygame

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
    

class ItemBox(Collectible):
    def __init__(self, x, y):
        super().__init__(x ,y)
