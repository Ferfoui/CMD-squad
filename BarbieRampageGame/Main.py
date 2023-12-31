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

### Fonctions ###
# Function qui affiche le background
def draw_background(screen: pygame.Surface, scroll: Scroll):
    """Function qui affiche l'arrière plan

    Args:
        screen (pygame.Surface): écran sur lequel le background doit être affiché
    """
    screen.fill(COLOR_GRAY)
    
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
# Boucle qui va permettre de faire tourner le jeu
while run:

    # Fait en sorte que le jeu tourne à un nombre limité de FPS
    clock.tick(FPS)

    draw_background(screen, scroll)
    
    world.draw(screen)

    player.update()
    player.draw(screen)
    
    player.move(world)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Faire quitter la boucle si l'utilisateur quitte le jeu
            run = False

    # Mise à jour de l'écran à chaque tours de boucle
    pygame.display.update()

# Fermeture le programme
pygame.quit()
