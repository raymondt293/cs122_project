import pygame
import random
import numpy
from item import Item

vec = pygame.math.Vector2

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("images/mob_snail/tile000.png")
        self.rect = self.image.get_rect()

        self.pos = vec(random.randint(0,800),0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.FRIC = -0.1
        self.ACC = round(random.uniform(0.1, 0.2), 2)

        self.direction = random.randint(0, 1) # 0 -> right, 1 -> left

    def move(self):
        self.acc = vec(0, 0.5)

        if self.direction == 0:
            self.acc.x = self.ACC
        elif self.direction == 1:
            self.acc.x = -self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > 780:
            self.direction = 1
        elif self.pos.x < 0:
            self.direction = 0

        self.rect.topleft = self.pos

    def collision(self, group):
        hits = pygame.sprite.spritecollide(self, group, False)

        if self.vel.y > 0:
            if hits:
                hit = hits[0]
                if self.rect.bottom >= hit.rect.top:
                    self.pos.y = hit.rect.top - self.rect.height
                    self.rect.y = hit.rect.top - self.rect.height
                    self.vel.y = 0

    def player_collision(self, player, projectiles, itemGroup):
        if self.rect.colliderect(player.rect):
            player.player_hit(1)    # Player took damage
        elif self.rect.colliderect(player.attack_range) or pygame.sprite.spritecollideany(self,projectiles):
            self.kill()     # Mob hit by user

            probability = numpy.random.uniform(1, 100)
            if probability >= 1 and probability <= 20:
                item = Item(self.pos.x, self.pos.y, "coin", "images/coin/coin_anim_f3.png", scale=3)
                itemGroup.add(item)
            elif probability >= 11 and probability <= 50:
                item = Item(self.pos.x, self.pos.y, "health", "images/healthbar/ui_heart_full.png")
                itemGroup.add(item)
            
    def render(self, display):
        pygame.draw.rect(display, (0,0,255), self.rect)
        display.blit(self.image, self.pos)

    def update(self, groundGroup, player, projectiles, itemGroup):
        self.move()
        self.collision(groundGroup)
        self.player_collision(player, projectiles, itemGroup)
