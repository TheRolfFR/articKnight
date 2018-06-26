import pygame
from pygame.locals import *
from classes import *

class StartMenu:
    "charge le menu de demarrage"
    def __init__(self):
        self.fenetre = ''
        return None
    def afficher(self, lancer,fenetre):
        while lancer:
            for event in pygame.event.get(): #Attente des événements
                if event.type == pygame.QUIT: #evenenment quitter
                    stop()
                if event.type == pygame.VIDEORESIZE:
                    resizeWindow(fenetre, RESIZABLE, event)

            #definir le conteneur
            container, offset, ratio = getcontainer(fenetre)
            
            start = pygame.image.load(realpath('res','startmenubackground.png')).convert_alpha()
            start = pygame.transform.scale(start, container.get_size())
            container.blit(start, (0,0))

            startbutton = Bouton(190,70, ((container.get_width() - 190)//2),(container.get_height()-100)//2- 70, summersky,'start')
            quitter = Bouton(190,70, ((container.get_width() - 190)//2),(container.get_height()+100)//2, poppy,'quit')
            fsbutton = Bouton( 50, 50, container.get_width() - 100, 50, red, '', realpath('res','fullscreen.png'))

            startbutton.afficher(container, offset, ratio)
            quitter.afficher(container, offset, ratio)
            fsbutton.afficher(container, offset, ratio)
            
            showinfenetre(fenetre, container)

            if(quitter.click()):
                stop()
            if(startbutton.click()):
                lancer = False
            if(fsbutton.click()):
                switchMode(fenetre)
                
            pygame.display.update()