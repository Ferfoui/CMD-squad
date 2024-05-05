import pygame

from _common import ColorValue
from constants import *
from utils import Assets
from .buttons import Button, DropDown, Cursor

# Classe qui gère les menus
class Menu():
    def __init__(self, background_color: ColorValue):
        """Initialise un Menu
        
        Args:
            background_color (ColorValue): couleur de l'arrière-plan
        """
        self.background_color = background_color
        self.images_to_draw = {}
        self.buttons_to_draw = {}
        self.drop_downs_to_draw = {}
        self.cursors_to_draw = {}
        
    def add_image(self, image: pygame.Surface, x: int, y: int, do_place_center: bool = False, name: bool = None):
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
        
        if name == None:
            name = "image:" + str(len(self.images_to_draw))
        
        self.images_to_draw[name] = (image, img_rect)
    
    def add_text(self, text: str, font: pygame.font.Font, text_col: ColorValue, x: int, y: int, do_place_center: bool = False, name: str = None):
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
        
        if name == None:
            name = text
        
        self.images_to_draw[name] = (text_img, img_rect)
    
    def add_button(self, button_name: str, image: pygame.Surface, image_on_click: pygame.Surface, x: int, y: int, scale: float, do_place_center: bool = False):
        """Ajoute un bouton au menu

        Args:
            button_name (str): nom du bouton
            image (pygame.Surface): image du bouton
            image_on_click (pygame.Surface): image du bouton quand il est cliqué
            x (int): position en abscisses où le bouton va être créé
            y (int): position en ordonnées où le bouton va être créé
            scale (float): nombre par lequel le bouton va être redimensionné
            do_place_center (bool, optional): si les coordonnées données sont celles du centre du texte. False par défaut
        """
        button = Button(x, y, image, image_on_click, scale, do_place_center)
        self.buttons_to_draw[button_name] = button
    
    def add_text_button(self, button_name: str, text_to_draw: str, font: pygame.font.Font, text_col: ColorValue, x: int, y: int, scale: float, do_place_center: bool = False):
        """Ajoute un bouton sous forme de texte au menu

        Args:
            button_name (str): nom du bouton
            text_to_draw (str): texte à afficher
            font (pygame.font.Font): police d'écriture
            text_col (ColorValue): couleur
            x (int): position en abscisses où le bouton va être créé
            y (int): position en ordonnées où le bouton va être créé
            scale (float): nombre par lequel le bouton va être redimensionné
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
    
    def add_cursor(self, cursor_name: str, x: int, y: int, width: int, height: int, line_color: ColorValue, cursor_color: ColorValue, min_value: int, max_value: int,
                   default_value: int, do_place_center: bool = False):
        """Ajoute un curseur au menu

        Args:
            cursor_name (str): nom du curseur
            x (int): position en abscisses où le curseur va être créé
            y (int): position en ordonnées où le curseur va être créé
            width (int): largeur du curseur
            height (int): hauteur du curseur
            line_color (ColorValue): couleur de la ligne sur laquelle le curseur se déplace
            cursor_color (ColorValue): couleur du curseur
            min_value (int): valeur minimale du curseur
            max_value (int): valeur maximale du curseur
            default_value (int): valeur par défaut du curseur
            do_place_center (bool, optional): si les coordonnées données sont celles du centre du curseur. False par défaut
        """
        cursor = Cursor(x, y, width, height, line_color, cursor_color, min_value, max_value, do_place_center)
        cursor.set_value(default_value)
        self.cursors_to_draw[cursor_name] = cursor
    
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
        
        for image, img_rect in self.images_to_draw.values():
            screen.blit(image, img_rect)
        
        self.gui_values = {}
        for button_name, button in self.buttons_to_draw.items():
            self.gui_values[button_name] = button.draw(screen)

        for drop_down_name, drop_down in self.drop_downs_to_draw.items():
            self.gui_values[drop_down_name] = drop_down.draw(screen)
        
        for cursor_name, cursor in self.cursors_to_draw.items():
            self.gui_values[cursor_name] = cursor.draw(screen)
            
        return self.gui_values

    def set_cursors_off(self):
        """Désactive les curseurs
        """
        for cursor in self.cursors_to_draw.values():
            cursor.set_off()

class HealthBar():
    def __init__(self, x: int, y: int, width: int, max_hp: int, assets: Assets):
        """Initialise la barre de vie

        Args: 
            x (int): position en abscisses où la barre de vie va être créee
            y (int): position en ordonnées où la barre de vie va être créee
            width (int): largeur de la barre de vie 
            max_hp (int): valeur maximale des points de vie
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
        """Affiche la barre de vie sur l'écran

        Args:
            screen (pygame.Surface): surface de l'écran sur laquelle dessiner la barre de vie
        """
        # Calcul du ratio de vie
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, COLOR_HEALTH_PINK, (self.x + 5, self.y + 5, (self.width - 10) * ratio, self.height - 10))
        screen.blit(self.image, (self.x, self.y))

