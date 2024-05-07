import pygame

class InventorySlot:
    def __init__(self, name, pos):
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.count = 0

        self.font = pygame.font.Font("images/Optima.ttc", 25)

    def render(self, display):
        """
        Render the item on the display surface.

        Parameters:
        - display (pygame.Surface): The surface to render the item on.
        """
        text = self.font.render(str(self.count), True, (0, 0, 0))
        display.blit(self.image, self.rect)
        display.blit(text, self.rect.midright)
