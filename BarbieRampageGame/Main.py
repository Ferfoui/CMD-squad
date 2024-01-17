# Codé par la CMD-squad

import pygame
from Constants import *
from Classes import *

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
# Fonction qui affiche le background
def draw_background(screen: pygame.Surface, scroll: Scroll):
    """Fonction qui affiche l'arrière plan

    Args:
        screen (pygame.Surface): écran sur lequel le background doit être affiché
    """
    screen.fill(COLOR_SKY_BLUE)
    width = assets.sky_img.get_width()
    for x in range(5):
        screen.blit(assets.sky_img, ((x * width) - scroll.bg_scroll * 0.2, 0))
    
def draw_loading_screen(screen: pygame.Surface):
    """Fonction qui affiche l'image incroyable

    Args:
        screen (pygame.Surface): écran sur lequel l'image doit être affichée
    """
    img_rect = assets.cmd_img.get_rect()
    img_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.fill(COLOR_WHITE_AZURE)
    screen.blit(assets.cmd_img, img_rect)

def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, text_col: tuple[int, int, int], x: int, y: int):
    """Fonction qui affiche du texte

    Args:
        screen (pygame.Surface): écran sur lequel le texte doit être affiché
        text (str): texte qui doit être affiché
        font (pygame.font.Font): police à utiliser
        text_col (tuple[int, int, int]): couleur du texte
        x (int): position en abscisses où le texte va être affiché
        y (int): position en ordonnées où le texte va être affiché
    """
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def timer_minute(milisec:int) -> str:
    """Transforme des milisecondes dans le format heures, minutes puis secondes

    Args:
        milisec (int): nombre de milisecondes

    Returns:
        str: temps converti (et pas au christiannisme hein ^^)
    """
    sec = milisec // 1000
    min = sec // 60
    hour = min // 60
    return f"{hour:02}:{min - hour * 60:02}:{sec - min * 60:02}"


scroll = Scroll(TILE_SIZE)

world = World(TILE_SIZE, scroll)

world.init_data("level0_data.json", ROWS)

player = world.process_data()

run = True
game_loading = True
game_loading_timer = 3000 #ms
loading_start_time = pygame.time.get_ticks()
current_time = loading_start_time
# Boucle qui va permettre de faire tourner le jeu
while run:

    # Fait en sorte que le jeu tourne à un nombre limité de FPS
    clock.tick(FPS)
    
    if game_loading:
        draw_loading_screen(screen)
        if current_time - loading_start_time >= game_loading_timer:
            game_loading = False
    else:

        draw_background(screen, scroll)
        
        world.draw(screen)

        # Met à jour le joueur
        player.update()
        
        # Affiche le joueur
        player.draw(screen)
        
        player.move(world)
        
        input_key = pygame.key.get_pressed()
        
        if not player.is_alive:
            screen.blit(assets.debug_img, (0, 0))
            #pour afficher l'écran ptés(nan l'écran de mort bouffon)
            if input_key[pygame.K_r]:
                player.is_alive = True
                #début de piste pour le problème respawn...
        
    
    current_time = pygame.time.get_ticks()

    # Afficher le temps actuel à l'écran
    draw_text(screen, "game time: ", assets.default_font, COLOR_DARK, 5, 5)
    draw_text(screen, timer_minute(current_time), assets.default_font, COLOR_DARK, 15, 25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Faire quitter la boucle si l'utilisateur quitte le jeu
            run = False

    # Mise à jour de l'écran à chaque tours de boucle
    pygame.display.update()

# Fermeture du programme
pygame.quit()
