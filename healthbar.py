import pygame

health_animations = [pygame.image.load("images/healthbar/ui_heart_empty.png"),
                     pygame.image.load("images/healthbar/ui_heart_half.png"),
                     pygame.image.load("images/healthbar/ui_heart_full.png")]

vec = pygame.math.Vector2

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.health = 6

        self.pos = vec(x, y)
        self.images = self.create_health_bar()

    def create_health_bar(self):
        full_hearts = self.health // 2
        half_heart = self.health % 2
        health_bar = [health_animations[2] for i in range(full_hearts)]
        if half_heart:
            health_bar.append(health_animations[1])
        empty_hearts = (3 - len(health_bar)) * [health_animations[0]]
        return health_bar + empty_hearts

    def render(self, display):
        scale_factor = 2 
        for i, image in enumerate(self.images):
            scaled_image = pygame.transform.scale(image, (image.get_width() * scale_factor, image.get_height() * scale_factor))
            display.blit(scaled_image, self.pos + vec(i * scaled_image.get_width(), 0))

    def takeDamage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.images = self.create_health_bar()

        

    def heal(self, heal):
        self.health += heal
        if self.health > 6:
            self.health = 6
        self.images = self.create_health_bar()
        

        