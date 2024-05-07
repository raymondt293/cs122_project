import pygame
from inventory import Inventory

class UserInterface:
    def __init__(self, player):
        """
        Initialize the UserInterface object.

        Args:
            player: The player object associated with the user interface.
        """
        self.color_red = (255, 0, 0)
        self.color_green = (0, 255, 0)
        self.color_blue = (0, 0, 255)
        self.color_black = (0, 0, 0)
        self.color_white = (255, 255, 255)

        self.smallfont = pygame.font.SysFont("Pixellari", 12)
        self.regularfont = pygame.font.SysFont("Pixellari", 20)
        self.largefont = pygame.font.SysFont("Pixellari", 40)

        # Inventory object associated with player
        self.inventory=Inventory(player)
        self.inventoryRender=True

        self.text = self.regularfont.render("0", True, self.color_black)

    def update(self, fps):
        """
        Update the user interface.

        Args:
            fps: Frames per second to be displayed.
        """
        self.text = self.regularfont.render(str(fps), True, self.color_black)
        self.inventory.update()

    def render(self, display):
        """
        Render the user interface on the display surface.

        Args:
            display: The display surface to render on.
        """
        display.blit(self.text, (600, 20))

        if self.inventoryRender:
            if self.inventory.playerInfo.is_alive:
                self.inventory.render(display)
            else:
                game_over_text = self.largefont.render("Game Over!", True, self.color_red)
                display.blit(game_over_text, (330, 150))


    def toggleInventory(self):
        """
        Toggle the rendering of the inventory.
        """
        if self.inventoryRender==True:
            self.inventoryRender=False
        elif self.inventoryRender==False:
            self.inventoryRender=True
