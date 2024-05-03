# Codé par la CMD-squad

import pygame, os, sys

from constants import *
from world import World
import utils, menus, interface, weapon

print(f"Bienvenue dans le jeu Barbie Rampage!\nVersion: {GAME_VERSION}\nPar la CMD-squad\n")

# Initialisation du moteur graphique
pygame.init()

# Initiallisation du mixer
pygame.mixer.init()

# Tous les paramètres que le joueur peut modifier comme les touches, etc.
game_settings = utils.Settings()

# Musique du Jeu
pygame.mixer.music.load(PLAYBACK_MUSIC)
pygame.mixer.music.set_volume(game_settings.volume)
pygame.mixer.music.play(loops = -1, start = 0.0, fade_ms = 0)   


# Définition de la taille de l'écran
screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))

# Changement du nom de l'écran vers le nom du jeu
pygame.display.set_caption(f"{GAME_NAME} {GAME_VERSION}")

# Met en place l'horloge
clock = pygame.time.Clock()

# Tous les assets du jeu, c'est-à-dire les images, les sons, les polices, etc...
assets = utils.Assets(game_settings)
# Pour les imputs du joueur
user_inputs_utils = utils.UserInputStates.get_instance()

### Fonctions ###

def timer_minute(time_milisec: int) -> str:
    """Transforme des milisecondes dans le format heures, minutes puis secondes

    Args:
        milisec (int): nombre de milisecondes

    Returns:
        str: temps converti
    """
    sec = time_milisec // 1000
    min = sec // 60
    hour = min // 60
    return f"{hour:02}:{min - hour * 60:02}:{sec - min * 60:02}"

def spawn_player():
    """Fais réapparaître le joueur et réinitialise le monde

    Returns:
        Player: joueur recréé
    """
    death_menu.reset_animation(game_settings.screen_width)
    world.init_data("level0_data.json", assets, game_settings)
    player = world.process_data(assets)
    world.set_debug_display(game_settings.do_draw_hitboxes)
    
    # Création des éléments de l'interface
    player.create_health_bar(10, game_settings.screen_width // 18, assets)
    player.create_kill_counter(10, int(game_settings.screen_width * 5/45), assets)
    player.create_bullet_counter(10, int(game_settings.screen_width * 33/45), assets)
    
    return player


### Initialisation des variables ###

# Création des menus
start_menu = menus.StartMenu(assets, game_settings)
death_menu = menus.DeathMenu(assets, game_settings)
pause_menu = menus.PauseMenu(assets, game_settings)
inventory_menu = menus.InventoryMenu(assets, game_settings)
settings_menu = menus.SettingsMenu(assets, game_settings)
#skilltree_menu = menus.SkillMenu(assets, game_settings)
#weapon_menu = menus.WeaponMenu(assets, game_settings)
#outfit_menu = menus.OutfitMenu(assets, game_settings)
#trophy_menu = menus.TrophyMenu(assets, game_settings)

# Initialisation du monde et du joueur
world = World()

player = spawn_player()

# Debug

# Variables pour la boucle
run = True
game_loading = True
pause = False
settings_choice = False
inventory_choice = False
inventory = False

current_time = pygame.time.get_ticks()

# Boucle qui va permettre de faire tourner le jeu
while run:

    # Fait en sorte que le jeu tourne à un nombre limité de FPS
    clock.tick(FPS)
    
    current_time = pygame.time.get_ticks()
    
    if game_loading:
        game_loading = not start_menu.draw(screen, True)['start']
    else:
        
        # Affiche les éléments à afficher à l'écran
        world.draw(screen)
        player.draw(screen)
        world.update_groups()
        world.draw_sprite_groups(screen)
        
        # Met à jour le joueur
        player.update()
        
        # Affiche les éléments de l'interface
        player.health_bar.draw(screen)
        player.kill_counter.draw(screen)
        player.bullet_counter.draw(screen)
        
        # Gestion de certains menus
        if inventory :
            if settings_choice:
                inventory_buttons = inventory_menu.draw(screen)
                inventory_choice = not inventory_buttons['back']
            else:
                # Gestion du menu pause
                menu_buttons = inventory_menu.draw(screen)
                if menu_buttons['quit'] or settings_menu.do_restart:
                    run = False
                elif menu_buttons['inventory']:
                    settings_choice = True
                elif menu_buttons['back']:
                    pause = False 
        if pause:
            if settings_choice:
                settings_buttons = settings_menu.draw(screen)
                settings_choice = not settings_buttons['back']
                if not settings_choice:
                    settings_menu.set_menu_off()
            else:
                # Gestion du menu pause
                menu_buttons = pause_menu.draw(screen)
                if menu_buttons['quit'] or settings_menu.do_restart:
                    run = False
                elif menu_buttons['settings']:
                    settings_choice = True
                elif menu_buttons['back']:
                    pause = False
        else:
            player.move(world, game_settings)
            
            # Faire bouger les ennemis
            for enemy in world.enemy_group:
                enemy.ai(world)
        
        if not player.is_alive:
            if death_menu.draw(screen, True)['respawn']:
                player = spawn_player()
    
    if game_settings.do_draw_game_time:
        # Afficher le temps actuel à l'écran
        interface.draw_text(screen, "game time: ", assets.default_font, COLOR_DARK, 5, 5, False)
        interface.draw_text(screen, timer_minute(current_time), assets.default_font, COLOR_DARK, 15, 25, False)
    

    for event in pygame.event.get():
        user_inputs_utils.process_events(event)
        
        # Faire quitter la boucle si l'utilisateur quitte le jeu
        if event.type == pygame.QUIT:
            run = False
        
        # Quand des touches sont pressées
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RETURN:
                if game_loading:
                    # Lancer le jeu si la touche 'enter' est pressée
                    game_loading = False
                elif not player.is_alive:
                    # Faire réapparaître le joueur si la touche 'enter' est pressée
                    player = spawn_player()
            if event.key == pygame.K_ESCAPE:
                if (not game_loading) and player.is_alive:
                    if settings_choice:
                        settings_choice = False
                    else:
                        # Activer ou désactiver le menu pause
                        pause = not pause
            if event.key == pygame.K_TAB:
                player.weapon_holder.shoot(world.bullet_group, 1)
                pygame.mixer.Sound.play(assets.weapon_cross_sound)

            if event.key == pygame.K_i:
                if (not game_loading) and player.is_alive:
                    #inventory = not inventory
                    pass
            if event.key == pygame.K_e:
                player.check_collectibles(world)

    # Mise à jour de l'écran à chaque tour de boucle
    pygame.display.update()

# Sauvegarde des paramètres
game_settings.save_settings()
# Fermeture du programme
pygame.quit()

if settings_menu.do_restart:
    # Redémarrer le jeu si l'utilisateur a choisi de redémarrer
    os.execl(sys.executable, sys.executable, *sys.argv)
