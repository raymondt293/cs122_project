import pygame
import random
import numpy
from item import Item
from fireball import Fireball

vec = pygame.math.Vector2

class SecondEnemy(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()

        self.image=None
        self.direction = random.randint(0, 1) # 0 -> right, 1 -> left
        self.projectilesGroup=group

        if self.direction==0:
            self.image = pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle1.png")
            self.direction="RIGHT"
        elif self.direction==1:
            self.image = pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle1.png")
            self.direction="LEFT"

        self.rect = self.image.get_rect()

        self.pos = vec(random.randint(0,800),0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.FRIC = -0.1
        self.ACC = round(random.uniform(0.3, 0.2), 2)
        self.attack_cooldown=300
        self.turn_cooldown=120
    
    # Enemy life
        self.is_alive = True
        self.is_dying = False
        self.death_frame = 0
        self.death_frame_counter = 0

        self.load_animations()

    def move(self):
        self.acc = vec(0, 0.5)

        if self.direction == "RIGHT":
            self.acc.x = self.ACC
        elif self.direction == "LEFT":
            self.acc.x = -self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > 780:
            self.direction = "LEFT"
            self.image = pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle1.png")
        elif self.pos.x < 0:
            self.direction = "RIGHT"
            self.image = pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle1.png")

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
        if self.rect.colliderect(player.attack_range) or pygame.sprite.spritecollideany(self,projectiles):
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
        self.attack()
        self.turn(player)
    
    def attack(self):
        if self.attack_cooldown <= 0:
            fireball=Fireball(self.direction, self.rect.center)
            self.projectilesGroup.add(fireball)
            self.attack_cooldown=300
        else:
            self.attack_cooldown -= 1
    
    def turn(self, player):
        if self.turn_cooldown <= 0:
            if (player.rect.centerx - self.rect.x < 0 and self.direction == "RIGHT"):
                self.direction = "LEFT"
                self.image = pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle1.png")
            elif (player.rect.centerx - self.rect.x > 0 and self.direction == "LEFT"):
                self.direction = "RIGHT"
                self.image = pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle1.png")
            self.turn_cooldown=120
        else:
            self.turn_cooldown -= 1
    
    def render(self, display):
        display.blit(self.image, self.pos)

    def update_death_animation(self):
        if self.death_frame < len(self.animation_dead) - 1:
            self.image = self.animation_dead[self.death_frame]
            self.death_frame_counter += 1
            if self.death_frame_counter >= 10:
                self.death_frame += 1
                self.death_frame_counter = 0
        else:
            self.is_dying = False
            self.is_alive = False
            self.kill()
    
    def load_animations(self):
        self.animation_left = [pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk1.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk2.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk3.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk4.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk5.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk6.png").convert_alpha(),]
        
        self.animation_right = [pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk1.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk2.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk3.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk4.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk5.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Walk/crab-walk6.png").convert_alpha(),]
        
        self.animation_dead = [pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle1.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle2.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle3.png").convert_alpha(),
                               pygame.image.load("images/sprites/Characters/Enemies/sprites/Idle/crab-idle4.png").convert_alpha(),]