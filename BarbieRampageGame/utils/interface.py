import pygame

from _common import ColorValue
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
            bool: si l'utilisateur a clické sur le bouton
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
    def __init__(self, background_color: ColorValue):
        """Initialise un Menu
        
        Args:
            background_color (ColorValue): couleur de l'arrière-plan
        """
        self.background_color = background_color
        self.images_to_draw = []
        self.buttons_to_draw = {}
        
    def add_image(self, image: pygame.Surface, x: int, y: int, do_place_center: bool):
        img_rect = image.get_rect()
        if do_place_center:
            img_rect.center = (x, y)
        else:
            img_rect.topleft = (x, y)
        
        self.images_to_draw.append((image, img_rect))
    
    def add_text_button(self, button_name: str, text_to_draw: str, font: pygame.font.Font, text_col: ColorValue, x: int, y: int, scale, do_place_center: bool):
        """Ajoute un bouton sous forme de texte au menu

        Args:
            button_name (str): nom du bouton
            text_to_draw (str): texte à afficher
            font (pygame.font.Font): police d'écriture
            text_col (ColorValue): couleur
            x (int): position en abscisses où le bouton va être créé
            y (int): position en ordonnées où le bouton va être créé
            scale (int or float): nombre par lequel le bouton va être redimensionné
            do_place_center (bool): si les coordonnées données sont celles du centre du texte
        """
        text_img = font.render(text_to_draw, True, text_col)
        button = Button(x, y, text_img, text_img, scale, do_place_center)
        self.buttons_to_draw[button_name] = button
    
    def draw(self, screen: pygame.Surface, do_draw_background: bool) -> list[str]:
        """Affiche les images et les boutons à l'écran et renvoie les noms des boutons qui ont été cliqués

        Args:
            screen (pygame.Surface): écran sur lequel le menu doit s'afficher
            do_draw_background (bool): si la couleur d'arrière-plan doit être affichée

        Returns:
            list[str]: noms des boutons qui ont été cliqués
        """
        if do_draw_background:
            screen.fill(self.background_color)
        
        for image, img_rect in self.images_to_draw:
            screen.blit(image, img_rect)
        
        clicked_buttons = []
        for button_name, button in self.buttons_to_draw.items():
            if button.draw(screen):
                clicked_buttons.append(button_name)
        
        return clicked_buttons

class HealthBar():
    def __init__(self, x, y, width, height, max_hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = max_hp
        self.max_hp = max_hp
    
    def draw(self,surface):
        #calcul du ratio de vie
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, "pink", (self.x, self.y, self.width * ratio, self.height))


