# Codé par la CMD-squad

import pygame

# Initialisation du moteur graphique
pygame.init

# La taille de l'écran
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# La taille de la marge sur les côtés
LOWER_MARGIN = 100
SIDE_MARGIN = 300

# Définition de la taille de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))

# Changement du nom de l'écran vers le nom du jeu
pygame.display.set_caption("Éditeur de niveaux pour le jeu Barbie Rampage")

# Déclaration des variables de l'éditeur
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# Function qui affiche le background
def draw_background(screen: pygame.Surface):
    screen.blit()

run = True
# Boucle qui va permettre de faire tourner l'éditeur
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Faire quitter la boucle si l'utilisateur quitte le jeu
            run = False
            
pygame.quit