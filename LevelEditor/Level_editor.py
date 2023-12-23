# Codé par la CMD-squad

import pygame

# Initialisation du moteur graphique
pygame.init()

clock = pygame.time.Clock()
FPS = 60


# La taille de l'écran
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# La taille de la marge sur les côtés
LOWER_MARGIN = 100
SIDE_MARGIN = 300

# Les couleurs utilisés
WHITE_AZURE = (240, 255, 255)
DARK = (20, 21, 25)

# Définition de la taille de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))

# Changement du nom de l'écran
pygame.display.set_caption("Éditeur de niveaux pour le jeu Barbie Rampage")

# Changement de l'icone
icon_img = pygame.image.load("LevelEditor/icon.png").convert_alpha()
pygame.display.set_icon(icon_img)

# Déclaration des variables de l'éditeur
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# Function qui affiche le background
def draw_background(screen: pygame.Surface):
    screen.fill(DARK)

# Function qui affiche les grilles
def draw_grid(screen: pygame.Surface):
    return

run = True
# Boucle qui va permettre de faire tourner l'éditeur
while run:
    
    # Fait en sorte que l'éditeur tourne à un nombre limité de FPS
    clock.tick(FPS)
    
    # Affiche le background
    draw_background(screen)
    
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True:
        scroll += 5 * scroll_speed

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