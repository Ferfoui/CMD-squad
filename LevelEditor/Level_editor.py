# Codé par la CMD-squad

import pygame
import sys
import csv

# Pour pouvoir importer les fichier se trouvant dans le jeu
sys.path.append("./BarbieRampageGame/")

import Classes as classes
import Constants as consts

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


# Crée une liste vide de tuiles
world_data = []
for row in range(ROWS):
    r = ["air"] * MAX_COLS
    world_data.append(r)

# Crée le sol
for tile in range(0, MAX_COLS):
    # remplace toutes les tuiles les plus basses par de l'herbe
    world_data[ROWS - 1][tile] = "grass_default"

# Création des boutons de sauvegarde et de chargement de niveau
save_img = default_font.render('SAVE', True, consts.COLOR_ORANGE)
load_img = default_font.render('LOAD', True, consts.COLOR_ORANGE)
save_button = classes.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = classes.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
# Crée la liste des boutons à afficher pour selectionner les tuiles
button_dict = {}
button_col = 0
button_row = 0
for tile_name in consts.TILE_TYPES:
	tile_button = classes.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_dict[tile_name], 1)
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

# Fonction qui affiche le monde
def draw_world(screen: pygame.Surface):
    for y, row in enumerate(world_data):
        for x, tile_name in enumerate(row):
            if tile_name in consts.TILE_TYPES:
                screen.blit(img_dict[tile_name], (x * TILE_SIZE - scroll, y * TILE_SIZE))


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
		#save level data
        with open(f'{consts.WORLDS_DATA_LOCATION}level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
    # Charge le monde si l'utilisateur appuie sur le boutons "load"
    if load_button.draw(screen):
        scroll = 0
        with open(f'{consts.WORLDS_DATA_LOCATION}level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = tile
    
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
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = 'air'


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