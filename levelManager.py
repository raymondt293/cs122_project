import pygame
from level import Level
from ground import Ground
from building import Building

class LevelManager:
    def __init__(self):
        self.levels=[]
        self.level=0
        self.generatedEnemies=0
        self.enemyGroup = pygame.sprite.Group()
        self.enemy_generation = pygame.USEREVENT + 2

        #Starting Level 
        L0 = Level()
        L0.addGround(Ground(900, 120, -20, 360, color=(64,169,134)))
        self.levels.append(L0)

        #Level 1
        L1 = Level(5)
        L1.addGround(Ground(900, 120, -20, 360, color=(64,169,134)))
        L1.addGround(Ground(100, 20, 200, 230, image="images/Ground.png"))
        L1.addGround(Ground(120, 20, 100, 180, image="images/Ground.png"))
        L1.addGround(Ground(80, 20, 500, 130, image="images/Ground.png"))
        self.levels.append(L1)

        #Level 2
        L2 = Level(8)
        L2.addGround(Ground(900, 120, -20, 360, color=(64,169,134)))
        L2.addGround(Ground(100, 20, 200, 230, image="images/Ground.png"))
        L2.addGround(Ground(120, 20, 300, 180, image="images/Ground.png"))
        L2.addGround(Ground(80, 20, 400, 130, image="images/Ground.png"))
        self.levels.append(L2)

        #Level 3
        L3 = Level(10)
        L3.addGround(Ground(900, 120, -20, 360, color=(64,169,134)))
        L3.addGround(Ground(100, 20, 100, 200, image="images/Ground.png"))
        L3.addGround(Ground(120, 20, 300, 120, image="images/Ground.png"))
        L3.addGround(Ground(80, 20, 500, 300, image="images/Ground.png"))
        self.levels.append(L3)
    
    def getLevel(self):
        return self.level
    
    def nextLevel(self):
        self.level+=1

    def changeLevel(self, n):
        self.level=n
        self.generatedEnemies=0
        self.enemyGroup.empty()
        pygame.time.set_timer(self.enemy_generation, 2000)
    
    def update(self):
        if(self.generatedEnemies == self.levels[self.getLevel()].enemyCount):
            pygame.time.set_timer(self.enemy_generation, 0)
