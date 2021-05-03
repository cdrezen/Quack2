import pygame

leJeuTourne = True
Score = 0
dimentions = (1024, 720)
Fenêtre = None
timer = pygame.time.Clock()
#bonusTime = 51

#personnage joueur
class Nafaire:
    def __init__(self, position=(0,0), animation=None, vie=0, dmg=1, vitesse=25, vitesseY=25, rect=None):
        self.x , self.y = position
        self.animation = animation
        self.vie = vie
        self.dmg = dmg   
        self.vitesse = vitesse
        self.vitesseY = vitesseY
        
        if(animation == None): return
        
        self.rect = self.animation[0].get_rect(center=(self.x, self.y))

    def deplacement(self, x, y):
        self.x += x * self.vitesse
        self.y += y * self.vitesseY
        self.rect = self.animation[0].get_rect(center=(self.x, self.y))

#affichage contiens ce qui doit etre affiché grace a pygame il es tutiliser a la fin du mainloop pour raffraichir l'affichage  
def Affichage():

    Fenêtre.blit(arrièrePlan.animation[0], (arrièrePlan.x, arrièrePlan.y))
    Fenêtre.blit(Joueur.animation[0], Joueur.rect) #dessine le personnage à l'écran
    Fenêtre.blit(ennemi.animation[0], ennemi.rect)

    for b in balleList:
        Fenêtre.blit(b.animation[0], b.rect)

    pygame.display.update()
 

def tire():
    balle = Nafaire([Joueur.x, Joueur.y], balleImg)
    balleList.append(balle)

#DEBUT DU PROGRAMME
pygame.init()   #initialisation de pygame
pygame.display.set_caption("JEU BIEN")  #titre du jeu
Fenêtre = pygame.display.set_mode(dimentions) # crée la fenêtre et enregiste sa variable

arrièrePlan = Nafaire([0,0], [pygame.image.load("background0.png")])
arrièrePlan.animation[0] = pygame.transform.scale(arrièrePlan.animation[0], dimentions)

Joueur = Nafaire([dimentions[0] / 2, dimentions[1] / 2], [pygame.image.load("quack0.png")])

ennemi = Nafaire([dimentions[0] / 2, 5 ], [pygame.image.load("heart.png")])   #cree un ennemi

balleImg = [pygame.image.load("heart.png")]
balleList = list()
bonus = Nafaire(dmg=0, vitesse=0)
    


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

        #corrige la position du joueur pour qu'il ne sorte pas du cadre
        if Joueur.x < 0 : Joueur.x = 0
        if Joueur.x > dimentions[0] : Joueur.x = dimentions[0]
        if Joueur.y < 0 : Joueur.y = 0
        if Joueur.y > dimentions[1] : Joueur.y = dimentions[1]

        Joueur.rect = Joueur.animation[0].get_rect(center=(Joueur.x, Joueur.y))

    ennemi.deplacement(0, 1)

    for b in balleList:
        b.deplacement(0, -1)
    ###

    Affichage()






