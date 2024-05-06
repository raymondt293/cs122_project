import pygame
from pygame.locals import *
import sys

from ground import Ground
from player import Player
from enemy import Enemy
from userInterface import UserInterface
from levelManager import LevelManager

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

player = Player(200, 200)
user_interface = UserInterface(player)
#player.load_animations()

itemGroup = pygame.sprite.Group()
projectiles=pygame.sprite.Group()

levelManager = LevelManager()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == player.hit_cooldown_event:
            player.hit_cooldown = False
            pygame.time.set_timer(player.hit_cooldown_event, 0)
        if event.type == levelManager.enemy_generation:
            enemy = Enemy()
            levelManager.enemyGroup.add(enemy)
            levelManager.generatedEnemies += 1
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()
            if event.key == K_z:
                player.attacking = True
                player.attack()
            if event.key == K_1:
                levelManager.changeLevel(1)
            if event.key == K_2:
                levelManager.changeLevel(2)
            if event.key == K_3:
                levelManager.changeLevel(3)
            if event.key == K_h:
                user_interface.toggleInventory()
            if event.key == K_f:
                player.fireball(projectiles)
            if event.key == K_c:
                player.useCoin()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                player.jump_cancel()

    # Update functions
    for enemy in levelManager.enemyGroup:
        enemy.update(levelManager.levels[levelManager.getLevel()].groundData, player, projectiles, itemGroup)
    player.update(levelManager.levels[levelManager.getLevel()].groundData)
    user_interface.update(CLOCK.get_fps())

    levelManager.update()

    # Render
    display.blit(background_back, (0,0))
    display.blit(background_forest, (0,0))

    for ground in levelManager.levels[levelManager.getLevel()].groundData:
        ground.render(display)

    player.render(display)

    for item in itemGroup:
        item.render(display)
        item.update(player)
    
    for enemy in levelManager.enemyGroup:
        enemy.render(display)
    
    for projectile in projectiles:
        projectile.render(display)
        projectile.update(levelManager.enemyGroup)
    
    user_interface.render(display)

    pygame.display.update()
    CLOCK.tick(FPS)
