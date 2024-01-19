import pygame
import json

from constants import *
from sprites import Player
import utils

# Classe qui permet de gérer le scrolling de l'écran
class Scroll():
    def __init__(self, tile_size: int):
        """Initialise la class Scroll

        Args:
            tile_size (int): taille des tuiles
        """
        self.THRESH = 200
        self.screen_scroll = 0
        self.bg_scroll = 0
        self.tile_size = tile_size

    def set_screen_scroll(self, screen_scroll: int):
        self.screen_scroll = screen_scroll
        self.bg_scroll -= screen_scroll

# Classe qui permet de créer des mondes
class World():
    def __init__(self, tile_size: int):
        """Initialise la classe World

        Args:
            tile_size (int): longueur des côtés des tuiles
        """
        self.world_data = []
        self.tile_size = tile_size
        self.obstacle_list = []
        self.scroll = Scroll(tile_size)

        # Charge toutes les images
        self.img_dict = {}
        for tile_name in TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES:
            img = pygame.image.load(f'{TILES_TEXTURES_LOCATION}{tile_name}.png').convert_alpha()
            img = pygame.transform.scale(img, (tile_size, tile_size * img.get_height() // img.get_width()))
            self.img_dict[tile_name] = img
    
    def init_data(self, level_name: str, rows: int, assets: utils.Assets):
        """Initialise les données du niveau

        Args:
            level_name (str): nom du niveau dans les fichiers
            rows (int): nombre de lignes dans le niveau
        """
        # Reset les data du monde
        self.world_data = []
        
        # Chargement du monde
        
        # Ouverture du fichier json
        with open(WORLDS_DATA_LOCATION + level_name, 'r') as worldfile:
            self.world_json = json.load(worldfile)
        
        # Récupération des images pour l'arrière-plan
        background_image_names = self.world_json['attributes']['background_images']
        self.background_images = []
        for image_name in background_image_names:
            self.background_images.append(assets.get_image(image_name, f"{BACKGROUND_TEXTURES_LOCATION}{image_name}.png", SCREEN_WIDTH, 0))
        
        for col in range(self.world_json['attributes']['level_size']):
            r = ['air'] * rows
            self.world_data.append(r)
        
        # Ajout de toutes les tuiles dans le monde
        for tile in self.world_json['tiles']:
            self.world_data[tile['x']][tile['y']] = tile['type']
        


    def process_data(self) -> Player:
        """Méthode qui génére le monde en fonction des données données

        Returns:
            Player: joueur créé dans le monde
        """
        self.scroll.bg_scroll = 0
        self.obstacle_list = []
        
        self.level_length = self.world_json['attributes']['level_size']
        
        for x, column in enumerate(self.world_data):
            for y, tile in enumerate(column):
                # Si c'est un objet comme un bloc ou une entité
                if tile in TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES:
                    img = self.img_dict[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * self.tile_size
                    img_rect.y = y * self.tile_size
                    tile_data = (img, img_rect)
                    if tile in OBSTACLES_TILE_TYPES:
                        self.obstacle_list.append(tile_data)
                # Si c'est un personnage comme le joueur ou un ennemi
                elif tile in PLAYER_AND_ENEMIES_TILE_TYPES:
                    # Si c'est le point de spawn du joueur
                    if tile == PLAYER_AND_ENEMIES_TILE_TYPES[0]:
                        player = Player(x * self.tile_size, y * self.tile_size, self.scroll, 5, 2)
        
        return player
    
    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher le monde

        Args:
            screen (Surface): fenêtre sur laquelle le monde doit être affiché
        """
        self.draw_background(screen)
        
        for tile in self.obstacle_list:
            tile[1][0] += self.scroll.screen_scroll
            screen.blit(tile[0], tile[1])
    
    def draw_background(self, screen: pygame.Surface):
        """Fonction qui affiche l'arrière plan

        Args:
            screen (pygame.Surface): écran sur lequel le background doit être affiché
        """
        screen.fill(COLOR_SKY_BLUE)
        width = self.background_images[0].get_width()
        for x in range(5):
            screen.blit(self.background_images[0], ((x * width) - self.scroll.bg_scroll * 0.2, 0))
