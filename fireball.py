import pygame

class Fireball(pygame.sprite.Sprite):
    def __init__(self, direction, position, image):
        super().__init__()
        self.image=None
        self.direction= direction

        if self.direction=="RIGHT":
            self.image=pygame.image.load(image)
        elif self.direction=="LEFT":
            self.image=pygame.image.load(image)
        
        self.rect=self.image.get_rect(center=position)
    
    def render(self,display):
        """
        Render the item on the display surface.

        Parameters:
        - display (pygame.Surface): The surface to render the item on.
        """
        display.blit(self.image,self.rect)

    def update(self,group):
        """
        Updates the collision and position of the fireball

        Args:
            group: The Sprite group

        """
        hit=pygame.sprite.spritecollideany(self,group)
        if hit:
            self.kill()

        if self.direction=="RIGHT":
            self.rect.move_ip(3,0)
        elif self.direction=="LEFT":
            self.rect.move_ip(-3,0)
