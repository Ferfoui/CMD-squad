###### Les constantes sont définies dans ce fichier ######

# Le nom du jeu
GAME_NAME = "Barbie Rampage"

# La taille de l'écran
SCREEN_WIDTH = 1000 # La largeur
SCREEN_HEIGHT = 800 # La hauteur

# Le nombre d'images par seconde
FPS = 60


# Les couleurs du jeu
COLOR_WHITE_AZURE = (240, 255, 255)
COLOR_GRAY = (60, 64, 64)
COLOR_DARK = (20, 21, 25)
COLOR_RED = (200, 25, 25)
COLOR_ORANGE = (255, 69, 0)

# Les noms des tuiles
TILE_TYPES = ['dirt_default', 'grass_default', 'player_spawn']


### Les images et les sons utilisés (les assets)
ASSETS_ROOT = "BarbieRampageGame/ressources/assets/"
TEXTURES_ROOT = ASSETS_ROOT + "textures/" # Le chemin des textures
SOUNDS_ROOT = ASSETS_ROOT + "sounds/" # Le chemin des effets sonores
FONTS_ROOT = ASSETS_ROOT + "fonts/" # Le chemin vers les polices d'écriture

PLAYER_TEXTURES_LOCATION = TEXTURES_ROOT + "player/"

TILES_TEXTURES_LOCATION = TEXTURES_ROOT + "tiles/"

PS2P_FONT_LOCATION = FONTS_ROOT + "Press_Start_2P/PressStart2P-REGULAR.ttf"


### Les données utilisées (les data)
DATA_ROOT = "BarbieRampageGame/ressources/data/"

WORLDS_DATA_LOCATION = DATA_ROOT + "worlds/"