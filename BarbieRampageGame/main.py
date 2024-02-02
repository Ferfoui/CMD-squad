 # Codé par la CMD-squad

import pygame

from _common import ColorValue
from constants import *
from world import World
import utils
import menus

# Initialisation du moteur graphique
pygame.init()

# Tous les paramètres que le joueur peut modifier comme les touches, etc...
game_settings = utils.Settings()

# Définition de la taille de l'écran
screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))

# Changement du nom de l'écran vers le nom du jeu
pygame.display.set_caption(f"{GAME_NAME} {GAME_VERSION}")

# Met en place l'horloge
clock = pygame.time.Clock()

# Tous les assets du jeu, c'est à dire les images, les sons, les polices, etc...
assets = utils.Assets(game_settings)

### Fonctions ###

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

def timer_minute(milisec: int) -> str:
    """Transforme des milisecondes dans le format heures, minutes puis secondes

    Args:
        milisec (int): nombre de milisecondes

    Returns:
        str: temps converti (et pas au bouddhisme hein ^^)
    """
    sec = milisec // 1000
    min = sec // 60
    hour = min // 60
    return f"{hour:02}:{min - hour * 60:02}:{sec - min * 60:02}"

def respawn_player():
    """Fais réapparaître le joueur

    Returns:
        Player: joueur recréé
    """
    death_menu.reset_animation(game_settings.screen_width)
    world.init_data("level0_data.json", assets, game_settings)
    return world.process_data()

world = World()

world.init_data("level0_data.json", assets, game_settings)

player = world.process_data()

start_menu = menus.StartMenu(assets, game_settings)
death_menu = menus.DeathMenu(assets, game_settings)
pause_menu = menus.PauseMenu(game_settings)

# Variables pour la boucle
run = True
game_loading = True
pause = False
current_time = pygame.time.get_ticks()

# Boucle qui va permettre de faire tourner le jeu
while run:

    # Fait en sorte que le jeu tourne à un nombre limité de FPS
    clock.tick(FPS)
    
    current_time = pygame.time.get_ticks()
    
    if game_loading:
        game_loading = not ("start" in start_menu.draw(screen, True))
    else:
        
        # Affiche les éléments à afficher à l'écran
        world.draw(screen)
        player.draw(screen)
        
        # Met à jour le joueur
        player.update()
        
        if pause:
            pause_menu.draw(screen)
        else:
            player.move(world, game_settings)
        
        if not player.is_alive:
            if 'respawn' in death_menu.draw(screen, True):
                player = respawn_player()
            

    if game_settings.do_draw_game_time:
        # Afficher le temps actuel à l'écran
        draw_text(screen, "game time: ", assets.default_font, COLOR_DARK, 5, 5, False)
        draw_text(screen, timer_minute(current_time), assets.default_font, COLOR_DARK, 15, 25, False)

    for event in pygame.event.get():
        
        # Faire quitter la boucle si l'utilisateur quitte le jeu
        if event.type == pygame.QUIT:
            run = False
        
        # Quand des touches sont pressées
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_loading:
                    # Lancer le jeu si la touche 'enter' est pressée
                    game_loading = False
                elif not player.is_alive:
                    # Faire réapparaître le joueur si la touche 'enter' est pressée
                    player = respawn_player()
            if event.key == pygame.K_ESCAPE:
                if (not game_loading) and player.is_alive:
                    pause = not pause

    # Mise à jour de l'écran à chaque tours de boucle
    pygame.display.update()

# Sauvegarde des paramètres
game_settings.save_settings()
# Fermeture du programme
pygame.quit()
