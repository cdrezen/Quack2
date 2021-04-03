import pygame
import math

running = True
timer = pygame.time.Clock()
dimentions = (1024, 720)
fps = 16
iFrames = 0
mousePos = [0,0]

class Acteur:
    def __init__(self, animation, framesCount, position = (0,0), angle = 0):
        self.animation = animation
        self.framesCount = framesCount
        self.position = position
        self.angle = angle#useless

     
def draw():
    screen.blit(background.animation[int(iFrames / (fps / background.framesCount))], background.position)
    quackFrame = quack.animation[int(iFrames / (fps / quack.framesCount))]

    screen.blit(quackFrame, quack.position)

    pygame.display.update()


pygame.init()
pygame.display.set_caption("JEU BIEN")
screen = pygame.display.set_mode(dimentions)


background = Acteur([pygame.image.load("background0.png"), pygame.image.load("background1.png")], 2)
quack = Acteur([pygame.image.load("quack0.png"), pygame.image.load("quack1.png")], 2, (dimentions[0] / 2, dimentions[1] / 2))


# main loop
while running:

    timer.tick(1000 / fps)

    #gestion des evenements:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# change the value to False, to exit the main loop
            running = False
        if event.type == pygame.MOUSEMOTION:
            mousePos = list(pygame.mouse.get_pos())
    draw()
    iFrames += 1
    if (iFrames >= fps): iFrames = 0









