import pygame

from constants import *

class Dummy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale):
        super().__init__()

        self.is_alive = True
        self.health = 100
        self.direction = 1

        self.image = self.load_image(ENEMIES_TEXTURES_LOCATION + "dummy.png", scale)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def load_image(self, texture_location, scale) -> pygame.Surface:
        # Charge l'image dans la mémoire
        img = pygame.image.load(f"{texture_location}").convert_alpha()
        # Converti l'image pour qu'elle soit de la taille voulue
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        return img   

    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher l'opps 

        Args:
            screen (Surface): fenêtre sur laquelle l'ennemi doit être affiché
        """
        screen.blit(self.image, self.rect)