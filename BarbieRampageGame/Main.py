# Codé par la CMD-squad

import pygame
from Constants import *

# Initialisation du moteur graphique
pygame.init

# Définition de la taille de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True
# Boucle qui va permettre de faire tourner le jeu
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quitter la boucle while si l'utilisateur quitte le jeu
            run = False

    # Mise à jour de l'écran à chaques tours de boucle
    pygame.display.update()

# Fermer le programme
pygame.quit()
