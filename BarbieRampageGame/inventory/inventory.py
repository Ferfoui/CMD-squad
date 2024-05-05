import pygame

class Inventory:
    def __init__(self):
        """Crée un inventaire du joueur
        """
        self.bullets = 0
        self.items = []
        self.selected_item = None
        self.selected_index = 0
    
    def add_item(self, item):
        """Ajoute un item à l'inventaire
        
        Args:
            item (Item): item à ajouter
        """
        self.items.append(item)