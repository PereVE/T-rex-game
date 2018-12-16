import math, random, sys
import pygame
from pygame.locals import*


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
sortir = False

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
        self.w = w
        h = self.cellHeight = int(self.rect.height / rows)
        self.h = h
        hw,hh = self.cellCenter = (w/2, h/2)

        self.cells = list([(index % cols * w, int(index / cols) * h, w, h)for index in range(self.totalCellCount)])
        self.handle = list([
            (0,  0), (-hw,   0), (-w,  0),
            (0,-hh), (-hw, -hh), (-w,-hh),
            (0, -h), (-hw,  -h), (-w, -h),])
    def draw(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet,(x + self.handle[handle][0], y + self.handle[handle][1]),self.cells[cellIndex])

# definir classes de imatges que apareixen per pantalla
PossObst = (
    (
        ("1x-obstacle-large.png"),
        (6,1,0),
        (6,1,1),
        (6,1,2),
        (6,1,3),
        (3,1,2),
        (3,1,0),
        (3,1,1)
    ),
    (
        ("1x-obstacle-small.png"),
        (6,1,0),
        (6,1,2),
        (6,1,4),
        (6,1,5),
        (3,1,0),
        (3,1,1),
        (3,1,2)
        )
    )

class counter:
    def __init__(self):
        self.image = spritesheet("1x-text.png",19,2)
        self.count = 0
        self.handle = 0
    def reinicia(self):
        self.count = 0
        self.handle = 0
    def drawnum(self,n,x,y):
        self.image.draw(CANVAS, n % self.image.totalCellCount, x, y, self.handle)
    def actualitza(self):
        self.count += 1
    def draw(self):
        x = W-75
        zeros = 5-len(str(self.count))
        for zero in range(0,zeros):
            self.drawnum(0,x,0)
            x += 15
        for num in str(self.count):
            self.drawnum(int(num),x,0)
            x+=15
contador = counter()
class obstacle:
    def __init__(self):
        self.num = random.randint(0,6)
        self.SmOrLa = random.randint(0,1)
        self.image = spritesheet(PossObst[self.SmOrLa][0],PossObst[self.SmOrLa][self.num+1][0],PossObst[self.SmOrLa][self.num+1][1])
        self.handle = 7
        self.x = W
        self.y = H
        self.velocitat = 5
        self.increment = 0.005
    def reinicia(self):
        self.num = random.randint(0,6)
        self.SmOrLa = random.randint(0,1)
        self.image = spritesheet(PossObst[self.SmOrLa][0],PossObst[self.SmOrLa][self.num+1][0],PossObst[self.SmOrLa][self.num+1][1])
        self.handle = 7
        self.x = W
    def actualitza(self,rex):
        if not((self.y + self.image.h >= rex.y) and (self.x + self.image.w >= rex.x) and (self.x <= rex.x + rex.image.w) and (self.y <= rex.y + rex.image.h)):
            if self.x >= -10:
                self.x -= self.velocitat
                self.velocitat += self.increment
            else:
                self.reinicia()
            return False
        else:
            return True
    def draw(self):
        self.image.draw(CANVAS, PossObst[self.num % 2][self.num+1][2] % self.image.totalCellCount, self.x, self.y, self.handle)
obstacles = obstacle()

class cloud:
    def __init__(self,i):
        self.i = i
        self.image = pygame.image.load("1x-cloud.png")
        self.y = random.randint(10,50)
        self.start_x = random.randint(0,200)
        self.x = self.start_x + 200*self.i
    def reinicia(self):

        self.y = random.randint(10,50)
        self.start_x = random.randint(0,200)
        self.x = self.start_x + 200*self.i
    def actualitza(self):
        if self.x > -200+self.start_x:
            self.x -= 1
        else:
            self.y = random.randint(10,50)
            self.start_x = random.randint(0,200)
            self.x = self.start_x + 600
    def draw(self):
        CANVAS.blit(self.image,(self.x,self.y))
nuvols = [cloud(0), cloud(1), cloud(2), cloud(3)]

class ground:
    def __init__(self,x):
        self.image = pygame.image.load("1x-horizon.png")
        self.x = x
        self.y = H-self.image.get_height()
        self.velocitat = 5
        self.increment = 0.005
    def actualitza(self):
        if self.x > -1200:
            self.x -= self.velocitat
            self.velocitat += self.increment
        else:
            self.x = 1200
    def draw(self) :
        CANVAS.blit(self.image,(self.x,self.y))
terres = [ground(0), ground(1200)]

class rex:
    def __init__(self):
        self.image = spritesheet("1x-trex.png",6,1)
        self.x = 50
        self.y = H
        self.index = 2
        self.const = -math.sqrt(H)
        self.count = 0
        self.salta = False
        self.salt  = -5
        self.handle = 7
    def reinicia(self):
        self.x = 50
        self.y = H
        self.index = 2
        self.const = -math.sqrt(H)
        self.count = 0
        self.salta = False
        self.salt  = -5
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
        else:
            self.index = 0
            self.y = int((self.const)**2)
            self.const += 0.5
            if self.y > H:
                self.y = H
                self.const = -math.sqrt(H)
                self.salta = False
        #print(self.y)
##            self.index = 0
##            if self.y + self.salt > self.image.h and self.salt < 0:
##                self.y += self.salt
##            elif self.y + self.salt <= self.image.h:
##                self.salt = -1*self.salt
##            elif self.y + self.salt < H and self.salt > 0:
##                self.y += self.salt
##            elif self.y + self.salt >= H:
##                self.salta = False
##                self.salt = -1*self.salt
##                self.y = H
                
    def draw(self):
        self.image.draw(CANVAS, self.index % self.image.totalCellCount, self.x, self.y, self.handle)
    def xoc(self):
        self.image.draw(CANVAS, 4 % self.image.totalCellCount, self.x, self.y, self.handle)
Trex = rex()

# main loop
while not sortir:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sortir = True

        if event.type == KEYDOWN and event.key == K_SPACE:
            Trex.salta = True

    
    for terra in terres:
        terra.actualitza()
    contador.actualitza()
    for nuvol in nuvols:
        nuvol.actualitza()
    xoc = obstacles.actualitza(Trex)
    if xoc:
        (spritesheet("1x-text.png",1,2)).draw(CANVAS, 1, HW, HH, 4)
        CANVAS.blit(pygame.image.load("1x-restart.png"),(HW-18,HH+10))
        Trex.xoc()
        pygame.display.update()
    while xoc:
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sortir = True
                xoc = False
            if event.type == KEYDOWN and event.key == K_SPACE:
                xoc = False
                contador.reinicia()
                obstacles.reinicia()
                for nuvol in nuvols:
                    nuvol.reinicia()
                Trex.reinicia()
                for terra in terres:
                    terra.velocitat = 5
                obstacles.velocitat = 5
        
    
    Trex.actualitza()

    
    CANVAS.fill(WHITE)
    for nuvol in nuvols:
        nuvol.draw()
    contador.draw()
    for terra in terres:
        terra.draw()
    Trex.draw()
    obstacles.draw()
    
    
    
    pygame.display.update()
    CLOCK.tick(FPS)

    
pygame.quit()
sys.exit()
