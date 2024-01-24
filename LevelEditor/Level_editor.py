# Codé par la CMD-squad

import pygame
import sys
import json

# Pour pouvoir importer les fichier se trouvant dans le jeu
sys.path.append("./BarbieRampageGame/")

import constants as consts
import utils

# Initialisation du moteur graphique
pygame.init()

clock = pygame.time.Clock()
FPS = 60


# La taille de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# La taille de la marge sur les côtés
LOWER_MARGIN = 100
SIDE_MARGIN = 300


# Définition de la taille de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))

# Changement du nom de l'écran
pygame.display.set_caption("Éditeur de niveaux pour le jeu Barbie Rampage")

# Déclaration des variables de l'éditeur
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
level = 0
current_tile = consts.TILE_TYPES[0]
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# La police utilisée
default_font = pygame.font.Font(consts.PS2P_FONT_LOCATION, 30)

# Conserve les images dans un dictionnaire
img_dict = {}
for tile_name in consts.TILE_TYPES:
    img = pygame.image.load(f'{consts.TILES_TEXTURES_LOCATION}{tile_name}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE * img.get_height() // img.get_width()))
    img_dict[tile_name] = img

# Changement de l'icone
pygame.display.set_icon(img_dict["grass_default"])


# Création des boutons de sauvegarde et de chargement de niveau
save_img = default_font.render('SAVE', True, consts.COLOR_ORANGE)
save_clicked_img = default_font.render('SAVE', True, consts.COLOR_DARK_ORANGE)
load_img = default_font.render('LOAD', True, consts.COLOR_ORANGE)
load_clicked_img = default_font.render('LOAD', True, consts.COLOR_DARK_ORANGE)

save_button = utils.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, save_clicked_img, 1, False)
load_button = utils.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, load_clicked_img, 1, False)
# Crée la liste des boutons à afficher pour selectionner les tuiles
button_dict = {}
button_col = 0
button_row = 0
for tile_name in consts.TILE_TYPES:
	tile_button = utils.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_dict[tile_name], img_dict[tile_name], 1, False)
	button_dict[tile_name] = tile_button
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0

### Fonctions ###

# Function pour afficher du text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function qui affiche le background
def draw_background(screen: pygame.Surface):
    screen.fill(consts.COLOR_DARK)

# Function qui affiche les grilles
def draw_grid(screen: pygame.Surface):
    # Les lignes verticales
	for column in range(MAX_COLS + 1):                   # La coordonnée en haut de la ligne       La coordonnée en bas de la ligne
		pygame.draw.line(screen, consts.COLOR_WHITE_AZURE, (column * TILE_SIZE - scroll, 0), (column * TILE_SIZE - scroll, SCREEN_HEIGHT))
	# Les lignes horizontales
	for row in range(ROWS + 1):
		pygame.draw.line(screen, consts.COLOR_WHITE_AZURE, (0, row * TILE_SIZE), (SCREEN_WIDTH, row * TILE_SIZE))

# Fonction qui donne un monde vide
def empty_world(world_size: int):
    world = []
    for row in range(world_size):
        r = ["air"] * ROWS
        world.append(r)
    
    return world

# Fonction qui affiche le monde
def draw_world(screen: pygame.Surface):
    for x, column in enumerate(world_data):
        for y, tile_name in enumerate(column):
            if tile_name in consts.TILE_TYPES:
                screen.blit(img_dict[tile_name], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# Fonction qui sauvegarde le monde dans un fichier json
def save_world():
    # Dictionnaire qui sera converti en json
    world_dict = {}
    
    # Création d'un dictionnaire pour les attributs du niveau
    world_dict['attributes'] = {}
    
    world_dict['attributes']['level_size'] = MAX_COLS
    world_dict['attributes']['level_height'] = ROWS
    world_dict['attributes']['background_images'] = ["sky_default"]
    
    # Création d'une liste qui va contenir toutes les tuiles
    world_dict['tiles'] = []

    # Ajout des coordonnées des tuiles et leur type dans la liste
    for x, column in enumerate(world_data):
        for y, tile in enumerate(column):
            if tile in consts.TILE_TYPES:
                tile_dict = {
                    'type': tile,
                    'x': x,
                    'y': y
                    }
                world_dict['tiles'].append(tile_dict)
    
    # Transformation du dictionnaire en json
    world_json = json.dumps(world_dict, indent=4)
    # Création du fichier json
    with open(f'{consts.WORLDS_DATA_LOCATION}level{level}_data.json', 'w') as outfile:
        outfile.write(world_json)

# Fonction qui charge le monde à partir d'un fichier json
def load_world():
    # Ouverture du fichier json
    with open(f'{consts.WORLDS_DATA_LOCATION}level{level}_data.json', 'r') as worldfile:
        world_dict = json.load(worldfile)
    
    # Création d'un monde vide de la longueur du niveau à charger
    world = empty_world(world_dict['attributes']['level_size'])
    
    # Ajout de toutes les tuiles dans le monde
    for tile in world_dict['tiles']:
        if tile['type'] in consts.TILE_TYPES:
            world[tile['x']][tile['y']] = tile['type']

    return world

# Crée une liste vide de tuiles
world_data = empty_world(MAX_COLS)

# Crée le sol
for column in range(MAX_COLS):
    # remplace toutes les tuiles les plus basses par de l'herbe
    world_data[column][ROWS - 1] = "grass_default"


run = True
# Boucle qui va permettre de faire tourner l'éditeur
while run:
    
    # Fait en sorte que l'éditeur tourne à un nombre limité de FPS
    clock.tick(FPS)
    
    # Affiche le background
    draw_background(screen)
    
    # Affiche le monde
    draw_world(screen)

    # Affiche les grilles
    draw_grid(screen)
    
    # Affiche le panneau sur lequel il y a les boutons
    pygame.draw.rect(screen, consts.COLOR_GRAY, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    pygame.draw.rect(screen, consts.COLOR_GRAY, (0, SCREEN_HEIGHT - 7, SCREEN_WIDTH + SIDE_MARGIN, int(LOWER_MARGIN * 1.1)))
    
    # Sauvegarde le monde si l'utilisateur appuie sur le boutons "save"
    if save_button.draw(screen):
        save_world()

    # Charge le monde si l'utilisateur appuie sur le boutons "load"
    if load_button.draw(screen):
        scroll = 0
        world_data = load_world()
    
    # Affiche les boutons et vérifie si l'utilisateur a cliqué dessus
    for tile_name, button in button_dict.items():
        if button.draw(screen):
            current_tile = tile_name

    # Encadre en rouge le bouton séléctionné
    pygame.draw.rect(screen, consts.COLOR_RED, button_dict[current_tile].rect, 3)

    # Fais scroller l'écran
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True:
        scroll += 5 * scroll_speed
    
    # Pour que l'utilisateur ne puisse pas scroller plus loin que ce qu'il est autorisé
    if scroll < 0:
        scroll = 0

    # Ajout des nouvelles tuiles à l'écran
    mouse_pos = pygame.mouse.get_pos() # Obtention de la position de la souris
    x = (mouse_pos[0] + scroll) // TILE_SIZE
    y = mouse_pos[1] // TILE_SIZE

    # Vérifie si la souris se trouve dans la zone de la tuile
    if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[1] < SCREEN_HEIGHT:
        # Met à jour la valeur de la tuile
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[x][y] != current_tile:
                world_data[x][y] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[x][y] = 'air'


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Faire quitter la boucle si l'utilisateur quitte le jeu
            run = False
        
        # Quand on appuie sur une touche
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5

        # Quand on arrête d'appuyer sur une touche
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1

    pygame.display.update()
            
pygame.quit