import pygame

health_animations = [pygame.image.load("images/healthbar/ui_heart_empty.png"),
                     pygame.image.load("images/healthbar/ui_heart_half.png"),
                     pygame.image.load("images/healthbar/ui_heart_full.png")]

vec = pygame.math.Vector2

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        '''
        Initializes a HealthBar object.

        Args:
            x : The x-coordinate of the health bar.
            y : The y-coordinate of the health bar.
        '''
        super().__init__()

        self.health = 6

        self.pos = vec(x, y)
        self.images = self.create_health_bar()

    def create_health_bar(self):
        """
        Creates the health bar images based on the current health value.

        Returns:
            list: List of pygame Surface objects representing the health bar.
        """
        full_hearts = self.health // 2
        half_heart = self.health % 2
        health_bar = [health_animations[2] for i in range(full_hearts)]
        if half_heart:
            health_bar.append(health_animations[1])
        empty_hearts = (3 - len(health_bar)) * [health_animations[0]]
        return health_bar + empty_hearts

    def render(self, display):
        """
        Renders the health bar on the display surface.

        Args:
            display: The pygame display surface.
        """
        scale_factor = 2 
        for i, image in enumerate(self.images):
            scaled_image = pygame.transform.scale(image, (image.get_width() * scale_factor, image.get_height() * scale_factor))
            display.blit(scaled_image, self.pos + vec(i * scaled_image.get_width(), 0))

    def takeDamage(self, damage):
        """
        Reduces the health of the player by the given damage amount.

        Args:
            damage (int): The amount of damage to be inflicted.
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.images = self.create_health_bar()

    def heal(self, heal):
        """
        Increases the health of the player by the given heal amount.

        Args:
            heal (int): The amount of healing to be applied.
        """
        self.health += heal
        if self.health > 6:
            self.health = 6
        self.images = self.create_health_bar()
        

        