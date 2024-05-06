import pygame

class Level:
    def __init__(self, enemyCount=0):
        self.data = []

        self.groundData = pygame.sprite.Group()
        self.enemyData = pygame.sprite.Group()
        self.structureData = pygame.sprite.Group()

        self.enemyCount = enemyCount


    def add(self, data):
        self.data.append(data)

    def addEnemy(self, data):
        self.data.append(data)
        self.enemyData.add(data)

    def addGround(self, data):
        self.data.append(data)
        self.groundData.add(data)

    def addStructure(self, data):
        self.data.append(data)
        self.structureData.add(data)
