# Codé par la CMD-squad

import pygame
from Constants import *
from Classes import *

# Initialisation du moteur graphique
pygame.init

# Définition de la taille de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Changement du nom de l'écran vers le nom du jeu
pygame.display.set_caption(GAME_NAME)

# Appel de la classe 'Player' pour créer le Joueur
player = Player(200, 300, 3, 2)

run = True
# Boucle qui va permettre de faire tourner le jeu
while run:

    player.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Faire quitter la boucle si l'utilisateur quitte le jeu
            run = False

        # Quand on appuie sur une touche
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                player.moving_left = True
            if event.key == pygame.K_d:
                player.moving_right = True
        
        # Quand on arrête d'appuyer sur une touche
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                player.moving_left = False
            if event.key == pygame.K_d:
                player.moving_right = False

    # Mise à jour de l'écran à chaque tours de boucle
    pygame.display.update()

# Fermeture le programme
pygame.quit()
