import pygame
from inventory import Inventory

class UserInterface:
    def __init__(self, player):
        self.color_red = (255, 0, 0)
        self.color_green = (0, 255, 0)
        self.color_blue = (0, 0, 255)
        self.color_black = (0, 0, 0)
        self.color_white = (255, 255, 255)

        self.smallfont = pygame.font.SysFont("Pixellari", 12)
        self.regularfont = pygame.font.SysFont("Pixellari", 20)
        self.largefont = pygame.font.SysFont("Pixellari", 40)

        self.inventory=Inventory(player)
        self.inventoryRender=True

        self.text = self.regularfont.render("0", True, self.color_black)

    def update(self, fps):
        self.text = self.regularfont.render(str(fps), True, self.color_black)
        self.inventory.update()

    def render(self, display):
        display.blit(self.text, (600, 20))

        if self.inventoryRender==True:
            self.inventory.render(display)

    def toggleInventory(self):
        if self.inventoryRender==True:
            self.inventoryRender=False
        elif self.inventoryRender==False:
            self.inventoryRender=True
