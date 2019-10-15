import pygame
from pygame.locals import *
from classes import *

class GameOver:
    def __init__(self):
        self.gameover = False
        self.startmenu = True
        self.lancer = True
    def afficher(self, compteur, show, fenetre):
        self.startmenu = True
        #les 3 boutons et leur position
        while self.lancer and show:
            for event in pygame.event.get(): #Attente des événements
                if event.type == pygame.QUIT: #evenenment quitter
                    stop()
                if event.type == pygame.VIDEORESIZE:
                    resizeWindow(fenetre, RESIZABLE, event)


            container, offset, ratio = getcontainer(fenetre)
            
            container.fill(darkgray) #fond gris fonce

            #image au centre
            image = pygame.image.load(realpath('res', 'gameover.png')).convert_alpha()
            image_size = list(image.get_size())
            pos = list(container.get_size())
            pos[0] = pos[0] // 2 - image_size[0]//2
            pos[1] = pos[1] // 2 - image_size[1]
            container.blit(image ,pos)

            #texte en haut a gauche
            # game by :
            # Maxime Wisniewski
            # Yann Le Vaguerès
            texte_createurs = littleText.render("Game by", True, black)
            container.blit(texte_createurs, [20,20])
            texte_maxime = littleText.render("Maxime Wisniewski", True, white)
            container.blit(texte_maxime, [20, 20 + texte_createurs.get_height() + 10])
            texte_yann = littleText.render("Yann Le Vagueres", True, white)
            container.blit(texte_yann, [20, 20 + texte_createurs.get_height() + 10 + texte_maxime.get_height() + 10])

            #texte en haut a droite
            # Score
            # X
            texte_score = littleText.render("Score", True, black)
            texte_score_rect = texte_score.get_rect()
            texte_score_rect[0] = container.get_size()[0] - 20 - texte_score_rect[2]
            texte_score_rect[1] = 20
            container.blit(texte_score, texte_score_rect)

            texte_compteur = littleText.render(str(compteur), True, white)
            texte_compteur_rect = texte_compteur.get_rect()
            texte_compteur_rect[0] = container.get_size()[0] - 20 - texte_compteur_rect[2]
            texte_compteur_rect[1] = texte_score_rect[1] + texte_score_rect[3] + 10
            container.blit(texte_compteur, texte_compteur_rect)
            
            #texte milieu dessous image
            # Game Over
            texte_mort = font.render("Game Over", True, black)
            texte_mort_size = texte_mort.get_size()
            texte_mort_pos = list(container.get_size())
            texte_mort_pos[0] = texte_mort_pos[0] // 2 - texte_mort_size[0] // 2
            texte_mort_pos[1] = texte_mort_pos[1] // 2 + 30
            container.blit(texte_mort, texte_mort_pos)
                        
            #on afficher les boutons dessous
            home     = Bouton(190,70, (container.get_width()*1//4) - (190//2), (container.get_height()//2)+70+100, edward, 'home')
            restart  = Bouton(190,70, (container.get_width()*2//4) - (190//2) - 20,(container.get_height()//2)+70+100, summersky,'restart')
            quitter  = Bouton(190,70, (container.get_width()*3//4) - (190//2),(container.get_height()//2)+70+100, poppy,'quit')
            fsbutton = Bouton( 50, 50, container.get_width() - 100, container.get_height() - 100, red, '', realpath('res', 'fullscreen.png'))
            restart.afficher(container, offset, ratio)
            quitter.afficher(container, offset, ratio)
            home.afficher(container, offset, ratio)
            fsbutton.afficher(container, offset, ratio)
            
            showinfenetre(fenetre, container)

            #les actions si on clique
            if(quitter.click()):
                stop()
            if(restart.click()):
                self.startmenu = False
                self.lancer = False
            if(home.click()):
                self.startmenu = True
                self.lancer = False
            if(fsbutton.click()):
                switchMode(fenetre)

            pygame.display.update()
        self.lancer = True
