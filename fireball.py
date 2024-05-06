import pygame

class Fireball(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image=None
        self.direction=player.direction

        if self.direction=="RIGHT":
            self.image=pygame.image.load("images/fireball1_R.png")
        elif self.direction=="LEFT":
            self.image=pygame.image.load("images/fireball1_L.png")
        
        self.rect=self.image.get_rect(center=player.rect.center)
    
    def render(self,display):
        display.blit(self.image,self.rect)

    def update(self,group):
        hit=pygame.sprite.spritecollideany(self,group)
        if hit:
            self.kill()

        if self.direction=="RIGHT":
            self.rect.move_ip(3,0)
        elif self.direction=="LEFT":
            self.rect.move_ip(-3,0)
