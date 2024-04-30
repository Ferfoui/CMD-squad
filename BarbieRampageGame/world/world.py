import pygame
import json

from constants import *
import sprites
import utils

# Classe qui permet de gérer le scrolling de l'écran
class Scroll():
    def __init__(self, tile_size: int):
        """Initialise la class Scroll

        Args:
            tile_size (int): taille des tuiles
        """
        self.reset_thresh(tile_size)
        self.screen_scroll = 0
        self.bg_scroll = 0

    def set_screen_scroll(self, screen_scroll: int):
        self.screen_scroll = screen_scroll
        self.bg_scroll -= screen_scroll
    
    def reset_thresh(self, tile_size: int):
        """Reset la limite de distance entre le joueur et le bord de l'écran

        Args:
            tile_size (int): taille des tuiles
        """
        self.thresh = 6 * tile_size

# Classe qui permet de créer les tuiles
class Tile():
    def __init__(self, image: pygame.Surface, tile_rect: pygame.Rect):
        """Initialise une tuile de niveau

        Args:
            image (pygame.Surface): image de la tuile
            tile_rect (pygame.Rect): rectangle de la tuile
        """
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = tile_rect
        self.initial_x_coordinate = self.rect.x
    
    def scroll_tile(self, background_scroll_value):
        """Positionne la tuile correctement en fonction du défilement global de l'écran

        Args:
            background_scroll_value (float): défilement global de l'écran
        """
        self.rect.x = -background_scroll_value + self.initial_x_coordinate
    
    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher la tuile

        Args:
            screen (Surface): fenêtre sur laquelle le tuile doit être affiché
        """
        screen.blit(self.image, self.rect)

# Classe qui permet de créer des mondes
class World():
    def __init__(self):
        """Initialise la classe World
        """
        self.world_data = []
        self.obstacle_list = []
        
        self.player = None
        self.scroll = None
        
        self.load_sprite_groups()
    
    def load_sprite_groups(self):
        """Charge les groupes de sprites

        Args:
            enemy_group (pygame.sprite.Group): groupe d'ennemis
        """
        self.collectible_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
    
    def empty_sprite_groups(self):
        """Vide les groupes de sprites
        """
        self.collectible_group.empty()
        self.enemy_group.empty()
        self.bullet_group.empty()
    
    def load_tiles_images(self, tile_size):
        # Charge toutes les images
        self.img_dict = {}
        for tile_name in TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES:
            img = pygame.image.load(f'{TILES_TEXTURES_LOCATION}{tile_name}.png').convert_alpha()
            img = pygame.transform.scale(img, (tile_size, tile_size * img.get_height() // img.get_width()))
            self.img_dict[tile_name] = img
    
    def init_data(self, level_name: str, assets: utils.Assets, settings: utils.Settings):
        """Initialise les données du niveau

        Args:
            level_name (str): nom du niveau dans les fichiers
            rows (int): nombre de lignes dans le niveau
            settings (Settings): classe qui contient les paramètres du jeu
        """
        # Reset les data du monde
        self.world_data = []
        
        # Chargement du monde
        
        # Ouverture du fichier json
        with open(WORLDS_DATA_LOCATION + level_name, 'r') as worldfile:
            self.world_json = json.load(worldfile)
        
        # La taille des tuiles en pixel est égale à la taille de l'écran divisée par le nombre de ligne
        self.tile_size = settings.screen_height // self.world_json['attributes']['level_height']
        
        self.load_tiles_images(self.tile_size)
        
        # Initialise le scrolling du niveau
        if self.scroll == None:
            self.scroll = Scroll(self.tile_size)
        else:
            self.scroll.reset_thresh(self.tile_size)
        
        # Récupération des images pour l'arrière-plan
        background_image_names = self.world_json['attributes']['background_images']
        self.background_images = []
        for image_name in background_image_names:
            self.background_images.append(assets.get_image(image_name, f"{BACKGROUND_TEXTURES_LOCATION}{image_name}.png", settings.screen_width, 0))
        
        for col in range(self.world_json['attributes']['level_size']):
            r = ['air'] * self.world_json['attributes']['level_height']
            self.world_data.append(r)
        
        # Ajout de toutes les tuiles dans le monde
        for tile in self.world_json['tiles']:
            self.world_data[tile['x']][tile['y']] = tile['type']


    def process_data(self, assets: utils.Assets) -> sprites.Player:
        """Méthode qui génére le monde en fonction des données données

        Returns:
            Player: joueur créé dans le monde
        """
        self.empty_sprite_groups()
        
        self.scroll.bg_scroll = 0
        self.obstacle_list = []
        
        self.level_length = self.world_json['attributes']['level_size']
        
        for x, column in enumerate(self.world_data):
            for y, tile in enumerate(column):
                # Si c'est un obstacle
                if tile in OBSTACLES_TILE_TYPES:
                    img = self.img_dict[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * self.tile_size
                    img_rect.y = y * self.tile_size
                    if tile in OBSTACLES_TILE_TYPES:
                        tile_data = Tile(img, img_rect)
                        self.obstacle_list.append(tile_data)
                
                elif tile in ENTITY_TILE_TYPES:
                    if tile in COLLECTIBLES_TILE_TYPES:
                        # Si c'est une item box
                        if tile == COLLECTIBLES_TILE_TYPES[0]:
                            box = sprites.ItemBox(x * self.tile_size, y * self.tile_size, assets, self.tile_size)
                            self.collectible_group.add(box)
                    
                # Si c'est un personnage comme le joueur ou un ennemi
                elif tile in PLAYER_AND_ENEMIES_TILE_TYPES:
                    # Si c'est le point de spawn du joueur
                    if tile == PLAYER_AND_ENEMIES_TILE_TYPES[0]:
                        self.player = sprites.Player(x * self.tile_size, y * self.tile_size, self.tile_size, assets)
                    # Si c'est un dummy
                    if tile == PLAYER_AND_ENEMIES_TILE_TYPES[1]:
                        dummy = sprites.IntelligentDummy(x * self.tile_size, y * self.tile_size, self.tile_size, 2, assets, 2)
                        self.enemy_group.add(dummy)
        
        return self.player
    
    def draw(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher le monde

        Args:
            screen (Surface): fenêtre sur laquelle le monde doit être affiché
        """
        self.draw_background(screen)
        
        for tile in self.obstacle_list:
            tile.scroll_tile(self.scroll.bg_scroll)
            tile.draw(screen)
    
    def draw_background(self, screen: pygame.Surface):
        """Fonction qui affiche l'arrière plan

        Args:
            screen (pygame.Surface): écran sur lequel le background doit être affiché
        """
        screen.fill(COLOR_SKY_BLUE)
        width = self.background_images[0].get_width()
        for x in range(5):
            screen.blit(self.background_images[0], ((x * width) - self.scroll.bg_scroll * 0.2, 0))
