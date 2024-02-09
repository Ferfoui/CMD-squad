import pygame, os

from constants import *

# Classe pour les balles
class Bullet(pygame.sprite.Sprite):
    def __init__(self, scale, x: int, y: int, direction: int):
        super().__init__()
        
        self.direction = direction
        self.flip = direction < 0
        
        self.ANIMATION_TYPES = ["bullet_start", "bullet_end"]
        
        self.animation = self.load_animation(self.ANIMATION_TYPES, TEXTURES_ROOT + "weapons/bullets", scale)
        self.index = 0
        
        # Valeur du temps pour l'animation de la balle
        self.update_time = pygame.time.get_ticks()
        
        self.continue_move = True
    
        # Met la balle en position start
        self.action = self.ANIMATION_TYPES[self.index]
        # Met l'image correspondant à son action
        self.image = self.animation_dict[self.action][self.frame_index]
        # Crée le rectangle de la balle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Crée la hitbox de la balle
        self.mask = pygame.mask.from_surface(self.image)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        
    def load_animation(self, animation_types: list[str], texture_location: str, scale) -> dict[str, list[pygame.Surface]]:
        """Charge l'animation de la balle

        Args:
            animation_types (list[str]): noms des animations
            texture_location (str): position des textures
            scale (int or float): échelle de la taille de la texture

        Returns:
            dict[str, list[pygame.Surface]]: dictionnaire de listes de frames
        """
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
    
    
    def update_animation(self):
        ANIMATION_COOLDOWN = 50
        # Met à jour l'image en fonction de la frame actuelle
        self.image = self.animation_dict[self.action][self.frame_index]
        
        # Vérifie si assez de temps est passé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

	    # Si l'animation est terminée, remise de la première image
        if self.frame_index >= len(self.animation_dict[self.action]):
            if self.action == self.ANIMATION_TYPES[1]:
                self.frame_index = len(self.animation_dict[self.action]) - 1
                self.continue_move = False
            else:
                self.frame_index = 0
    
    def draw(self, screen: pygame.Surface):
        """Affiche la balle

        Args:
            screen (pygame.Surface): écran sur lequel la balle va être affichée
        """
        self.update_animation()
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
