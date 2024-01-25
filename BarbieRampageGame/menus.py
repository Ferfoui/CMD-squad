from constants import *
import utils

# Classe du menu de démarrage
class StartMenu(utils.Menu):
    def __init__(self, assets: utils.Assets):
        """Initialise le menu de démarrage

        Args:
            assets (Assets): classe qui contient les assets
        """
        super().__init__(COLOR_WHITE_AZURE)
        
        # Ajoute l'image au milieu de l'écran
        self.add_image(assets.cmd_img, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, True)
        # Ajoute le bouton de démarrage
        self.add_text_button("start", "PRESS ENTER TO START :)", assets.default_font, COLOR_HOT_PINK, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.96, 1, True)

