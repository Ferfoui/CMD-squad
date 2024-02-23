import pygame

from _common import ColorValue
from constants import *
from utils import Assets

from .buttons import Button, DropDown

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
        self.drop_downs_to_draw = {}
        
    def add_image(self, image: pygame.Surface, x: int, y: int, do_place_center: bool = False):
        """Ajoute une image au menu

        Args:
            image (pygame.Surface): image à ajouter
            x (int): position en abscisses de l'image
            y (int): position en ordonnée de l'image
            do_place_center (bool, optional): si les coordonnées données sont celles du centre du texte. False par défaut
        """
        img_rect = image.get_rect()
        if do_place_center:
            img_rect.center = (x, y)
        else:
            img_rect.topleft = (x, y)
        
        self.images_to_draw.append((image, img_rect))
    
    def add_text(self, text: str, font: pygame.font.Font, text_col: ColorValue, x: int, y: int, do_place_center: bool = False):
        """Ajoute du texte au menu

        Args:
            text (str): texte qui doit être affiché
            font (pygame.font.Font): police d'écriture
            text_col (ColorValue): couleur du texte
            x (int): position en abscisses où le texte va être affiché
            y (int): position en ordonnées où le texte va être affiché
            do_place_center (bool, optional): si les coordonnées données sont celles du centre du texte. False par défaut
        """
        text_img = font.render(text, True, text_col)
        
        if do_place_center:
            img_rect = text_img.get_rect(center = (x, y))
        else:
            img_rect = text_img.get_rect(topleft = (x, y))
        
        self.images_to_draw.append((text_img, img_rect))
    
    def add_text_button(self, button_name: str, text_to_draw: str, font: pygame.font.Font, text_col: ColorValue, x: int, y: int, scale, do_place_center: bool = False):
        """Ajoute un bouton sous forme de texte au menu

        Args:
            button_name (str): nom du bouton
            text_to_draw (str): texte à afficher
            font (pygame.font.Font): police d'écriture
            text_col (ColorValue): couleur
            x (int): position en abscisses où le bouton va être créé
            y (int): position en ordonnées où le bouton va être créé
            scale (int or float): nombre par lequel le bouton va être redimensionné
            do_place_center (bool, optional): si les coordonnées données sont celles du centre du texte. False par défaut
        """
        text_img = font.render(text_to_draw, True, text_col)
        button = Button(x, y, text_img, text_img, scale, do_place_center)
        self.buttons_to_draw[button_name] = button
    
    def add_drop_down(self, drop_down_name: str, x: int, y: int, menu_colors: list[ColorValue, ColorValue], options_colors: list[ColorValue, ColorValue],
                 width: int, height: int, font: pygame.font.Font, main_option: str, options: list[str], do_place_center: bool = False):
        """Ajoute un menu déroulant au menu

        Args:
            drop_down_name (str): nom du menu déroulant
            x (int): position en abscisses où le menu déroulant va être créé
            y (int): position en ordonnées où le menu déroulant va être créé
            menu_colors (list[ColorValue, ColorValue]): liste de la couleur de base et de la couleur active de l'option par défaut
            options_color (list[ColorValue, ColorValue]): liste de la couleur de base et de la couleur active des options
            width (int): largeur d'une case
            height (int): hauteur d'une case
            font (pygame.font.Font): police utilisée
            main_option (str): nom de l'option par défaut
            options (list[str]): noms des options
            do_place_center (bool, optional): si les coordonnées données sont celles du centre du menu. False par défaut
        """
        drop_down = DropDown(x, y, menu_colors, options_colors, width, height, font, main_option, options, do_place_center)
        self.drop_downs_to_draw[drop_down_name] = drop_down
    
    def draw(self, screen: pygame.Surface, do_draw_background: bool) -> dict[str, any]:
        """Affiche les images et les boutons à l'écran et renvoie les noms des boutons qui ont été cliqués

        Args:
            screen (pygame.Surface): écran sur lequel le menu doit s'afficher
            do_draw_background (bool): si la couleur d'arrière-plan doit être affichée

        Returns:
            dict[str, any]: dictionnaire avec les noms des gui et la valeur qui leur est assigné. Pour les 'Button' (dict[str, bool]), pour les 'DropDown' (dict[str, str])
        """
        if do_draw_background:
            screen.fill(self.background_color)
        
        for image, img_rect in self.images_to_draw:
            screen.blit(image, img_rect)
        
        self.gui_values = {}
        for button_name, button in self.buttons_to_draw.items():
            self.gui_values[button_name] = button.draw(screen)

        for drop_down_name, drop_down in self.drop_downs_to_draw.items():
            self.gui_values[drop_down_name] = drop_down.draw(screen)
            
        return self.gui_values

