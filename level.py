import pygame

class Level:
    def __init__(self, enemyCount=0):
        """
        Initializes a Level object.

        Args:
            enemyCount (int): The initial count of enemies in the level. Default is 0.
        """
        self.data = [] # Add everything here for easy iteration

        self.groundData = pygame.sprite.Group()
        self.enemyData = pygame.sprite.Group()
        self.structureData = pygame.sprite.Group()

        self.enemyCount = enemyCount


    def add(self, data):
        """
        Adds data to the level.

        Args:
            data: Any game element (ground, enemy, structure) to add to the level.
        """
        self.data.append(data)

    def addEnemy(self, data):
        """
        Adds an enemy to the level.

        Args:
            data: Enemy object to add to the level.
        """
        self.data.append(data)
        self.enemyData.add(data)

    def addGround(self, data):
        """
        Adds ground tile(s) to the level.

        Args:
            data: Ground tile object(s) to add to the level.
        """
        self.data.append(data)
        self.groundData.add(data)

    def addStructure(self, data):
        """
        Adds a structure element to the level.

        Args:
            data: Structure object to add to the level.
        """
        self.data.append(data)
        self.structureData.add(data)
