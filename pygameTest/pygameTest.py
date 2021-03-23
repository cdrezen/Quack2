import pygame
import math
import os

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
        self.angle = angle

     
def draw():
    screen.blit(background.animation[int(iFrames / (fps / background.framesCount))], background.position)
    quackFrame = quack.animation[int(iFrames / (fps / quack.framesCount))]
    
    rel_x, rel_y = mousePos[0] - quack.position[0], mousePos[1] - quack.position[1]

    if(abs(rel_x) > 4 or abs(rel_y) > 4):##sensibilité de 4px

        quack.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        print(quack.angle)###
        quack.position = (mousePos[0], mousePos[1])


    quackFrame = pygame.transform.rotate(quackFrame, int(quack.angle - 90))     
    rect = quackFrame.get_rect(center=quack.position)  

    print(rect)###

    screen.blit(quackFrame, rect)

    pygame.display.update()


print(os.getcwd())

pygame.init()
pygame.display.set_caption("QUACK 2.0")
screen = pygame.display.set_mode(dimentions)
logo = pygame.image.load("heart.png")
pygame.display.set_icon(logo)

background = Acteur([pygame.image.load("background0.png"), pygame.image.load("background1.png")], 2)
quack = Acteur([pygame.image.load("quack0.png"), pygame.image.load("quack1.png")], 2, (dimentions[0] / 2, dimentions[1] / 2))


# main loop
while running:

    timer.tick(1000 / fps)
    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# change the value to False, to exit the main loop
            running = False
        if event.type == pygame.MOUSEMOTION:
            mousePos = list(pygame.mouse.get_pos())
    draw()
    iFrames += 1
    if (iFrames >= fps): iFrames = 0
