import pygame

leJeuTourne = True
Score = 0
dimentions = (1024, 720)
Fenêtre = None
timer = pygame.time.Clock()

X,Y = 0,1

#personnage joueur
class Nafaire:
    def __init__(self, position=[0,0], animation=[], vie=0, dmg=1, vitesse=10):
        self.position = position
        self.animation = animation
        self.vie = vie
        self.dmg = dmg   
        self.vitesse = vitesse
        
def Affichage():

    Fenêtre.blit(arrièrePlan.animation[0], arrièrePlan.position)
    Fenêtre.blit(Joueur.animation[0], Joueur.position) #dessine le personnage à l'écran

    pygame.display.update()
 

def tire():
    return 0

#DEBUT DU PROGRAMME
pygame.init()   #initialisation de pygame
pygame.display.set_caption("JEU BIEN")  #titre du jeu
Fenêtre = pygame.display.set_mode(dimentions) # crée la fenêtre et enregiste sa variable

arrièrePlan = Nafaire([0,0], [pygame.image.load("background0.png")])
arrièrePlan.animation[0] = pygame.transform.scale(arrièrePlan.animation[0], dimentions)

Joueur = Nafaire([dimentions[X] / 2, dimentions[Y] / 2], [pygame.image.load("quack0.png")])
enemi = Nafaire()
balle = Nafaire()
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
            Joueur.position[Y] -= 1 * Joueur.vitesse
        if keysDown[pygame.K_s]:
            Joueur.position[Y] += 1 * Joueur.vitesse
        if keysDown[pygame.K_q]:
            Joueur.position[X] -= 1 * Joueur.vitesse
        if keysDown[pygame.K_d]:                
            Joueur.position[X] += 1 * Joueur.vitesse
    ###

    Affichage()






