import pygame
from _common import ColorValue
from utils.user_inputs import UserInputStates

# Classe qui permet de créer les boutons
class Button():
    def __init__(self, x: int, y: int, image: pygame.Surface, clicked_image: pygame.Surface,
                 scale: float, do_place_center: bool = False):
        """Initialise la classe Button

        Args:
            x (int): position en abscisses où le bouton va être créé
            y (int): position en ordonnées où le bouton va être créé
            image (Surface): image qui correspond au bouton
            clicked_image (Surface): image qui va s'afficher quand on clicke sur le bouton
            scale (float): nombre par lequel on multiplie la taille de l'image pour obtenir la taille du bouton
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
        
        self.clickable = True
    
    def set_clickability_state(self, state: bool):
        """Change l'accès au bouton

        Args:
            state (bool): si le bouton est clickable ou non
        """
        self.clickable = state
    
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
        
        if self.clickable:
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

class ActivableUI:
    def __init__(self):
        self.is_off = True
    
    def draw(self, screen: pygame.Surface):
        self.is_off = False
    
    def set_off(self):
        self.is_off = True

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
        
        self.input_states = UserInputStates.get_instance()
        
        
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
        """Met à jour le statut du menu déroulant

        Returns:
            int: index de l'option choisie, -1 si aucune option n'a été choisie
        """
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
        
        # Vérifie si la souris a clické sur une des options du menu déroulant
        if self.input_states.mouse_single_pressed():
            # Si la souris se trouve sur la case principale, le menu doit s'afficher ou arrêter de s'afficher
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            
            # Si le menu est affiché et la souris se trouve sur une des options
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                self.main_option = self.options[self.active_option]
                return self.active_option

        return -1

class InputBox(ActivableUI):
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
        super().__init__()
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
        
        self.input_states = UserInputStates.get_instance()
        self.input_states.add_method_to_be_processed(self.check_status)
        
    def check_status(self, event: pygame.event.Event):
        """Vérifie l'état de l'entrée de texte et la met à jour en fonction de ce que l'utilisateur a fait
        
        Args:
            event (pygame.event.Event): évènement de pygame
        """
        self.clicked = False
        mpos = pygame.mouse.get_pos()
        
        if self.is_off:
            return
        
        if self.input_states.mouse_single_pressed():
            # Si l'utilisateur a cliqué sur l'entrée de texte
            if self.rect.collidepoint(mpos):
                # Fais basculer l'état du l'entrée
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.current_color = self.color_active if self.active else self.color_inactive
        
        # Si l'entrée de texte est active et que l'utilisateur a appuyé sur une touche
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = self.font.render(self.text, True, self.current_color)

    def update(self):
        """Met à jour la taille de l'entrée de texte
        """
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen: pygame.Surface):
        """Affiche l'entrée de texte à l'écran

        Args:
            screen (pygame.Surface): écran sur lequel l'entrée de texte doit être affichée
        """
        super().draw(screen)
        self.update()
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.current_color, self.rect, 2)

class Cursor(ActivableUI):
    def __init__(self, x: int, y: int, width: int, height: int, line_color: ColorValue, cursor_color: ColorValue,
                 min_value: float, max_value: float, do_place_center: bool = False):
        """Crée un curseur qui permet de sélectionner une valeur entre les deux extrémités

        Args:
            x (int): position sur l'axe horizontal
            y (int): position sur l'axe vertical
            width (int): largeur du curseur
            height (int): hauteur du curseur
            line_color (ColorValue): couleur de la ligne sur laquelle le curseur se déplace
            cursor_color (ColorValue): couleur du curseur
            min_value (float): valeur minimale que le curseur peut prendre
            max_value (float): valeur maximale que le curseur peut prendre
            do_place_center (bool, optional): si les coordonnées données sont celles du centre du menu. False par défaut
        """
        super().__init__()
        self.line_color = line_color
        self.cursor_color = cursor_color
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value
        self.dragging = False
        
        self.line_rect = pygame.Rect(x, y, width, height)
        if do_place_center:
            self.line_rect.center = (x, y)

        self.cursor_rect = pygame.Rect(0, 0, width // 15, height * 2)
        
        self.cursor_rect.center = self.line_rect.left, self.line_rect.centery
        
        self.input_states = UserInputStates.get_instance()
        self.input_states.add_method_to_be_processed(self.handle_event)

    def handle_event(self, event: pygame.event.Event):
        """Permet de faire bouger le curseur en fonction de la position de la souris

        Args:
            event (pygame.event.Event): évènement de pygame
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.cursor_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging and not self.is_off:
            self.move(event.pos[0])

    def move(self, mouse_x: int):
        """Fait bouger le curseur

        Args:
            x (int): position de la souris en abscisses
        """
        if mouse_x < self.line_rect.left:
            self.cursor_rect.x = self.line_rect.left
        elif mouse_x > (self.line_rect.right - self.cursor_rect.width):
            self.cursor_rect.x = self.line_rect.right - self.cursor_rect.width
        else:
            self.cursor_rect.x = mouse_x
        
        x_difference = self.cursor_rect.x - self.line_rect.left
        x_ratio = x_difference / (self.line_rect.width - self.cursor_rect.width)
        value_difference = self.max_value - self.min_value
        self.value = self.min_value + x_ratio * value_difference
    
    def set_value(self, value: float):
        """Change la valeur du curseur

        Args:
            value (float): nouvelle valeur du curseur
        """
        if value < self.min_value:
            self.value = self.min_value
        elif value > self.max_value:
            self.value = self.max_value
        else:
            self.value = value
        
        value_difference = self.max_value - self.min_value
        
        self.cursor_rect.x = self.line_rect.left + (self.value - self.min_value) / value_difference * (self.line_rect.width - self.cursor_rect.width)

    def draw(self, screen: pygame.Surface) -> float:
        """Affiche le curseur

        Args:
            screen (pygame.Surface): écran sur lequel le curseur doit être affiché
        
        Returns:
            float: valeur du curseur
        """
        super().draw(screen)
        pygame.draw.rect(screen, self.line_color, self.line_rect)
        pygame.draw.rect(screen, self.cursor_color, self.cursor_rect)
        
        return self.value
