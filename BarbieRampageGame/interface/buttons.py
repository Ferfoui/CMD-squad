import pygame
from _common import ColorValue

# Classe qui permet de créer les boutons
class Button():
    def __init__(self, x: int, y: int, image: pygame.Surface, clicked_image: pygame.Surface, scale, do_place_center: bool = False):
        """Initialise la classe Button

        Args:
            x (int): position en abscisses où le bouton va être créé
            y (int): position en ordonnées où le bouton va être créé
            image (Surface): image qui correspond au bouton
            clicked_image (Surface): image qui va s'afficher quand on clicke sur le bouton
            scale (int or float): nombre par lequel on multiplie la taille de l'image pour obtenir la taille du bouton
            do_place_center (bool, optional): si les coordonnées données sont celles du centre du bouton. False par défaut
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
    
    
    def set_clicked_img(self):
        """Affiche l'image qui indique que le bouton à été activé
        """
        self.do_draw_clicked_img = True
        self.update_time = pygame.time.get_ticks()


    def draw(self, screen: pygame.Surface) -> bool:
        """Affiche le bouton

        Args:
            screen (pygame.Surface): écran sur lequel le bouton doit être affiché

        Returns:
            bool: si l'utilisateur a clické sur le bouton
        """
        RESET_CLICKED_IMG_TIME = 200
        
        action = self.update()
        
        # Vérifie si le bouton a été clické depuis assez longtemps pour remettre l'image par defaut
        if pygame.time.get_ticks() - self.update_time > RESET_CLICKED_IMG_TIME:
            self.do_draw_clicked_img = False

        # Affiche le bouton à l'écran en fonction de s'il a été clické ou non
        if self.do_draw_clicked_img:
            screen.blit(self.clicked_image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
    def update(self):
        """Met à jour l'état du bouton
        """
        action = False

		# Position de la souris
        mpos = pygame.mouse.get_pos()

		# Vérifie si la souris a clické sur le bouton
        if self.rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                self.set_clicked_img()

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        return action


# Classe qui permet de créer les menus déroulant
class DropDown():
    def __init__(self, x: int, y: int, menu_colors: list[ColorValue, ColorValue], options_colors: list[ColorValue, ColorValue],
                 width: int, height: int, font: pygame.font.Font, main_option: str, options: list[str], do_place_center: bool = False):
        """Initialise un menu déroulant

        Args:
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
        self.menu_colors = menu_colors
        self.options_colors = options_colors
        self.rect = pygame.Rect(x, y, width, height)
        if do_place_center:
            self.rect.center = (x, y)
        self.font = font
        self.main_option = main_option
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.clicked = False
        
        self.update_time = pygame.time.get_ticks()
        
        
    def draw(self, screen: pygame.Surface) -> str:
        """Affiche le menu déroulant

        Args:
            screen (pygame.Surface): écran sur lequel le menu déroulant va être affiché

        Returns:
            str: option qui a été séléctionnée
        """
        self.update()
        
        BORDER_RADIUS = 4
        TEXT_COLOR = (0, 0, 0)
        # Affiche la case principale
        if not self.draw_menu:
            # Met des coins arrondis sur tous les bords
            pygame.draw.rect(screen, self.menu_colors[self.menu_active], self.rect, 2, border_radius = BORDER_RADIUS)
        else:
            # Met des coins arrondis sur les deux bords supérieurs
            pygame.draw.rect(screen, self.menu_colors[self.menu_active], self.rect, 2, border_top_left_radius = BORDER_RADIUS, border_top_right_radius = BORDER_RADIUS)
        text = self.font.render(self.main_option, 1, self.menu_colors[0])
        screen.blit(text, text.get_rect(center = self.rect.center))

        # Affiche les autres cases
        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                # Place le rectangle en dessous du précédent
                rect.y += (i + 1) * self.rect.height
                
                # Met des coins arrondis uniquement sur la dernière case
                if i == len(self.options) - 1:
                    pygame.draw.rect(screen, self.options_colors[i == self.active_option], rect, 0, border_bottom_left_radius = BORDER_RADIUS, border_bottom_right_radius = BORDER_RADIUS)
                else:
                    pygame.draw.rect(screen, self.options_colors[i == self.active_option], rect, 0)
                text = self.font.render(text, 1, TEXT_COLOR)
                screen.blit(text, text.get_rect(center = rect.center))
        
        return self.main_option
    
    def update(self) -> int:
        """Met à jour le menu déroulant

        Returns:
            int: index de l'option choisie, -1 si aucune option n'a été choisie
        """
        RESET_CLICKED_STATE_TIME = 20
        # Position de la souris
        mpos = pygame.mouse.get_pos()
        # Si la souris est se trouve sur le menu
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        # Vérifie la case sur laquelle la souris se trouve
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        # Arrête d'afficher le menu si la souris ne se trouve plus dessus
        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False
        
        # Reset l'update time si la souris a été clickée
        if pygame.mouse.get_pressed()[0] == 1:
            self.update_time = pygame.time.get_ticks()
           
        if pygame.time.get_ticks() - self.update_time > RESET_CLICKED_STATE_TIME:
            self.clicked = False
        
        # Vérifie si la souris a clické sur une des options du menu déroulant
        if pygame.mouse.get_pressed()[0] and not self.clicked:
            
            self.clicked = True
            # Si la souris se trouve sur la case principale, le menu doit s'afficher ou arrêter de s'afficher
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            
            # Si le menu est affiché et la souris se trouve sur une des options
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                self.main_option = self.options[self.active_option]
                return self.active_option

        return -1

class InputBox:
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font,color_active: ColorValue,
                 color_inactive: ColorValue, text='', do_place_center: bool = False):
        """Crée une entrée de texte

        Args:
            x (int): position sur l'axe horizontal
            y (int): position sur l'axe vertical
            width (int): largeur de l'entrée de texte
            height (int): hauteur de l'entrée de texte
            font (pygame.font.Font): police d'écriture utilisée
            color_active (ColorValue): couleur du texte quand l'entrée est utilisé
            color_inactive (ColorValue): couleur du texte quand l'entrée n'est pas utilisé
            text (str, optional): texte à afficher. '' par défaut
            do_place_center (bool, optional): si les coordonnées données sont celles du centre du menu. False par défaut
        """
        self.rect = pygame.Rect(x, y, width, height)
        if do_place_center:
            self.rect.center = (x, y)
        self.current_color = color_inactive
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.current_color)
        self.active = False

    def check_status(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.current_color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.current_color)

    def update(self, event: pygame.event.Event):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        
        self.check_status(event)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.current_color, self.rect, 2)
 