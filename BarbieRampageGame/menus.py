import pygame, random, os

from constants import *
import interface as gui
import utils

# Classe du menu de démarrage
class StartMenu(gui.Menu):
    def __init__(self, assets: utils.Assets, settings: utils.Settings):
        """Initialise le menu de démarrage

        Args:
            assets (Assets): classe qui contient les assets du jeu
            settings (Settings): classe qui contient les paramètres du jeu
        """
        super().__init__(COLOR_WHITE_AZURE)
        cmd_img = assets.get_image("cmd_img", ASSETS_ROOT + "casadojomojo.png", settings.screen_width // 2)
        # Ajoute l'image au milieu de l'écran
        self.add_image(cmd_img, settings.screen_width // 2, settings.screen_height // 2, True)
        # Ajoute le bouton de démarrage
        self.add_text_button("start", "PRESS ENTER TO START :3", assets.default_font, COLOR_HOT_PINK, settings.screen_width//2, settings.screen_height * 0.96, 1, True)

# Classe du menu pause
class PauseMenu(gui.Menu):
    def __init__(self, assets: utils.Assets, settings: utils.Settings):
        """Initialise le menu de pause

        Args:
            settings (Settings): classe qui contient les paramètres du jeu
        """
        background_color = COLOR_DARK + (128,) # Le '128' correspond à l'opacité de la couleur
        super().__init__(background_color)
        
        self.add_text_button("quit", "quit the game", assets.default_font_bigger, COLOR_WHITE_AZURE, settings.screen_width//2, settings.screen_height * 0.4, 1, True)
        self.add_text_button("settings", "game settings", assets.default_font_bigger, COLOR_WHITE_AZURE, settings.screen_width//2, settings.screen_height * 0.5, 1, True)
        self.add_text_button("back", "back to game", assets.default_font_bigger, COLOR_WHITE_AZURE, settings.screen_width//2, settings.screen_height * 0.6, 1, True)
        
        # Création d'un background à moitié transparent
        self.semi_transparent_background = pygame.Surface((settings.screen_width, settings.screen_height), pygame.SRCALPHA)
        self.semi_transparent_background.fill(self.background_color)
        
    
    def draw(self, screen: pygame.Surface) -> dict[str, bool]:
        """Affiche les images et les boutons à l'écran et renvoie les noms des boutons qui ont été cliqués

        Args:
            screen (pygame.Surface): écran sur lequel le menu doit s'afficher

        Returns:
            dict[str, bool]: noms des boutons avec la valeur true s'ils ont été cliqués
        """
        # Affiche le background à moitié transparent
        screen.blit(self.semi_transparent_background, (0, 0))

        clicked_buttons = super().draw(screen, False)
        
        AROUND_BORDER_SIZE = 15
        border_rect = pygame.Rect(0, 0, screen.get_width()/2, 23 + 2 * AROUND_BORDER_SIZE)
        
        # Affiche une bordure autour de chaque boutons
        for button in self.buttons_to_draw.values():
            
            # Positionnement du rectangle pour la bourdure
            border_rect.center = button.rect.center
            
            pygame.draw.rect(screen, COLOR_HOT_PINK, border_rect, 4, border_radius= 6)
        
        return clicked_buttons

class SettingsMenu(gui.Menu):
    def __init__(self, assets: utils.Assets, settings: utils.Settings):
        """Initialise le menu pause

        Args:
            assets (Assets): classe qui contient les assets du jeu
            settings (Settings): classe qui contient les paramètres du jeu
        """
        super().__init__(COLOR_DARK)
        self.settings = settings
        self.do_restart = False
        self.default_font = assets.default_font
        self.bigger_font = assets.default_font_bigger
        self.initial_resolution = (settings.screen_width, settings.screen_height)
        
        self.set_initial_state(assets, settings)
        
    def set_initial_state(self, assets: utils.Assets, settings: utils.Settings):
        """Remet les paramètres par défaut à l'état initial
        
        Args:
            assets (Assets): classe qui contient les assets du jeu
            settings (Settings): classe qui contient les paramètres du jeu
        """
        self.add_text("resolution :", assets.default_font, COLOR_WHITE_AZURE, settings.screen_width / 4, settings.screen_height / 8, True)
        self.add_drop_down("resolution", settings.screen_width * 5/8, settings.screen_height / 8, [COLOR_WHITE_AZURE, COLOR_GRAY], [COLOR_WHITE_AZURE, COLOR_GRAY], 200, 50, assets.default_font, self.settings.resolution_name, list(RESOLUTION_OPTIONS.keys()), True)
        self.add_text("/!\\ Attention, le jeu doit être redémarré", assets.default_font, COLOR_WHITE_AZURE, settings.screen_width / 2, settings.screen_height * 3/16, do_place_center=True, name='do_restart_line1')
        self.add_text("si cette option est changée", assets.default_font, COLOR_WHITE_AZURE, settings.screen_width / 2, settings.screen_height * 7/32, do_place_center=True, name='do_restart_line2')
        
        self.set_back_button(False)
        
    def draw(self, screen: pygame.Surface) -> dict[str, any]:
        """Affiche le menu pause

        Args:
            screen (pygame.Surface): écran sur lequel le menu doit être affiché

        Returns:
            dict[str, any]: dict[str, any]: dictionnaire avec les noms des gui et la valeur qui leur est assigné. Pour les 'Button' (dict[str, bool]), pour les 'DropDown' (dict[str, str])
        """
        gui_values = super().draw(screen, True)
        self.change_resolution(gui_values["resolution"])
        return gui_values

    def change_resolution(self, resolution_str_value: str):
        """Change la résolution dans les paramètres

        Args:
            resolution_str_value (str): nom de la résolution
        """
        if self.settings.resolution_name != resolution_str_value:
            # Change la résolution
            new_width, new_height = RESOLUTION_OPTIONS[resolution_str_value]
            self.settings.screen_width = new_width
            self.settings.screen_height = new_height
            self.settings.resolution_name = resolution_str_value
            # Change la valeur de la variable qui indique si le jeu doit être redémarré
            self.do_restart = (self.initial_resolution[0] != new_width) or (self.initial_resolution[1] != new_height)
        
        # Change le texte pour indiquer si le jeu doit être redémarré
        if self.do_restart:
            self.add_text("/!\\ Attention, le jeu va être redémarré", self.default_font, COLOR_ORANGE, self.initial_resolution[0] / 2, self.initial_resolution[1] * 3/16, do_place_center=True, name='do_restart_line1')
            self.add_text("pour appliquer les changements", self.default_font, COLOR_ORANGE, self.initial_resolution[0] / 2, self.initial_resolution[1] * 7/32, do_place_center=True, name='do_restart_line2')
        else:
            self.add_text("/!\\ Attention, le jeu doit être redémarré", self.default_font, COLOR_WHITE_AZURE, self.initial_resolution[0] / 2, self.initial_resolution[1] * 3/16, do_place_center=True, name='do_restart_line1')
            self.add_text("si cette option est changée", self.default_font, COLOR_WHITE_AZURE, self.initial_resolution[0] / 2, self.initial_resolution[1] * 7/32, do_place_center=True, name='do_restart_line2')
        
        self.set_back_button(self.do_restart)

    def set_back_button(self, do_restart: bool):
        """Change le bouton de retour pour qu'il redémarre le jeu

        Args:
            do_restart (bool): si le bouton doit redémarrer le jeu
        """
        if do_restart:
            self.add_text_button("back", "restart game", self.bigger_font, COLOR_WHITE_AZURE, self.initial_resolution[0] / 2, self.initial_resolution[1] * 0.9, 1, True)
        else:
            self.add_text_button("back", "back to game", self.bigger_font, COLOR_WHITE_AZURE, self.initial_resolution[0] / 2, self.initial_resolution[1] * 0.9, 1, True)



# Classe du menu de mort et de réapparition
class DeathMenu(gui.Menu):
    def __init__(self, assets: utils.Assets, settings: utils.Settings):
        """Initialise le menu de mort

        Args:
            assets (Assets): classe qui contient les assets du jeu
            settings (Settings): classe qui contient les paramètres du jeu
        """
        super().__init__(COLOR_DARK)
        
        # Valeur du temps pour l'animation
        self.update_time = pygame.time.get_ticks()
        
        self.death_animation = self.load_death_animation(f"{TEXTURES_ROOT}deathscreen/falling/", f"{TEXTURES_ROOT}deathscreen/landing/")
        self.frame_index = 0
        self.barbie_head_rect = self.death_animation['falling'][0].get_rect()
        
        # Intervalle en pourcent pour le positionnement aléatoire de la tête sur l'axe horizontal
        self.RANDOM_RANGE = (20, 70)
        
        self.reset_animation(settings.screen_width)
        
        # L'état actuel de l'animation
        self.head_actual_state = 'falling'
        
        # Ajoute le bouton de respawn
        self.add_text_button('respawn', "PRESS ENTER TO RESPAWN T^T", assets.default_font_bigger, COLOR_HOT_PINK, settings.screen_width//2, settings.screen_height * 0.9, 1, True)
    
    
    def load_death_animation(self, falling_texture_location: str, landing_texture_location: str) -> dict[str, list[pygame.Surface]]:
        """Charge l'animation de la tête qui tombe

        Args:
            falling_texture_location (str): position des textures qui représentent la tête qui tombe
            landing_texture_location (str): position des textures qui représentent la tête qui attérrit

        Returns:
            dict[str, list[pygame.Surface]]: dictionnaire qui contient les listes d'image de l'animation
        """
        animation_dict = {}
        
        scale = 2.5
        
        animation_dict['falling'] = []
		# Compte le nombre d'image qu'il y a dans le dossier
        falling_number_of_frames = len(os.listdir(falling_texture_location))
        for i in range(falling_number_of_frames):
            # Charge l'image dans la mémoire
            img = pygame.image.load(f"{falling_texture_location}{i}.png").convert_alpha()
            # Converti l'image pour qu'elle soit de la taille voulue
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            animation_dict['falling'].append(img)
            
        animation_dict['landing'] = []
        # Compte le nombre d'image qu'il y a dans le dossier
        falling_number_of_frames = len(os.listdir(landing_texture_location))
        for i in range(falling_number_of_frames):
            # Charge l'image dans la mémoire
            img = pygame.image.load(f"{landing_texture_location}{i}.png").convert_alpha()
            # Converti l'image pour qu'elle soit de la taille voulue
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            animation_dict['landing'].append(img)

        return animation_dict

    
    def update_death_animation(self) -> pygame.Surface:
        """Met à jour l'animation de mort (la tête qui tombe)

        Returns:
            pygame.Surface: image à afficher pour l'animation
        """
        
        ANIMATION_COOLDOWN = 50
        
        self.move_barbie_head()
        
        # Met à jour l'image en fonction de la frame actuelle
        image = self.death_animation[self.head_actual_state][self.frame_index]
        
        # Vérifie si assez de temps est passé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Si l'animation est terminée, remise de la première image
        if self.frame_index >= len(self.death_animation[self.head_actual_state]):
            if self.head_actual_state == 'landing':
                self.frame_index = len(self.death_animation[self.head_actual_state]) - 1
            else:
                self.frame_index = 0
        
        return image
    
    
    def move_barbie_head(self):
        """Fais bouger la tête de Barbie en fonction de la gravité et des obstacles
        """
        dy = 0
        
        dy += self.head_vel_y
        
        if self.barbie_head_rect.bottom + dy > self.buttons_to_draw['respawn'].rect.top:
            dy = self.buttons_to_draw['respawn'].rect.top - self.barbie_head_rect.bottom
            self.head_actual_state = 'landing'
            self.head_vel_y = 0
        else:
            self.head_vel_y += GRAVITY

        self.barbie_head_rect.y += dy
        

    def draw(self, screen: pygame.Surface, do_draw_background: bool) -> dict[str, bool]:
        """Affiche les images et les boutons à l'écran, renvoie les noms des boutons qui ont été cliqués et affiche l'animation de la tête de Barbie qui tombe

        Args:
            screen (pygame.Surface): écran sur lequel le menu doit s'afficher
            do_draw_background (bool): si la couleur d'arrière-plan doit être affichée

        Returns:
            dict[str, bool]: noms des boutons avec la valeur true s'ils ont été cliqués
        """
        clicked_buttons = super().draw(screen, do_draw_background)
        
        head_img = self.update_death_animation()
        
        screen.blit(head_img, self.barbie_head_rect)
        
        return clicked_buttons
    
    
    def reset_animation(self, screen_width: int):
        """Remet les paramètres par défaut à l'animation du menu
        
        Args:
            screen_width (int): hauteur de l'écran en pixel
        """
        self.frame_index = 0
        self.head_actual_state = 'falling'
        
        # Vitesse de la tête sur l'axe des abscisses
        self.head_vel_y = 14
        
        # Positionnement de la tête de Barbie avec la position des abscisses aléatoire
        random_postion = random.randint(self.RANDOM_RANGE[0], self.RANDOM_RANGE[1]) / 100
        self.barbie_head_rect.bottomleft = (screen_width * random_postion, 0)
        

#Classe du menu de l'inventaire

class InventoryMenu(gui.Menu):
    # TODO: Régler les problèmes et faire les autres sous-menus
    def __init__(self, assets: utils.Assets, settings: utils.Settings):
        """Initialise le menu de l'inventaire

        Args:
            settings (Settings): classe qui contient les paramètres du jeu
        """
        super().__init__(COLOR_DARK)
        talented_tree_image = assets.get_scaled_image("talented_tree", f"{GUI_TEXTURES_LOCATION}talented_tree.png", 1)
        golden_trophy_image = assets.get_scaled_image("gold_trophy", f"{GUI_TEXTURES_LOCATION}gold_trophy.png", 1)
        manteau_style_image = assets.get_scaled_image("manteau_super_clean", f"{GUI_TEXTURES_LOCATION}manteau_super_clean.png", 1)
        ar_b4rb13_image = assets.get_scaled_image("AR_B4RB13", f"{GUI_TEXTURES_LOCATION}AR_B4RB13.png", 1)

        self.add_button("arbre des talents", talented_tree_image, talented_tree_image, settings.screen_width//1.5, settings.screen_height * 0.1, 1, True)
        self.add_button("trophees", golden_trophy_image, golden_trophy_image, settings.screen_width//1.5, settings.screen_height * 0.1, 1, True)
        self.add_button("apparences", manteau_style_image, manteau_style_image, settings.screen_width//1.5, settings.screen_height * 0.1, 1, True)
        self.add_button("progression des armes", ar_b4rb13_image, ar_b4rb13_image, settings.screen_width//1.5, settings.screen_height * 0.1, 1, True)
    
    def draw(self, screen: pygame.Surface) -> dict[str, bool]:
        """Affiche les images et les boutons à l'écran et renvoie les noms des boutons qui ont été cliqués

        Args:
            screen (pygame.Surface): écran sur lequel le menu doit s'afficher

        Returns:
            dict[str, bool]: noms des boutons avec la valeur true s'ils ont été cliqués
        """
        # Affiche le background à moitié transparent
        screen.blit(self.semi_transparent_background, (0, 0))

        clicked_buttons = super().draw(screen, False)
        
        AROUND_BORDER_SIZE = 15
        border_rect = pygame.Rect(0, 0, screen.get_width()/2, 23 + 2 * AROUND_BORDER_SIZE)
        
        # Affiche une bordure autour de chaque boutons
        for button in self.buttons_to_draw.values():
            
            # Positionnement du rectangle pour la bordure
            border_rect.center = button.rect.center
            
            pygame.draw.rect(screen, COLOR_HOT_PINK, border_rect, 4, border_radius= 6)
        
        return clicked_buttons


   