import pygame
from pygame.locals import *
import sys

from ground import Ground
from player import Player
from enemy import Enemy
from userInterface import UserInterface

pygame.init()

WIDTH = 800
HEIGHT = 400
FPS = 60
CLOCK = pygame.time.Clock()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Venture")

background_back = pygame.image.load("images/country-platform-back.png")
background_back = pygame.transform.scale(background_back, (WIDTH, HEIGHT))

background_forest = pygame.image.load("images/country-platform-forest.png")
background_forest = pygame.transform.scale(background_forest, (WIDTH, HEIGHT))

user_interface = UserInterface()

groundGroup = pygame.sprite.Group()
ground = Ground(900, 120, -20, 360, color=(64,169,134))
ground1 = Ground(100, 20, 200, 230, image="images/Ground.png")
ground2 = Ground(120, 20, 100, 180, image="images/Ground.png")
ground3 = Ground(80, 20, 500, 130, image="images/Ground.png")
groundGroup.add(ground)
groundGroup.add(ground1)
groundGroup.add(ground2)
groundGroup.add(ground3)


player = Player(200, 200)
#player.load_animations()

enemyGroup = pygame.sprite.Group()
enemy_generation = pygame.USEREVENT + 2

itemGroup = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == player.hit_cooldown_event:
            player.hit_cooldown = False
            pygame.time.set_timer(player.hit_cooldown_event, 0)
        if event.type == enemy_generation:
            enemy = Enemy()
            enemyGroup.add(enemy)
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()
            if event.key == K_z:
                player.attacking = True
                player.attack()
            if event.key == K_q:
                pygame.time.set_timer(enemy_generation, 2000)
            if event.key == K_w:
                pygame.time.set_timer(enemy_generation, 0)
        if event.type == KEYUP:
            if event.key == K_SPACE:
                player.jump_cancel()



    # Update functions
    for enemy in enemyGroup:
        enemy.update(groundGroup, player, itemGroup)
    player.update(groundGroup)
    user_interface.update(CLOCK.get_fps())

    # Render
    display.blit(background_back, (0,0))
    display.blit(background_forest, (0,0))

    for ground in groundGroup:
        ground.render(display)

    player.render(display)

    for item in itemGroup:
        item.render(display)
        item.update(player)
    
    for enemy in enemyGroup:
        enemy.render(display)
    
    user_interface.render(display)

    pygame.display.update()
    CLOCK.tick(FPS)


