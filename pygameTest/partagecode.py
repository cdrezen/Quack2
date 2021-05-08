import pygame
from enum import Enum

leJeuTourne = True
score = 0
dimentions = (1024, 720)
fps = 60
tireParSecondes = 4
peutTirer = True
delaiSpawn = 100

AFFICHAGE_TIMER_EVENT = pygame.USEREVENT + 0
COLLISION_EVENT = pygame.USEREVENT + 1
DELAY_TIRE_EVENT = pygame.USEREVENT + 2
SPAWN_TIMER_EVENT = pygame.USEREVENT + 3

Fenêtre = None

class dim:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

        
class N2(Nafaire):
    def __init__(self, position=(...), animation=None, vie=0, dmg=1, vitesseX=0.05, vitesseY=0.05, rect=None, type=NafaireTypes.DEFAULT, dimX=0):
        self.dimX = dimX
#affichage contiens ce qui doit etre affiché grace a pygame il es tutiliser a la fin du mainloop pour raffraichir l'affichage  
def Affichage():

    Fenêtre.blit(arrièrePlan.animation[0], (0,0))
    
    Fenêtre.blit(Joueur.animation[0], Joueur.rect) #dessine le personnage à l'écran

    for enemi in enemies:
        Fenêtre.blit(enemi.animation[0], enemi.rect)

    for b in balleList:
        Fenêtre.blit(b.animation[0], b.rect)
    
    img = score_im.render('{}'.format(str(score)), True , (255,255,255))
    rect_score_img = score_img.get_rect()
    Fenêtre.blit(score_img, (0,0))
    Fenêtre.blit(img, rect_score_img.center)

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

Joueur = Nafaire([dimentions[0] / 2, dimentions[1] / 2], [pygame.image.load("quack0.png")], type=NafaireTypes.JOUEUR, vitesseX=5, vitesseY=5)

enemies = list()
enemies.append(Nafaire([dimentions[0] / 2, 5 ], [pygame.image.load("heart.png")], type=NafaireTypes.ENNEMI, vitesseX=4, vitesseY=4))   #cree un ennemi

balleImg = [pygame.image.load("balleJoueur.png")]
balleList = list()
bonus = Nafaire(dmg=0, vitesseX=0)

#rajout score
score_img = pygame.image.load("score_espace.jpg").convert() #c'est le cadre du score
score_img = pygame.transform.smoothscale(score_img,(100,45))
score_im = pygame.font.SysFont(None , 30)
img = score_im.render('{}'.format(str(score)), True , (255,255,255))
#rajout score

pygame.time.set_timer(AFFICHAGE_TIMER_EVENT, int(1000/fps))
pygame.time.set_timer(SPAWN_TIMER_EVENT, delaiSpawn)

pygame.key.set_repeat(int(1000/fps))

nn = N2(dimX = 1)###
print(nn.dimX)###

#rajout ennemi
dimx = []
dimy = 10
for i in range(20):
    dimx.append((int(i)*30))


change_dimx = 0

def spawn_enemies():
        
    global change_dimx
        
    enemies.append(Nafaire(( dimx[change_dimx] , dimy ), [pygame.image.load("ennemi.png")], type=NafaireTypes.ENNEMI))          #
            
    change_dimx += 1
    if change_dimx >= 20:
        change_dimx = 0
        #print("1 sec est passée")
#rajout

LEFT_CLICK = 1
keysDown = None

while leJeuTourne:

    ###gestion des evenements:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:# Change la valeur à False pour terminer le while
            leJeuTourne = False

        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            keysDown = pygame.key.get_pressed()

        elif event.type == pygame.MOUSEBUTTONUP: #tire quand on clique avec la souris
            if (event.button == LEFT_CLICK and peutTirer == True): 
                tire()            

        elif event.type == DELAY_TIRE_EVENT:
            peutTirer = True

        elif event.type == COLLISION_EVENT:

            if(event.collision == None):#collision avec la 'bordure du cadre'
                
                if(event.source.type == NafaireTypes.JOUEUR or event.source.type == NafaireTypes.ENNEMI):
                    ###corrige la position du joueur ou de l'ennemi pour qu'il ne sorte pas du cadre
                    if event.source.x < 0 : event.source.x = 0
                    if event.source.x > dimentions[0] : event.source.x = dimentions[0]
                    if event.source.y < 0 : event.source.y = 0
                    if event.source.y > dimentions[1] : event.source.y = dimentions[1]

                elif(event.source.type == NafaireTypes.BALLE):
                    ###détruit les balles hors champs
                    if event.source in balleList:
                        balleList.remove(event.source)                

            elif(event.source.type == NafaireTypes.BALLE and event.collision.type == NafaireTypes.ENNEMI):#collision balle ennemi
                if event.collision in enemies:
                    enemies.remove(event.collision)
                if event.source in balleList:
                    balleList.remove(event.source)
                score += 1
                
            elif(event.source.type == NafaireTypes.ENNEMI and event.collision.type == NafaireTypes.JOUEUR) or (event.source.type == NafaireTypes.JOUEUR and event.collision.type == NafaireTypes.ENNEMI):#collision joueur ennemi
                event.source.x, event.source.y = event.source.anciennePos
                event.source.rect = event.source.animation[0].get_rect(center=(event.source.x, event.source.y))

        elif event.type == SPAWN_TIMER_EVENT:
            spawn_enemies()
            print(len(enemies))


        elif event.type == AFFICHAGE_TIMER_EVENT:
            
            #gestion des déplacement dans le timer d'affichage pour eviter les bugs graphiques liés au déplacements trop rapides
            if(keysDown != None):

                tmpDeplacementJoueur = dim(0, 0)
       
                if keysDown[pygame.K_z]:             
                    tmpDeplacementJoueur.y -= 1
                if keysDown[pygame.K_s]:
                    tmpDeplacementJoueur.y += 1
                if keysDown[pygame.K_q]:
                    tmpDeplacementJoueur.x -= 1
                if keysDown[pygame.K_d]:                
                    tmpDeplacementJoueur.x += 1  
                if (keysDown[pygame.K_SPACE] and peutTirer == True):
                    tire()           
                
                if(tmpDeplacementJoueur.x != 0 or tmpDeplacementJoueur.y != 0):
                    Joueur.deplacement(tmpDeplacementJoueur.x, tmpDeplacementJoueur.y)

                keysDown = None

            if(len(enemies) != 0): 
                for ennemi in enemies:
                    ennemi.deplacement(0, 1)

            for b in balleList:
                b.deplacement(0, -1)

            Affichage()


        




