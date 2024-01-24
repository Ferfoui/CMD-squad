import pygame

from constants import *

# Classe qui permet de gérer les boutons
class Button():
    def __init__(self, x: int, y: int, image: pygame.Surface, clicked_image: pygame.Surface, scale, do_place_center: bool):
        """Initialise la classe Button

        Args:
            x (int): position en abscisses où le bouton va être créé
            y (int): position en ordonnées où le bouton va être créé
            image (Surface): image qui correspond au bouton
            clicked_image (Surface): image qui va s'afficher quand on clicke sur le bouton
            scale (int or float): nombre par lequel on multiplie la taille de l'image pour obtenir la taille du bouton
            do_place_center (bool): si les coordonnées données sont celles du centre du bouton
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.clicked_image = pygame.transform.scale(clicked_image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        if do_place_center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.clicked = False
        self.do_draw_clicked_img = False
        # Le temps pour pouvoir changer l'image pendant un certain temps
        self.update_time = pygame.time.get_ticks()

    def draw(self, screen: pygame.Surface) -> bool:
        """Affiche le bouton

        Args:
            screen (pygame.Surface): écran sur lequel le bouton doit être affiché

        Returns:
            bool: si l'utilisateur a clické dessus
        """
        RESET_CLICKED_IMG_TIME = 200
        action = False

		# Position de la souris
        pos = pygame.mouse.get_pos()

		# Vérifie si la souris a clické sur le bouton
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                self.set_clicked_img()

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                
        # Vérifie si le bouton a été clické depuis assez longtemps pour remettre l'image par defaut
        if pygame.time.get_ticks() - self.update_time > RESET_CLICKED_IMG_TIME:
            self.do_draw_clicked_img = False

        # Affiche le bouton à l'écran en fonction de s'il a été clické ou non
        if self.do_draw_clicked_img:
            screen.blit(self.clicked_image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
    def set_clicked_img(self):
        self.do_draw_clicked_img = True
        self.update_time = pygame.time.get_ticks()
        
# Classe qui gère les menus
class Menu():
    def __init__(self):
        """Initialise un Menu
        """
        self.buttons_to_draw = {}
    
    def add_text_button(self, button_name, text_to_draw, font, text_col: tuple[int, int, int], x: int, y: int, do_align_center: bool):
        button = Button()
    
    def draw(self, screen: pygame.Surface) -> list[str]:
        """Affiche les boutons à l'écran et renvoie les noms des boutons qui ont été cliqués

        Args:
            screen (pygame.Surface): écran sur lequel le menu doit s'afficher

        Returns:
            list[str]: noms des boutons qui ont été cliqués
        """
        clicked_buttons = []
        for button_name, button in self.buttons_to_draw.items():
            if button.draw(screen):
                clicked_buttons.append(button_name)
        
        return clicked_buttons
