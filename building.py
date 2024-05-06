import pygame
vec = pygame.math.Vector2

class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, color=None, image=None):
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
        if self.image is None:
            pygame.draw.rect(display, self.color, self.rect)
        else:
            display.blit(self.image, self.pos)
