import pygame

class UserInputStates():
    __instance = None

    @staticmethod
    def get_instance():
        """Méthode pour donner une instance unique de la classe UserImputStates
        """
        if UserInputStates.__instance == None:
            UserInputStates.__instance = UserInputStates()
        return UserInputStates.__instance
    
    def __init__(self):
        """Crée une instance de UserImputStates
        """
        self.RESET_CLICKED_STATE_TIME = 20
        self.update_time = pygame.time.get_ticks()
        self._clicked = False
        self.keydown = False
    
    def process_events(self, event: pygame.event):
        """Gère les évènements de l'utilisateur

        Args:
            event (pygame.event): évènement de pygame
        """
        self.keydown = True if event.type == pygame.KEYDOWN else False
        self.pressed_key = event.key if self.keydown else None
        self.key_unicode = event.unicode if self.keydown else None
        
        if event.type != 1024:
            print(event.type, self.keydown, self.key_unicode, sep=" : ")
    
    def mouse_single_pressed(self) -> bool:
        """Renvoie si la souris a cliqué

        Returns:
            bool: si la souris a cliqué
        """
        # Reset l'update time si la souris a été clickée
        if pygame.mouse.get_pressed()[0]:
            self.update_time = pygame.time.get_ticks()
        
        if pygame.time.get_ticks() - self.update_time > self.RESET_CLICKED_STATE_TIME:
            self._clicked = False
        
        if pygame.mouse.get_pressed()[0] and not self._clicked:
            self._clicked = True
            return True
        
        return False
        