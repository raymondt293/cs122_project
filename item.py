import pygame

vec = pygame.math.Vector2

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, itemType, imagePath, scale=1.3):
        '''
        Initialize a new instance of the Item class.

        Parameters:
        - x (int): The x-coordinate of the item's position.
        - y (int): The y-coordinate of the item's position.
        - itemType (str): The type of item.
        - imagePath (str): The file path to the image of the item.
        - scale (float): The scaling factor for the item's image (default is 1.3).
        '''
        super().__init__()

        self.pos = vec(x, y)
        self.itemType = itemType
        self.original_image = pygame.image.load(imagePath).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale), int(self.original_image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self, player):
        """
        Update the item, checking for collision with the player and applying effects accordingly.

        Parameters:
        - player (Player): The player object.
        """
        hits = self.rect.colliderect(player.rect)
        if hits:
            if self.itemType == "health":
                player.healthBar.heal(1)
            elif self.itemType == "coin":
                player.coins+=1
            self.kill()

    def render(self, display):
        """
        Render the item on the display surface.

        Parameters:
        - display (pygame.Surface): The surface to render the item on.
        """
        display.blit(self.image, self.pos)
