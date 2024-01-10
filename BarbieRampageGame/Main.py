# Codé par la CMD-squad

import pygame
import csv
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

# Images
sky_img = pygame.image.load(f"{BACKGROUND_TEXTURES_LOCATION}sky.png").convert_alpha()
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_WIDTH * sky_img.get_height() // sky_img.get_width()))

cmd_img = pygame.image.load(f"{ASSETS_ROOT}casadojomojo.png").convert()
cmd_img = pygame.transform.scale(cmd_img, (SCREEN_WIDTH // 2, (SCREEN_WIDTH // 2) * cmd_img.get_height() // cmd_img.get_width()))

debug_img = pygame.image.load(f"{TEXTURES_ROOT}debug.png").convert_alpha()
debug_img = pygame.transform.scale(debug_img, (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2)))

### Fonctions ###
# Fonction qui affiche le background
def draw_background(screen: pygame.Surface, scroll: Scroll):
    """Fonction qui affiche l'arrière plan

    Args:
        screen (pygame.Surface): écran sur lequel le background doit être affiché
    """
    screen.fill(COLOR_SKY_BLUE)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - scroll.bg_scroll * 0.2, 0))
    
def draw_loading_screen(screen: pygame.Surface):
    """Fonction qui affiche l'image incroyable

    Args:
        screen (pygame.Surface): écran sur lequel l'image doit être affichée
    """
    img_rect = cmd_img.get_rect()
    img_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.fill(COLOR_WHITE_AZURE)
    screen.blit(cmd_img, img_rect)

### Initialisation du monde ###
world_data = []
for row in range(ROWS):
    r = ['air'] * COLS
    world_data.append(r)

# Chargement du monde
with open(f"{WORLDS_DATA_LOCATION}level0_data.csv") as world_file:
    reader = csv.reader(world_file, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = tile

world = World(TILE_SIZE)

scroll = Scroll(TILE_SIZE)

player = world.process_data(world_data, scroll)

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

        player.update()
        player.draw(screen)
        
        player.move(world)
        
        if not player.is_alive:
            screen.blit(debug_img, (0, 0))
        
    
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Faire quitter la boucle si l'utilisateur quitte le jeu
            run = False

    # Mise à jour de l'écran à chaque tours de boucle
    pygame.display.update()

# Fermeture du programme
pygame.quit()