class HealthBar():
    def __init__(self, x, y, width: int, max_hp: int, assets: Assets):
        """Initialise la barre de vie

        Args: 
            x (int): position en abscisses où la barre de vie va être créee
            y (int): position en ordonnées où la barre de vie va être créee
            width (int): largeur de la barre de vie 
            assets (Assets): classe des assets
        """
        self.x = x
        self.y = y
        self.width = width
        self.hp = max_hp
        self.max_hp = max_hp
        self.image = assets.get_image("health_bar", f"{TEXTURES_ROOT}gui/Health_bar_empty.png", width)
        self.height = self.image.get_height()
        
    def draw(self, screen: pygame.Surface):
        # Calcul du ratio de vie
        ratio = self.hp / self.max_hp
        #pygame.draw.rect(screen, "red", (self.x + 10, self.y + 10, self.width - 20, self.height - 20))
        pygame.draw.rect(screen, COLOR_HEALTH_PINK, (self.x + 5, self.y + 5, (self.width - 10) * ratio, self.height - 10))
        screen.blit(self.image, (self.x, self.y))

class BulletCounter():
    #a delete + 30 munis 
    def __init__(self, x, y, width: int, max_bullet: int, assets: Assets):
        self.x = x
        self.y = y
        self.width = width
        self.bullet= max_bullet
        self.max_bullet = max_bullet
        #self.image = assets.get_image("bullet_count", f"{TEXTURES_ROOT}gui/Bullet_count")
        self.image = assets.debug_img
        self.height = self.image.get_height()
    def draw(self, screen):
        pass

class KillCounter():
    def __init__(self, x, y, width: int, max_kl: int, assets: Assets):
        self.x = x
        self.y = y
        self.width = width
        self.kl = max_kl
        self.max_kl = max_kl
        self.image = assets.get_image("kill_counter", f"{TEXTURES_ROOT}gui/Kill_bar.png", width)
        self.height = self.image.get_height()
        
    def draw(self, screen: pygame.Surface):
        # Calcul du ratio de kills
        ratio = self.kl / self.max_kl
        #pygame.draw.rect(screen, "red", (self.x + 10, self.y + 10, self.width - 20, self.height - 20))
        pygame.draw.rect(screen, COLOR_RED, (self.x + 5, self.y + 5, (self.width -10) * ratio, self.height - 10))
        screen.blit(self.image, (self.x, self.y))
    
def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, text_col: ColorValue, x: int, y: int, do_place_center: bool):
    """Fonction qui affiche du texte

    Args:
        screen (pygame.Surface): écran sur lequel le texte doit être affiché
        text (str): texte qui doit être affiché
        font (pygame.font.Font): police à utiliser
        text_col (tuple[int, int, int]): couleur du texte (racismo no)
        x (int): position en abscisses où le texte va être affiché
        y (int): position en ordonnées où le texte va être affiché
        do_place_center (bool): si les coordonnées données sont celles du centre du texte
    """
    img = font.render(text, True, text_col)
    if do_place_center:
        img_rect = img.get_rect()
        img_rect.center = (x, y)
        screen.blit(img, img_rect)
    else:
        screen.blit(img, (x, y))

