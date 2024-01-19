# Codé par la CMD-squad

import pygame
from constants import *

from world import World
from utils import Assets

# Initialisation du moteur graphique
pygame.init()

# Définition de la taille de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Changement du nom de l'écran vers le nom du jeu
pygame.display.set_caption(GAME_NAME)

# Met en place l'horloge
clock = pygame.time.Clock()

### Variables ###
# Constantes provisoires
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS

# Tous les assets du jeu, c'est à dire les images, les sons, les polices, etc...
assets = Assets()

### Fonctions ###

def draw_death_screen(screen: pygame.Surface):
    """Fonction qui affiche l'écran de mort

    Args:
        screen (pygame.Surface): écran sur lequel l'image doit être affichée
    """
    img_rect = assets.slayed_img.get_rect()
    img_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.fill(COLOR_DARK)
    screen.blit(assets.slayed_img, img_rect)
    draw_text(screen, "PRESS ENTER TO RESPAWN T^T", assets.default_font, COLOR_HOT_PINK, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.96, True)

# Affiche l'écran de chargement
def draw_loading_screen(screen: pygame.Surface):
    """Fonction qui affiche l'image incroyable

    Args:
        screen (pygame.Surface): écran sur lequel l'image doit être affichée
    """
    img_rect = assets.cmd_img.get_rect()
    img_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.fill(COLOR_WHITE_AZURE)
    screen.blit(assets.cmd_img, img_rect)
    draw_text(screen, "PRESS ENTER TO START :3", assets.default_font, COLOR_HOT_PINK, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.96, True)

def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, text_col: tuple[int, int, int], x: int, y: int, do_align_center: bool):
    """Fonction qui affiche du texte

    Args:
        screen (pygame.Surface): écran sur lequel le texte doit être affiché
        text (str): texte qui doit être affiché
        font (pygame.font.Font): police à utiliser
        text_col (tuple[int, int, int]): couleur du texte (racismo no)
        x (int): position en abscisses où le texte va être affiché
        y (int): position en ordonnées où le texte va être affiché
        do_align_center (bool): si les coordonnées données sont celles du centre du texte
    """
    img = font.render(text, True, text_col)
    if do_align_center:
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

world = World(TILE_SIZE)

world.init_data("level0_data.json", ROWS, assets)

player = world.process_data()

# Variables pour la boucle
run = True
game_loading = True
current_time = pygame.time.get_ticks()

# Boucle qui va permettre de faire tourner le jeu
while run:

    # Fait en sorte que le jeu tourne à un nombre limité de FPS
    clock.tick(FPS)
    
    if game_loading:
        draw_loading_screen(screen)
    else:
        world.draw(screen)

        # Met à jour le joueur
        player.update()
        
        # Affiche le joueur
        player.draw(screen)
        
        player.move(world)
        
        input_key = pygame.key.get_pressed()
        
        if not player.is_alive:
            draw_death_screen(screen)
    
    current_time = pygame.time.get_ticks()

    # Afficher le temps actuel à l'écran
    draw_text(screen, "game time: ", assets.default_font, COLOR_DARK, 5, 5, False)
    draw_text(screen, timer_minute(current_time), assets.default_font, COLOR_DARK, 15, 25, False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Faire quitter la boucle si l'utilisateur quitte le jeu
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_loading:
                    game_loading = False

    # Mise à jour de l'écran à chaque tours de boucle
    pygame.display.update()

# Fermeture du programme
pygame.quit()
