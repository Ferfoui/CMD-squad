import pygame
import json

from constants import *
import sprites, utils, inventory

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
        self.current_level_index = 0
        self.world_data = []
        self.obstacle_list = []
        self.img_dict = {}
        self.killed = 0
        
        self.player = None
        self.scroll = None
        
        self.load_sprite_groups()
        
        self.display_debug = False
    
    def load_sprite_groups(self):
        """Charge les groupes de sprites

        Args:
            enemy_group (pygame.sprite.Group): groupe d'ennemis
        """
        self.player_group = pygame.sprite.Group()
        
        self.collectible_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
    
    def empty_sprite_groups(self):
        """Vide les groupes de sprites
        """
        self.player_group.empty()

        self.collectible_group.empty()
        self.enemy_group.empty()
        self.bullet_group.empty()
    
    def load_tiles_images(self, tile_size: int):
        """Charge les images des tuiles

        Args:
            tile_size (int): Taille des tuiles
        """
        do_keep_current_images = (len(self.img_dict) == len(TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES)) and (self.img_dict[TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES[0]].get_width() == tile_size)
        
        if do_keep_current_images:
            return
        # Charge toutes les images
        self.img_dict = {}
        for tile_name in TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES:
            img = pygame.image.load(f'{TILES_TEXTURES_LOCATION}{tile_name}.png').convert_alpha()
            img = pygame.transform.scale(img, (tile_size, tile_size * img.get_height() // img.get_width()))
            self.img_dict[tile_name] = img
    
    def first_level(self, assets: utils.Assets, settings: utils.Settings):
        """Charge le premier niveau

        Args:
            assets (Assets): classe qui contient les assets du jeu
            settings (Settings): classe qui contient les paramètres du jeu
        """
        self.current_level_index = 0
        world_file_name = f"{WORLD_LIST[self.current_level_index]}_data.json"
        
        self.init_data(world_file_name, assets, settings)
    
    def restart_level(self, assets: utils.Assets, settings: utils.Settings):
        """Recharge le niveau actuel

        Args:
            assets (Assets): classe qui contient les assets du jeu
            settings (Settings): classe qui contient les paramètres du jeu
        """
        world_file_name = f"{WORLD_LIST[self.current_level_index]}_data.json"
        
        self.init_data(world_file_name, assets, settings)
    
    def go_to_next_level(self, assets: utils.Assets, settings: utils.Settings):
        """Passe au niveau suivant
        
        Args:
            assets (Assets): classe qui contient les assets du jeu
            settings (Settings): classe qui contient les paramètres du jeu
        """
        self.current_level_index += 1
        if self.current_level_index >= len(WORLD_LIST):
            self.current_level_index = 0
            
        world_file_name = f"{WORLD_LIST[self.current_level_index]}_data.json"
        
        self.init_data(world_file_name, assets, settings)
    
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


    def process_data(self, assets: utils.Assets, player_inventory: inventory.Inventory = None) -> sprites.Player:
        """Méthode qui génére le monde en fonction des données données

        Args:
            assets (Assets): classe qui contient les assets du jeu
            inventory (Inventory): inventaire du joueur. S'il n'est pas donné, l'inventaire va être créé
        Returns:
            Player: joueur créé dans le monde
        """
        self.empty_sprite_groups()
        
        self.scroll.bg_scroll = 0
        self.obstacle_list = []
        
        self.level_length = self.world_json['attributes']['level_size']
        self.enemies = 0
        
        if player_inventory == None:
            player_inventory = inventory.Inventory()
            print("Inventory created")
        
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
                        # Si c'est une Ammo box
                        if tile == COLLECTIBLES_TILE_TYPES[0]:
                            box = sprites.AmmoBox(x * self.tile_size, y * self.tile_size, assets, self.tile_size)
                            self.collectible_group.add(box)
                        # Si c'est une Health Box
                        elif tile == COLLECTIBLES_TILE_TYPES[1]:
                            box = sprites.HealthBox(x * self.tile_size, y * self.tile_size, assets, self.tile_size)
                            self.collectible_group.add(box)
                        # Si c'est une Weapon Crate
                        elif tile == COLLECTIBLES_TILE_TYPES[2]:
                            box = sprites.WeaponCrate(x * self.tile_size, y * self.tile_size, assets, self.tile_size)
                            self.collectible_group.add(box)
                        # Si c'est un drapeau de fin de niveau
                        elif tile == COLLECTIBLES_TILE_TYPES[3]:
                            finish_flag = sprites.FinishLevelFlag(x * self.tile_size, y * self.tile_size, assets, self.tile_size)
                            self.collectible_group.add(finish_flag)
                    
                # Si c'est un personnage comme le joueur ou un ennemi
                elif tile in PLAYER_AND_ENEMIES_TILE_TYPES:
                    # Si c'est le point de spawn du joueur
                    if tile == PLAYER_AND_ENEMIES_TILE_TYPES[0]:
                        self.player = sprites.Player(x * self.tile_size, y * self.tile_size, self.tile_size, assets, player_inventory)
                        self.player_group.add(self.player)
                    # Si c'est un dummy
                    elif tile == PLAYER_AND_ENEMIES_TILE_TYPES[1]:
                        dummy = sprites.Dummy(x * self.tile_size, y * self.tile_size, self.tile_size, 2, assets)
                        self.enemy_group.add(dummy)
                        self.enemies += 1
                    elif tile == PLAYER_AND_ENEMIES_TILE_TYPES[2]:
                        ken = sprites.KenEnemy(x * self.tile_size, y * self.tile_size, self.tile_size, 2, assets)
                        self.enemy_group.add(ken)
                        self.enemies += 1
        
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
    
    def draw_sprite_groups(self, screen: pygame.Surface):
        """Méthode qui permet d'afficher les groupes de sprites

        Args:
            screen (Surface): fenêtre sur laquelle le premier plan doit être affiché
        """
        for bullet in self.bullet_group:
            bullet.draw(screen)
        
        for enemy in self.enemy_group:
            enemy.draw(screen)
            
        for collectible in self.collectible_group:
            collectible.draw(screen)

    def update_groups(self):
        """Met à jour les groupes de sprites
        """
        self.bullet_group.update(self)
        self.killed = 0
        for enemy in self.enemy_group :
            enemy.update()
            if not enemy.is_alive:
                self.killed += 1
        self.collectible_group.update(self)
        
    def set_debug_display(self, display: bool):
        """Méthode qui permet d'afficher les hitboxes et les lignes de vision des ennemis

        Args:
            display (bool): affiche les collisions si True
        """
        self.display_debug = display
        
        for enemy in self.enemy_group:
            enemy.display_debug = display
        
        self.player.display_debug = display