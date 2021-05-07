import pygame
from enum import Enum

leJeuTourne = True
Score = 0
dimentions = (1024, 720)
fps = 60
tireParSecondes = 4
peutTirer = True

AFFICHAGE_TIMER_EVENT = pygame.USEREVENT + 0
COLLISION_EVENT = pygame.USEREVENT + 1
DELAY_TIRE_EVENT = pygame.USEREVENT + 2

Fenêtre = None

class NafaireTypes(Enum):
    DEFAULT = 0
    JOUEUR = 1
    ENNEMI = 2
    BALLE = 3
    BALLE_ENNEMI = 4


#personnage joueur
class Nafaire:
    def __init__(self, position=(0,0), animation=None, vie=0, dmg=1, vitesseX=0.05, vitesseY=0.05, rect=None, type=NafaireTypes.DEFAULT):
        self.x , self.y = position
        self.anciennePos = position
        self.animation = animation
        self.vie = vie
        self.dmg = dmg   
        self.vitesseX = vitesseX
        self.vitesseY = vitesseY
        self.type = type
        
        if(animation == None): return
        
        self.rect = self.animation[0].get_rect(center=(self.x, self.y))

    def deplacement(self, x, y):
        self.anciennePos = (self.x, self.y)
        self.x += x * self.vitesseX
        self.y += y * self.vitesseY
        self.rect = self.animation[0].get_rect(center=(self.x, self.y))
        
        self.detectCollisions()

    def detectCollisions(self):

        if(self.x < 0 or self.x > dimentions[0] or self.y < 0 or self.y > dimentions[1]): 
            pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=None))        

        if(self.type == NafaireTypes.JOUEUR):
            
            for enemi in enemies:
                if self.rect.colliderect(enemi.rect): 
                    pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=enemi))

        elif(self.type == NafaireTypes.ENNEMI and self.rect.colliderect(Joueur.rect)): 
            pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=Joueur))

        elif(self.type == NafaireTypes.BALLE):
            
            for enemi in enemies:
                
                if self.rect.colliderect(enemi.rect): 
                    pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=enemi))
                    break

        elif(self.type == NafaireTypes.BALLE_ENNEMI and self.rect.colliderect(Joueur.rect)): 
            pygame.event.post(pygame.event.Event(COLLISION_EVENT, source=self, collision=Joueur))

        


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
    global peutTirer
    peutTirer = False
    balle = Nafaire([Joueur.rect.centerx + 4, Joueur.rect.top - 22], balleImg, type=NafaireTypes.BALLE, vitesseY=8)
    balleList.append(balle)

    pygame.time.set_timer(DELAY_TIRE_EVENT, int(1000/tireParSecondes), True)


#DEBUT DU PROGRAMME
pygame.init()   #initialisation de pygame
pygame.display.set_caption("JEU BIEN")  #titre du jeu
Fenêtre = pygame.display.set_mode(dimentions) # crée la fenêtre et enregiste sa variable

arrièrePlan = Nafaire([0,0], [pygame.image.load("background0.png")])
arrièrePlan.animation[0] = pygame.transform.scale(arrièrePlan.animation[0], dimentions)

Joueur = Nafaire([dimentions[0] / 2, dimentions[1] / 2], [pygame.image.load("quack0.png")], type=NafaireTypes.JOUEUR, vitesseX=0.0125, vitesseY=0.0125)

enemies = list()
enemies.append(Nafaire([dimentions[0] / 2, 5 ], [pygame.image.load("heart.png")], type=NafaireTypes.ENNEMI, vitesseX=4, vitesseY=4))   #cree un ennemi

balleImg = [pygame.image.load("balleJoueur.png")]
balleList = list()
bonus = Nafaire(dmg=0, vitesseX=0)
    
pygame.time.set_timer(AFFICHAGE_TIMER_EVENT, int(1000/fps))

LEFT_CLICK = 1
keysDown = None

while leJeuTourne:

    affiche = False
    ###gestion des evenements:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:# Change la valeur à False pour terminer le while
            leJeuTourne = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            keysDown = pygame.key.get_pressed()
        
        if event.type == pygame.MOUSEBUTTONUP: #tire quand on clique avec la souris
            if (event.button == LEFT_CLICK and peutTirer == True): 
                tire()

        if event.type == AFFICHAGE_TIMER_EVENT:
            affiche = True         

        if event.type == DELAY_TIRE_EVENT:
            peutTirer = True

        if event.type == COLLISION_EVENT:

            if(event.collision == None):#collision avec la 'bordure du cadre'
                
                if(event.source.type == NafaireTypes.JOUEUR or event.source.type == NafaireTypes.ENNEMI):
                    ###corrige la position du joueur ou de l'ennemi pour qu'il ne sorte pas du cadre
                    if event.source.x < 0 : event.source.x = 0
                    if event.source.x > dimentions[0] : event.source.x = dimentions[0]
                    if event.source.y < 0 : event.source.y = 0
                    if event.source.y > dimentions[1] : event.source.y = dimentions[1]

                elif(event.source.type == NafaireTypes.BALLE):
                    ###détruit les balles hors champs
                    balleList.remove(event.source)              
            

            elif(event.source.type == NafaireTypes.BALLE and event.collision.type == NafaireTypes.ENNEMI):#collision balle ennemi
                enemies.remove(event.collision)
                
            elif(event.source.type == NafaireTypes.ENNEMI and event.collision.type == NafaireTypes.JOUEUR) or (event.source.type == NafaireTypes.JOUEUR and event.collision.type == NafaireTypes.ENNEMI):#collision joueur ennemi
                event.source.x, event.source.y = event.source.anciennePos
                event.source.rect = event.source.animation[0].get_rect(center=(event.source.x, event.source.y))

    #key_pressed: 
    if(keysDown != None):
        x = 0
        y = 0
        if keysDown[pygame.K_z]:             
            y -= 1
        if keysDown[pygame.K_s]:
            y += 1
        if keysDown[pygame.K_q]:
            x -= 1
        if keysDown[pygame.K_d]:                
            x += 1
        if(x != 0 or y != 0):
            Joueur.deplacement(x, y)

        if (keysDown[pygame.K_SPACE] and peutTirer == True):
            tire()

    if affiche:

        affiche = False

        if(len(enemies) != 0): 
            enemies[0].deplacement(0, 1)

        for b in balleList:
            b.deplacement(0, -1)

        Affichage()




