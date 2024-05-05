import pygame

vec = pygame.math.Vector2

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, itemType, imagePath, scale=1.3):
        super().__init__()

        self.pos = vec(x, y)
        self.itemType = itemType
        self.original_image = pygame.image.load(imagePath).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale), int(self.original_image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self, player):
        hits = self.rect.colliderect(player.rect)
        if hits:
            if self.itemType == "health":
                player.healthBar.heal(1)
            elif self.itemType == "coin":
                pass
            self.kill()

    def render(self, display):
        display.blit(self.image, self.pos)