class BulletCounter():
    #a delete + 30 munis 
    def __init__(self, x, y, width: int, max_bullet: int, assets: Assets):
        """Initialise le compteur de munitions
        
        Args:
            x (int): position en abscisses où le compteur de munitions va être créé
            y (int): position en ordonnées où le compteur de munitions va être créé
            width (int): largeur du compteur de munitions
            max_bullet (int): nombre maximal de munitions
            assets (Assets): classe des assets
        """
        self.x = x
        self.y = y
        self.width = width
        self.bullets= max_bullet
        self.max_bullet = max_bullet
        #self.image = assets.get_image("bullet_count", f"{TEXTURES_ROOT}gui/Bullet_count")
        self.image = assets.get_image("bullet_counter", f"{TEXTURES_ROOT}gui/Bullet_count.png", width)
        self.height = self.image.get_height()
        self.font = assets.default_font


    def draw(self, screen: pygame.Surface):
        """Affiche le compteur de munitions sur l'écran
        
        Args:
            screen (pygame.Surface): surface de l'écran sur laquelle afficher le compteur de munitions
        """
        screen.blit(self.image, (self.x, self.y))
        draw_text(screen, f"Bullets: {self.bullets} ", self.font, COLOR_DARK, self.x+50, self.y, False)
        

class KillCounter():
    def __init__(self, x: int, y: int, width: int, max_kl: int, assets: Assets):
        """Initialise le compteur de kills
        
        Args:
            x (int): Position en abscisses où le compteur de kills va être créé
            y (int): Position en ordonnées où le compteur de kills va être créé
            width (int): Largeur du compteur de kills
            max_kl (int): Nombre maximal de kills
            assets (Assets): Classe des assets
        """
        self.x = x
        self.y = y
        self.width = width
        self.kl = max_kl
        self.max_kl = max_kl
        self.image = assets.get_image("kill_counter", f"{TEXTURES_ROOT}gui/Kill_bar.png", width)
        self.height = self.image.get_height()
        
    def draw(self, screen: pygame.Surface):
        """Affiche le compteur de kills sur l'écran
        
        Args:
            screen (pygame.Surface): écran sur laquelle afficher le compteur de kills
        """
        # Calcul du ratio de kills
        ratio = self.kl / self.max_kl
        pygame.draw.rect(screen, COLOR_RED, (self.x + 5, self.y + 5, (self.width - 10) * ratio, self.height - 10))
        screen.blit(self.image, (self.x, self.y))

### Fonctions ###
def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, text_col: ColorValue, x: int, y: int, do_place_center: bool = False):
    """Fonction fiche du texte

    Args:
        screen (pygame.pygame.Surface): écran sur lequel le texte doe doit être aff
        text (str): texte qui doit être affiché
        font (pygame.font.Font): police à utiliser
        text_col (tuple[int, int, int]): couleur du texte (racismo no)
        x (int): position n abscisses où le texte va être affiché
        y (int): position s où le text ordonnées où lere afe va 
        do_place_center (bool, optional): si les coordonsies scellesonn centonnées sont celles dutexte. False xtefaut
    """
    img = font.render(text, True, text_col)
    if do_place_center:
        img_rect = img.get_rect()
        img_rect.center = (x, y)
        screen.blit(img, img_rect)
    else:
        screen.blit(img, (x, y))
