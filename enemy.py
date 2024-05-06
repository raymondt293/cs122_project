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

        # Enemy movement
        self.direction = random.randint(0, 1) # 0 -> right, 1 -> left
        self.move_frame = 0
        self.move_counter = 0

        # Enemy life
        self.is_alive = True
        self.is_dying = False
        self.death_frame = 0
        self.death_frame_counter = 0

        self.load_animations()

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
    
    def update_image_frame(self):
        if self.move_frame > 7:
            self.move_frame = 0
            return
        
        if self.vel.x >= 0:
            self.image = self.animation_right[self.move_frame]
        elif self.vel.x < 0:
            self.image = self.animation_left[self.move_frame]
        self.move_counter += 1
        if self.move_counter >= 3:
            self.move_frame = (self.move_frame + 1) % len(self.animation_left)
            self.move_counter = 0

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
        if self.is_dying:
            self.update_death_animation()
        else:
            self.update_image_frame()
            self.move()
            self.collision(groundGroup)
            self.player_collision(player, projectiles, itemGroup)
        

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
        self.animation_left = [pygame.image.load("images/mob_snail_left/tile000.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_left/tile001.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_left/tile002.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_left/tile003.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_left/tile004.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_left/tile005.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_left/tile006.png").convert_alpha(),]
        
        self.animation_right = [pygame.image.load("images/mob_snail_right/tile000.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_right/tile001.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_right/tile002.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_right/tile003.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_right/tile004.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_right/tile005.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_right/tile006.png").convert_alpha(),]
        
        self.animation_dead = [pygame.image.load("images/mob_snail_dead/tile000.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_dead/tile001.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_dead/tile002.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_dead/tile003.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_dead/tile004.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_dead/tile005.png").convert_alpha(),
                               pygame.image.load("images/mob_snail_dead/tile006.png").convert_alpha(),]
