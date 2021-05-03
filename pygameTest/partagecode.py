import pygame
from enum import Enum

leJeuTourne = True
Score = 0
dimentions = (1024, 720)
Fenêtre = None
timer = pygame.time.Clock()
#bonusTime = 50
COLLISION_EVENT = pygame.USEREVENT + 0

class NafaireTypes(Enum):
    DEFAULT = 0
    JOUEUR = 1
    ENNEMI = 2
    BALLE = 3
    BALLE_ENNEMI = 4


#personnage joueur
class Nafaire:
    def __init__(self, position=(0,0), animation=None, vie=0, dmg=1, vitesseX=25, vitesseY=25, rect=None, type=NafaireTypes.DEFAULT, colisionBordure=False):
        self.x , self.y = position
        self.anciennePos = position
        self.animation = animation
        self.vie = vie
        self.dmg = dmg   
        self.vitesseX = vitesseX
        self.vitesseY = vitesseY
        self.type = type
        self.colisionBordure = colisionBordure
        
        if(animation == None): return
        
        self.rect = self.animation[0].get_rect(center=(self.x, self.y))

    def deplacement(self, x, y):
        self.anciennePos = (self.x, self.y)
        self.x += x * self.vitesseX
        self.y += y * self.vitesseY
        self.rect = self.animation[0].get_rect(center=(self.x, self.y))
        
        self.gérerCollisions()

    def gérerCollisions(self):
        
        if(self.type == NafaireTypes.JOUEUR or self.type == NafaireTypes.ENNEMI):
             ###corrige la position du joueur ou de l'ennemi pour qu'il ne sorte pas du cadre
            if self.x < 0 : self.x = 0
            if self.x > dimentions[0] : self.x = dimentions[0]
            if self.y < 0 : self.y = 0
            if self.y > dimentions[1] : self.y = dimentions[1]

            if(self.type == NafaireTypes.JOUEUR):
                for enemi in enemies:
                   if self.rect.colliderect(enemi.rect): 
                       self.x, self.y = self.anciennePos
                       self.rect = self.animation[0].get_rect(center=(self.x, self.y))
                       pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=enemi))
            else:#NafaireTypes.ENNEMI
                if self.rect.colliderect(Joueur.rect): 
                    self.x, self.y = self.anciennePos
                    self.rect = self.animation[0].get_rect(center=(self.x, self.y))
                    pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=Joueur))


        elif(self.type == NafaireTypes.BALLE or self.type == NafaireTypes.BALLE_ENNEMI):
            ###détruit les balles hors champs
            if(self.x < 0 or self.x > dimentions[0] or self.y < 0 or self.y > dimentions[1]): 
                balleList.remove(self);
                return
            if(self.type == NafaireTypes.BALLE):
                for enemi in enemies:
                   if self.rect.colliderect(enemi.rect): 
                       pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=enemi))
                       break
            else:#NafaireTypes.BALLE_ENNEMI
                if self.rect.colliderect(Joueur.rect): pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=Joueur))

        


#affichage contiens ce qui doit etre affiché grace a pygame il es tutiliser a la fin du mainloop pour raffraichir l'affichage  
def Affichage():

    Fenêtre.blit(arrièrePlan.animation[0], (arrièrePlan.x, arrièrePlan.y)) 

    Fenêtre.blit(Joueur.animation[0], Joueur.rect) #dessine le personnage à l'écran

    for enemi in enemies:
        Fenêtre.blit(enemi.animation[0], enemi.rect)

    for b in balleList:
        Fenêtre.blit(b.animation[0], b.rect)

    pygame.display.update()
 

def tire():
    balle = Nafaire([Joueur.rect.centerx + 4, Joueur.rect.top + 22], balleImg, type=NafaireTypes.BALLE)
    balleList.append(balle)

#DEBUT DU PROGRAMME
pygame.init()   #initialisation de pygame
pygame.display.set_caption("JEU BIEN")  #titre du jeu
Fenêtre = pygame.display.set_mode(dimentions) # crée la fenêtre et enregiste sa variable

arrièrePlan = Nafaire([0,0], [pygame.image.load("background0.png")])
arrièrePlan.animation[0] = pygame.transform.scale(arrièrePlan.animation[0], dimentions)

Joueur = Nafaire([dimentions[0] / 2, dimentions[1] / 2], [pygame.image.load("quack0.png")], type=NafaireTypes.JOUEUR, colisionBordure=True)

enemies = list()
enemies.append(Nafaire([dimentions[0] / 2, 5 ], [pygame.image.load("heart.png")], type=NafaireTypes.ENNEMI))   #cree un ennemi

balleImg = [pygame.image.load("balleJoueur.png")]
balleList = list()
bonus = Nafaire(dmg=0, vitesseX=0)
    


LEFT_CLICK = 1
keysDown = None

while leJeuTourne:

    timer.tick(1000/60)

    ###gestion des evenements:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:# Change la valeur à False pour terminer le while
            running = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            keysDown = pygame.key.get_pressed()
        
        if event.type == pygame.MOUSEBUTTONUP: #tire quand on clique avec la souris
            if event.button == LEFT_CLICK: tire()

        if event.type == COLLISION_EVENT:
            print("COLLISION")
            if(event.source.type == NafaireTypes.BALLE):
                enemies.remove(event.collision);
            #if(event.source.type == NafaireTypes.JOUEUR and event.collision.type == NafaireTypes.ENNEMI):
            #    Joueur.x, Joueur.y = Joueur.anciennePos
            #    event.collision.x, event.collision.y = event.collision.anciennePos

            #elif(event.source.type == NafaireTypes.ENNEMI and event.collision.type == NafaireTypes.JOUEUR):
            #    event.collision.x, event.collision.y = event.collision.anciennePos
            #    Joueur.x, Joueur.y = Joueur.anciennePos
            #    print(event.collision.anciennePos)





    #key_pressed: 
    if(keysDown != None):
        if keysDown[pygame.K_z]:             
            Joueur.deplacement(0, -1)
        if keysDown[pygame.K_s]:
            Joueur.deplacement(0, 1)
        if keysDown[pygame.K_q]:
            Joueur.deplacement(-1, 0)
        if keysDown[pygame.K_d]:                
            Joueur.deplacement(1, 0)
        if keysDown[pygame.K_SPACE]:
            tire()

    if(len(enemies) != 0): 
        enemies[0].deplacement(0, 1)

    for b in balleList:
        b.deplacement(0, -1)
    ###

    Affichage()






