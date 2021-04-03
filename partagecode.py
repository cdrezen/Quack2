import pygame

leJeuTourne = True
Score = 0

#personnage joueur
class Nafaire:
    def __init__(self, position = [0,0], vie = 0, dmg = 1, vitesse = 1):
        self.position = position
        self.vie = vie
        self.dmg = dmg   
        self.vitesse = vitesse
        
Joueur = Nafaire()
enemi = Nafaire()
balle = Nafaire()
bonus = Nafaire(dmg=0, vitesse=0)
tr

print(bonus)











while leJeuTourne:



    ###gestion des evenements:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:# change the value to False, to exit the main loop
            running = False

        if event.type == pygame.MOUSEMOTION:
            mousePos = list(pygame.mouse.get_pos())


    ###







