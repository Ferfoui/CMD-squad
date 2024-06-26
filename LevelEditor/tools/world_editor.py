import pygame, json, os

import constants as consts

# Classe du monde
class World():
    def __init__(self):
        """Initialise la classe qui permet d'éditer le monde
        """
        self.rows = 16
        self.world_size = 150
        self.set_level_name("level0")
        self.new_world()
        
        self.scroll = 0
        self.scroll_speed = 1
    
    def set_level_name(self, level_name: str):
        """Définit le nom du niveau

        Args:
            level_name (str): nom du niveau
        """
        self.level_name = level_name
        self.file_name = f"{self.level_name}_data.json"
    
    def empty(self):
        """Reset le monde
        """
        world = []
        for _ in range(self.world_size):
            r = ["air"] * self.rows
            world.append(r)
        
        self.world_map = world
        
    def new_world(self):
        self.empty()
        
        # Crée le sol
        for column in range(self.world_size):
            # remplace toutes les tuiles les plus basses par de l'herbe
            self.world_map[column][self.rows - 1] = "grass_default"
    
    def load_world(self):
        """charge le monde à partir d'un fichier json
        """
        if self.file_name in os.listdir(consts.WORLDS_DATA_LOCATION):
            # Ouverture du fichier json
            print(f"Chargement du monde {self.file_name}")
            with open(os.path.join(consts.WORLDS_DATA_LOCATION, self.file_name), 'r') as worldfile:
                world_dict = json.load(worldfile)
            
            # Création d'un monde vide de la longueur du niveau à charger
            self.world_size = world_dict['attributes']['level_size']
            # Création d'un monde vide de la longueur du niveau à charger
            self.rows = world_dict['attributes']['level_height']
            
            self.empty()
            
            # Ajout de toutes les tuiles dans le monde
            for tile in world_dict['tiles']:
                if tile['type'] in consts.TILE_TYPES:
                    self.world_map[tile['x']][tile['y']] = tile['type']
        else:
            print(f"Le monde {self.file_name} n'existe pas")
    
    
    def save_world(self):
        """sauvegarde le monde dans un fichier json
        """
        # Dictionnaire qui sera converti en json
        world_dict = {}
        
        # Création d'un dictionnaire pour les attributs du niveau
        world_dict['attributes'] = {}
        
        world_dict['attributes']['level_size'] = self.world_size
        world_dict['attributes']['level_height'] = self.rows
        world_dict['attributes']['background_images'] = ["sky_default"]
        
        # Création d'une liste qui va contenir toutes les tuiles
        world_dict['tiles'] = []

        # Ajout des coordonnées des tuiles et leur type dans la liste
        for x, column in enumerate(self.world_map):
            for y, tile in enumerate(column):
                if tile in consts.TILE_TYPES:
                    tile_dict = {
                        'type': tile,
                        'x': x,
                        'y': y
                        }
                    world_dict['tiles'].append(tile_dict)
        
        # Transformation du dictionnaire en json
        world_json = json.dumps(world_dict, indent=4)
        # Création du fichier json
        with open(os.path.join(consts.WORLDS_DATA_LOCATION, self.file_name), 'w') as outfile:
            outfile.write(world_json)
    
    # Fonction qui affiche le monde
    def draw(self, screen: pygame.Surface, tile_size: int, img_dict: dict[str, pygame.Surface]):
        for x, column in enumerate(self.world_map):
            for y, tile_name in enumerate(column):
                if tile_name in consts.TILE_TYPES:
                    screen.blit(img_dict[tile_name], (x * tile_size - self.scroll, y * tile_size))
    
    def scroll_world(self, direction: int, tile_size: int, screen_width: int):
        """Fait défiler le monde

        Args:
            direction (int): direction du défilement, 1 pour la droite et -1 pour la gauche
        """
        self.scroll += 5 * direction * self.scroll_speed
        
        if self.scroll > self.world_size * tile_size - screen_width:
            self.scroll = self.world_size * tile_size - screen_width
        
        if self.scroll < 0:
            self.scroll = 0
