import pygame, sys, time
from pygame.locals import *
from startmenu import *
from gameloop import *
from gameover import *

pygame.init() #on initialise pygame

taille_fenetre = [960, 640] #la fenetre de largeur x et de hauteur y
fenetre = pygame.display.set_mode(taille_fenetre, pygame.RESIZABLE) #on cree la fenetre de la taille precedente
pygame.display.set_caption("ArticKnight") #le nom de la fenetre
a = pygame.image.load(realpath('res','icon.png')).convert_alpha() #on charge l icone
pygame.display.set_icon(a) #on met l icone

gameover = GameOver()
startmenu = StartMenu()
while 1:
        gameloop = GameLoop() #on reinitialise la boucle du jeu

        #afficher les differents ecrans
        startmenu.afficher(gameover.startmenu, fenetre)
        gameloop.afficher(fenetre)
        gameover.afficher(gameloop.compteur, gameloop.showgameover, fenetre)