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
        self.slots[0].count=self.playerInfo.coins

    def render(self, display):
        display.blit(self.image, self.rect) 
        for slot in self.slots:
            slot.render(display)