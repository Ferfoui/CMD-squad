###### Les constantes sont définies dans ce fichier ######

# Le nom du jeu
GAME_NAME = "Barbie Rampage"
GAME_VERSION = "V0.1"

# Le nombre d'images par seconde
FPS = 60

# Les couleurs du jeu
COLOR_WHITE_AZURE = (240, 255, 255)
COLOR_SKY_BLUE = (52, 117, 183)
COLOR_GRAY = (60, 64, 64)
COLOR_LIGHT_GRAY = (120, 128, 128)
COLOR_DARK = (20, 21, 25)
COLOR_RED = (200, 25, 25)
COLOR_ORANGE = (189, 68, 23)
COLOR_DARK_ORANGE = (107, 28, 6)
COLOR_HOT_PINK = (227, 28, 121)
COLOR_HEALTH_PINK = (191, 17, 139)

# Les options pour les settings
RESOLUTION_OPTIONS = {"GRO": (1200, int(1200 * 0.8)), "PA GRO": (1000, 800), "POUTI": (700, 560)}

# Les noms des tuiles
OBSTACLES_TILE_TYPES = ['dirt_default', 'dirt_default_right_border', 'dirt_default_left_border', 'dirt_default_down_border', 'dirt_default_down_left_corner', 'dirt_default_down_right_corner', 'grass_default', 'grass_default_right_border', 'grass_default_left_border', 'sand_default','sand_default_right_border','sand_default_left_border','sand_default_top_border','sand_default_top_left_corner','sand_default_top_right_corner']
ENTITY_TILE_TYPES = []
PLAYER_AND_ENEMIES_TILE_TYPES = ['player_spawn']

TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES = OBSTACLES_TILE_TYPES + ENTITY_TILE_TYPES

TILE_TYPES = TILE_TYPES_WITHOUT_PLAYER_AND_ENEMIES + PLAYER_AND_ENEMIES_TILE_TYPES

# Les constantes in-game
GRAVITY = 0.75

# L'endroit ou se trouve tous les fichiers non python du jeu
RESSOURCES_ROOT = "BarbieRampageGame/resources/"

### Les images et les sons utilisés (les assets)
ASSETS_ROOT = RESSOURCES_ROOT + "assets/"
TEXTURES_ROOT = ASSETS_ROOT + "textures/" # Le chemin des textures
SOUNDS_ROOT = ASSETS_ROOT + "sounds/" # Le chemin des effets sonores
FONTS_ROOT = ASSETS_ROOT + "fonts/" # Le chemin vers les polices d'écriture

PLAYER_TEXTURES_LOCATION = TEXTURES_ROOT + "player/"

TILES_TEXTURES_LOCATION = TEXTURES_ROOT + "tiles/"

BACKGROUND_TEXTURES_LOCATION = TEXTURES_ROOT + "background/"

PS2P_FONT_LOCATION = FONTS_ROOT + "Press_Start_2P/PressStart2P-REGULAR.ttf"


### Les données utilisées (les data)
DATA_ROOT = RESSOURCES_ROOT + "data/"

WORLDS_DATA_LOCATION = DATA_ROOT + "worlds/"


### L'endroit où se trouvera les fichiers de sauvegarde
SAVE_ROOT = "GAMESAVE/"
