import pygame
vec = pygame.math.Vector2

class Ground(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color=None, image=None):
        super().__init__()

        self.size = vec(width, height)
        self.pos = vec(x, y)
        self.rect = pygame.Rect(self.pos, self.size)
        self.rect.topleft = self.pos

        if color is not None:
            self.color = color
            self.image = None
        elif image is not None:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (width, height))
            self.color = None
        


    def render(self, display):
        if self.image is None:
            pygame.draw.rect(display, self.color, self.rect)
        else:
            display.blit(self.image, self.pos)
