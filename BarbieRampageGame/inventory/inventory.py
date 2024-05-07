import pygame
import weapon

class Inventory:
    def __init__(self):
        """Crée un inventaire du joueur
        """
        self.bullets = 0
        self.items = []
        self.selected_item = None
        self.selected_index = 0
        self.unlocked_weapons = {}
        self.current_weapon_index = 0
    
    
    def add_item(self, item):
        """Ajoute un item à l'inventaire
        
        Args:
            item (Item): item à ajouter
        """
        self.items.append(item)
        if True:
            self.unlocked_weapons.append(weapon.Arb4rb13)
        elif item == weapon.GunP450:
            self.unlocked_weapons.append(weapon     )
        
        
        
    def check_weapons_in_items(self, items, Weapons, Player ):
        for item in items:
            if item in self.unlocked_weapons:
                continue
            if isinstance(item, weapon.Weapon):
                self.unlocked_weapons.append(item)
                pass
    
    def swap_weapons(self):
        return
        self.current_weapon_index += 1
        self.current_weapon = self.unlocked_weapons[self.current_weapon_index]