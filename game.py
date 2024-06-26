import pygame
from pygame.locals import *
import sys
import random

from ground import Ground
from player import Player
from enemy import Enemy
from secondEnemy import SecondEnemy
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
enemyProjectiles=pygame.sprite.Group()
playerGroup=pygame.sprite.Group()
playerGroup.add(player)

levelManager = LevelManager()

ATTACK_COOLDOWN = 500
last_attack_time = 0

while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == player.hit_cooldown_event:
            player.hit_cooldown = False
            pygame.time.set_timer(player.hit_cooldown_event, 0)
        if event.type == levelManager.enemy_generation:
            if levelManager.level == 1:
                levelManager.enemyGroup.add(Enemy())
                levelManager.generatedEnemies += 1
            elif levelManager.level == 3:
                levelManager.enemyGroup.add(SecondEnemy(enemyProjectiles))
                levelManager.generatedEnemies += 1
            else:
                choice = random.randint(0, 1)
                enemy = None
                if choice == 0:
                    enemy = Enemy()
                elif choice == 1:
                    enemy = SecondEnemy(enemyProjectiles)
                levelManager.enemyGroup.add(enemy)
                levelManager.generatedEnemies += 1  

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()
            if event.key == K_z:
                if current_time - last_attack_time >= ATTACK_COOLDOWN:
                    player.attacking = True
                    player.attack()
                    last_attack_time = current_time
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
    player.update(levelManager.levels[levelManager.getLevel()].groundData, enemyProjectiles)
    user_interface.update(CLOCK.get_fps())

    levelManager.update()

    # Render
    display.blit(background_back, (0,0))
    display.blit(background_forest, (0,0))

    for ground in levelManager.levels[levelManager.getLevel()].groundData:
        ground.render(display)

    if player.is_alive:
        player.render(display)

    for item in itemGroup:
        item.render(display)
        item.update(player)
    
    for enemy in levelManager.enemyGroup:
        enemy.render(display)
    
    for projectile in projectiles:
        projectile.render(display)
        projectile.update(levelManager.enemyGroup)

    for projectile in enemyProjectiles:
        projectile.render(display)
        projectile.update(playerGroup)
    
    user_interface.render(display)

    pygame.display.update()
    CLOCK.tick(FPS)
