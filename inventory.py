import pygame
from inventorySlot import InventorySlot

class Inventory:
    def __init__(self,player):
        self.slots = []

        self.image = pygame.image.load("images/bg1.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 360)
        self.playerInfo=player

        self.slots.append(InventorySlot("images/coin/coin.png", (10, 360)))

    def update(self):
        """
        Updates slots with player's coin information.
        """
        self.slots[0].count=self.playerInfo.coins

    def render(self, display):
        """
        Render the item on the display surface.

        Parameters:
        - display (pygame.Surface): The surface to render the item on.
        """
        display.blit(self.image, self.rect) 
        for slot in self.slots:
            slot.render(display)