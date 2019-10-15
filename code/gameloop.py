import pygame
from pygame.locals import *
from classes import *

class GameLoop:
    def __init__(self):
        self.compteur = 0
        self.showgameover = 1
    def afficher(self,fenetre):
        clock = pygame.time.Clock() #on charge une horloge
        
        container, offset, ratio = getcontainer(fenetre)

        perso = Personnage(container) #on initialise le personnage
        poulets = Poulets()
        mes_projectiles = Projectiles()
        pause  = Pausemenu()
        while perso.vie > 0:
            container, offset, ratio = getcontainer(fenetre)
            keys = pygame.key.get_pressed()
            pause.verifier(keys)

            for event in pygame.event.get(): #Attente des événements
                    if event.type == pygame.QUIT: #evenenment quitter
                            stop()
                    if event.type == pygame.VIDEORESIZE:
                        resizeWindow(fenetre, RESIZABLE, event)

            if pause.ispaused:
                fond = pygame.image.load(realpath('res', 'pausemenu.png')).convert()
                container.blit(fond, (0,0))

                resumebutton = Bouton(240, 96, 48, 224, summersky, 'RESUME')
                homebutton = Bouton(240, 96, 48, 352, edward, 'HOME')
                quitbutton = Bouton(240, 96, 48, 480, poppy, 'QUIT')
                fsbutton = Bouton( 50, 50, container.get_width() - 47-50, 64, red, '', realpath('res', 'fullscreen.png'))

                resumebutton.afficher(container, offset, ratio)
                homebutton.afficher(container, offset, ratio)
                quitbutton.afficher(container, offset, ratio)
                fsbutton.afficher(container, offset, ratio)

                if resumebutton.click():
                    pause.switchpause()
                if homebutton.click():
                    #dont go to gameovermenu
                    #go to startmenu
                    perso.vie = 0
                    self.showgameover = 0
                if quitbutton.click():
                    stop()
                if fsbutton.click():
                    switchMode(fenetre)
            else:
                pattern(container,realpath('res', 'Background.png'),[0,0],[0,0]) #on charge le terrain avec laterre
                
                perso.bouger(keys) #on bouge le personnage en fonction des touches appuyees

                perso.verifier(poulets,container)

                poulets.verifier(container, perso)
                
                mes_projectiles.verifier(perso, keys, container, poulets)
                #Rafraichissement
                mes_projectiles.afficher(container)
                perso.afficher(container) #on affiche le personnage dans la fenetre
                poulets.afficher(container)
                poulets.compteur(container)

            showinfenetre(fenetre, container)

            self.compteur = poulets.morts
            
            pygame.display.update() #on rafraichit l ecran

            clock.tick(60) #on fixe la frequence de rafraichissement a 60fps
