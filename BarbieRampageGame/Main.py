# Codé par la CMD-squad

import pygame
from Constants import *

# Initialisation du moteur graphique
pygame.init

# Définition de la taille de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)

run = True
# Boucle qui va permettre de faire tourner le jeu
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Faire quitter la boucle si l'utilisateur quitte le jeu
            run = False

    # Mise à jour de l'écran à chaque tours de boucle
    pygame.display.update()

# Fermeture le programme
pygame.quit()
