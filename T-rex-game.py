import math, random, sys
import pygame
from pygame.locals import*

# exit the program
def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

# define display surface
W, H = 600, 150
HW, HH= W//2,H//2
AREA = W*H

# initialize display
pygame.init()
CLOCK = pygame.time.Clock()
CANVAS = pygame.display.set_mode((W,H))
pygame.display.set_caption("T-rex")
FPS = 60

# define colors
BLACK = (  0,  0,  0)
WHITE = (255,255,255)

# definir spritesheet
class spritesheet:
    def __init__(self, filename, cols, rows):
        self.sheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw,hh = self.cellCenter = (w/2, h/2)

        self.cells = list([(index % cols * w, int(index / cols) * h, w, h)for index in range(self.totalCellCount)])
        self.handle = list([
            (0,  0), (-hw,   0), (-w,  0),
            (0,-hh), (-hw, -hh), (-w,-hh),
            (0, -h), (-hw,  -h), (-w, -h),])
    def draw(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet,(x + self.handle[handle][0], y + self.handle[handle][1]),self.cells[cellIndex])

# define Trex
class ground:
    def __init__(self,x):
        self.image = pygame.image.load("1x-horizon.png")
        self.x = x
        self.y = H-self.image.get_height()
        self.velocitat = 5
    def actualitza(self):
        if self.x > -1200:
            self.x -= self.velocitat
        else:
            self.x = 1200
    def draw(self):
        CANVAS.blit(self.image,(self.x,self.y))
terra = [ground(0),ground(1200)]        
class rex:
    def __init__(self):
        self.image = spritesheet("1x-trex.png",6,1)
        self.x = 50
        self.y = H
        self.index = 2
        self.count = 0
        self.salta = False
        self.handle = 7
    def actualitza(self):
        if not self.salta:
            self.count += 1
            if self.count < 5:
                self.index = 3
            if self.count >= 5:
                self.index = 2
            if self.count == 10:
                
                self.count = 0
    def draw(self):
        self.image.draw(CANVAS, self.index % self.image.totalCellCount, self.x, self.y, self.handle)

Trex = rex()

# main loop
while True:
    events()

    Trex.actualitza()
    for x in terra:
        x.actualitza()
    
    CANVAS.fill(WHITE)
    Trex.draw()
    for x in terra:
        x.draw()

    pygame.display.update()
    CLOCK.tick(FPS)
