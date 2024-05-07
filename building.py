import pygame
vec = pygame.math.Vector2

class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, color=None, image=None):
        '''
        A class representing a building object (or any background object) in a game.

        Parameters:
        - x: the x-coordinate of the top-left corner of the building
        - y: the y-coordinate of the top-left corner of the building
        - color (tuple or None): The color of the building if rendered as a rectangle. None if rendered with an image.
        - image (Surface or None): The image used to represent the building. None if rendered with a color.
        '''
        super().__init__()

        self.pos = vec(x, y)
        self.rect = pygame.Rect(self.pos)
        self.rect.topleft = self.pos

        if color is not None:
            self.color = color
            self.image = None
        elif image is not None:
            self.image = pygame.image.load(image)
            self.color = None

    def render(self, display):
        """
        Render the building on the game display.

        Parameters:
        - display (Surface): The game display surface on which to render the building.
        """
        if self.image is None:
            pygame.draw.rect(display, self.color, self.rect)
        else:
            display.blit(self.image, self.pos)
