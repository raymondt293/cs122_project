import pygame
from pygame.locals import *
from healthbar import HealthBar
from fireball import Fireball

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        '''
        Initialize the Player object.

        Args:
            x (int): Initial x-coordinate of the player.
            y (int): Initial y-coordinate of the player.
        '''
        super().__init__()
        self.image = pygame.image.load("images/player_running_right/tile000.png")
        self.rect = pygame.Rect(x, y, 30, 60)

        # Player information
        self.pos = vec(x, y)
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        self.healthBar = HealthBar(10, 10)
        self.coin=10
        self.maxCoin=100
        self.coins=3
        self.is_alive = True

        # Player constants
        self.ACC = 0.4
        self.FRIC = -0.1

        # Player movements
        self.jumping = False
        self.running = False
        self.direction = "RIGHT"
        self.move_frame = 0
        self.move_counter = 0

        # Player attacking
        self.attacking = False
        self.attack_frame = 0
        self.attack_counter = 0
        self.attack_range = pygame.Rect(0,0,0,0)
        self.hit_cooldown = False

        # Player events
        self.hit_cooldown_event = pygame.USEREVENT + 1

        self.load_animations()

    def move(self):
        """Update player's movement."""
        self.acc = vec(0, 0.5)

        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.acc.x = -self.ACC
        if keys[K_RIGHT]:
            self.acc.x = self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > 800:
            self.pos.x = 0
        elif self.pos.x < -30:
            self.pos.x = 800

        self.rect.topleft = self.pos
        self.rect.x += 30

        if keys[K_LEFT]:
            self.rect.x -= 10
        
        if not self.jumping and not self.running and not self.attacking:
            if self.direction == "RIGHT":
                self.image = pygame.image.load("images/player_idle_right/tile000.png")
            elif self.direction == "LEFT":
                self.image = pygame.image.load("images/player_idle_left/tile000.png")
            self.rect.topleft = (self.pos.x - (self.image.get_rect().width - self.rect.width) / 2 + self.rect.width + 5, self.pos.y - (self.image.get_rect().height - self.rect.height) + 30)

    def walking(self):
        """Update player's walking animation."""
        if self.move_frame > 7:
            self.move_frame = 0
            return
        
        if self.jumping == False and self.running == True:
            if self.vel.x >= 0:
                self.image = self.animation_right[self.move_frame]
                self.direction = "RIGHT"
            elif self.vel.x < 0:
                self.image = self.animation_left[self.move_frame]
                self.direction = "LEFT"
            self.move_counter += 1
            if self.move_counter >= 3:
                self.move_frame += 1
                self.move_counter = 0
        
        if self.running == False and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.animation_right[self.move_frame]
            elif self.direction == "LEFT":
                self.image = self.animation_left[self.move_frame]

    def attack(self):
        """Update player's attack animation."""
        if self.attacking == True:
            if self.direction == "RIGHT":
                self.attack_range = pygame.Rect(self.rect.x + self.rect.width, self.pos.y, 30, self.rect.height)
            elif self.direction == "LEFT":
                self.attack_range = pygame.Rect(self.pos.x, self.pos.y, 30, self.rect.height)

            if self.attack_frame > 7:
                self.attack_frame = 0
                self.attacking = False
                self.attack_range = pygame.Rect(0,0,0,0)
                return
            
            if self.direction == "RIGHT":
                self.image = self.attack_animation_right[self.attack_frame]
            elif self.direction == "LEFT":
                self.image = self.attack_animation_left[self.attack_frame]
            
            self.attack_counter += 1
            if self.attack_counter >= 2:
                self.attack_frame += 1
                self.attack_counter = 0

    def collision(self, group):
        """Handle collision with group and ground."""
        hits = pygame.sprite.spritecollide(self, group, False)

        if self.vel.y > 0:
            if hits:
                hit = hits[0]
                if self.rect.bottom < hit.rect.bottom:
                    self.pos.y = hit.rect.top - self.rect.height
                    self.rect.y = hit.rect.top - self.rect.height
                    self.vel.y = 0
                    self.jumping = False

    def update(self, group, enProjectiles):
        """Update player's position and interactions."""
        if(self.healthBar.health <= 0):
            self.is_alive = False
            self.healthBar.health = 0
            self.kill()
            print('player is dead')
        else:
            self.attack()
            self.walking()
            self.move()
            self.collision(group)
            self.checkProjectiles(enProjectiles)

    def checkProjectiles(self, group):
        """Check for collisions with enemy projectiles."""
        hits = pygame.sprite.spritecollideany(self, group)

        if hits:
            self.player_hit(1)

    def jump(self):
        """Make the player jump."""
        if self.jumping == False:
            self.jumping = True
            self.vel.y = -12

    def jump_cancel(self):
        """Cancel player's jump."""
        if self.jumping:
            if self.vel.y < -3: # Player is mid way through his jump
                self.vel.y = -3

    def render(self, display):
        """Render the player on the display surface."""
        display.blit(self.image, self.pos)
        pygame.draw.rect(display, (255, 102, 51), pygame.Rect(self.pos.x, self.rect.y - 30, 100*(self.coin/self.maxCoin), 8))
        self.healthBar.render(display)

    def load_animations(self):
        """Load player's animations."""
        self.animation_right = [pygame.image.load("images/player_running_right/tile000.png").convert_alpha(),
                   pygame.image.load("images/player_running_right/tile001.png").convert_alpha(),
                   pygame.image.load("images/player_running_right/tile002.png").convert_alpha(),
                   pygame.image.load("images/player_running_right/tile003.png").convert_alpha(),
                   pygame.image.load("images/player_running_right/tile004.png").convert_alpha(),
                   pygame.image.load("images/player_running_right/tile005.png").convert_alpha(),
                   pygame.image.load("images/player_running_right/tile006.png").convert_alpha(),
                   pygame.image.load("images/player_running_right/tile007.png").convert_alpha()]

        self.animation_left = [pygame.image.load("images/player_running_left/tile000.png").convert_alpha(),
                   pygame.image.load("images/player_running_left/tile001.png").convert_alpha(),
                   pygame.image.load("images/player_running_left/tile002.png").convert_alpha(),
                   pygame.image.load("images/player_running_left/tile003.png").convert_alpha(),
                   pygame.image.load("images/player_running_left/tile004.png").convert_alpha(),
                   pygame.image.load("images/player_running_left/tile005.png").convert_alpha(),
                   pygame.image.load("images/player_running_left/tile006.png").convert_alpha(),
                   pygame.image.load("images/player_running_left/tile007.png").convert_alpha()]

        self.attack_animation_right = [pygame.image.load("images/player_attack_right/tile000.png").convert_alpha(),
                          pygame.image.load("images/player_attack_right/tile001.png").convert_alpha(),
                          pygame.image.load("images/player_attack_right/tile002.png").convert_alpha(),
                          pygame.image.load("images/player_attack_right/tile003.png").convert_alpha(),
                          pygame.image.load("images/player_attack_right/tile004.png").convert_alpha(),
                          pygame.image.load("images/player_attack_right/tile005.png").convert_alpha(),
                          pygame.image.load("images/player_attack_right/tile006.png").convert_alpha(),
                          pygame.image.load("images/player_attack_right/tile007.png").convert_alpha()]

        self.attack_animation_left = [pygame.image.load("images/player_attack_left/tile000.png").convert_alpha(),
                          pygame.image.load("images/player_attack_left/tile001.png").convert_alpha(),
                          pygame.image.load("images/player_attack_left/tile002.png").convert_alpha(),
                          pygame.image.load("images/player_attack_left/tile003.png").convert_alpha(),
                          pygame.image.load("images/player_attack_left/tile004.png").convert_alpha(),
                          pygame.image.load("images/player_attack_left/tile005.png").convert_alpha(),
                          pygame.image.load("images/player_attack_left/tile006.png").convert_alpha(),
                          pygame.image.load("images/player_attack_left/tile007.png").convert_alpha()]
        self.idle_animation_left = [pygame.image.load("images/player_idle_left/tile000.png").convert_alpha(),
                          pygame.image.load("images/player_idle_left/tile001.png").convert_alpha(),
                          pygame.image.load("images/player_idle_left/tile002.png").convert_alpha(),
                          pygame.image.load("images/player_idle_left/tile003.png").convert_alpha()]
        
        self.idle_animation_right = [pygame.image.load("images/player_idle_right/tile000.png").convert_alpha(),
                          pygame.image.load("images/player_idle_right/tile001.png").convert_alpha(),
                          pygame.image.load("images/player_idle_right/tile002.png").convert_alpha(),
                          pygame.image.load("images/player_idle_right/tile003.png").convert_alpha()]
        
    def player_hit(self, damage):
        """Handle player's hit."""
        if self.hit_cooldown == False:
            self.hit_cooldown = True
            self.healthBar.takeDamage(damage)
            pygame.time.set_timer(self.hit_cooldown_event, 1000)
    
    def fireball(self,group):
        """Launch a fireball."""
        if self.coin >=10:
            if self.direction == "RIGHT":
                fireball=Fireball(self.direction, self.rect.center, "images/fireball2_R.png")
                group.add(fireball)
            elif self.direction == "LEFT":
                fireball=Fireball(self.direction, self.rect.center, "images/fireball2_L.png")
                group.add(fireball)
            self.coin -= 10
    
    def useCoin(self):
        """Use coins."""
        if self.coin == self.maxCoin:
           return
        if self.coins >= 2:
            self.coins -= 2
            if self.coin+50 > self.maxCoin:
                self.coin=self.maxCoin
            else:
                self.coin+=50
