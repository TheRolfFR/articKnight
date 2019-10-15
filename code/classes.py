import pygame, sys, time, random, math, os
from win32api import GetSystemMetrics
from pygame.locals import *

def getcontainer(fenetre):
    fenetre.fill(black)
    contain = pygame.Surface((960,640))

    if contain.get_height()/fenetre.get_height() < contain.get_width()/fenetre.get_width():
        ratio = fenetre.get_width() / contain.get_width()
        offset = (0, (fenetre.get_height() - (ratio*contain.get_height()))//2)
    else:
        ratio = fenetre.get_height() / contain.get_height()
        offset = ((fenetre.get_width()-(ratio*contain.get_width()))//2, 0)

    return contain, offset, ratio

def showinfenetre(fenetre, container):
    c, offset, ratio = getcontainer(fenetre)

    #afficher le conteneur
    if container.get_height()/fenetre.get_height() < container.get_width()/fenetre.get_width():
        # f w | c w
        # f h |  ?
        container = pygame.transform.scale(container, (fenetre.get_width(), int(ratio * container.get_height())))
    else:
        # f h | c h
        # f w |  ?
        container = pygame.transform.scale(container, (int(ratio * container.get_width()), fenetre.get_height()))
    fenetre.blit(container, offset)

def resizeWindow(fenetre, mode, event =""):
    minwidth = 960
    minheight = 640

    if not((event != '') and (fenetre.get_flags() == FULLSCREEN)):
        if event == '':
            if(mode == pygame.RESIZABLE):
                width, height = minwidth,minheight
            else:
                width = int(GetSystemMetrics(0))
                height = int(GetSystemMetrics(1))
        else:
            width, height = event.size
        
        if width < minwidth:
            width = minwidth
        if height < minheight:
            height = minheight
        
        fenetre = pygame.display.set_mode((width,height), mode|DOUBLEBUF|HWSURFACE)

def switchMode(fenetre):
    if fenetre.get_flags() & FULLSCREEN:
        resizeWindow(fenetre, pygame.RESIZABLE)
    else:
        resizeWindow(fenetre, pygame.FULLSCREEN)

def stop():
    "quitter le jeu sans erreurs"
    pygame.quit()
    sys.exit()

def pattern(fenetre, image,marge_debut,marge_fin): #fonction pour afficher un pattern dans une surface
    """gere un background avec fenetre"""
    f_taille = list(fenetre.get_size()) #la taille de la fenetre parente
    fond = pygame.image.load(image).convert_alpha() #on charge l image demandee en parametre
    surface = pygame.Surface([f_taille[0] - marge_debut[0] - marge_fin[0],f_taille[1] - marge_debut[1] - marge_fin[1]]) # on cree une surface de la taille de la fenetre parente - marge haut gauche - marge bas droit
    for a in range((f_taille[0] - marge_debut[0] - marge_fin[0]) // fond.get_width() + 1): #pour la largeur de la surface // largeur du fond + 1 au cas ou il ya un reste
        for i in range((f_taille[1] - marge_debut[1] - marge_fin[1]) // fond.get_height() + 1): #pour la hauteur de la surface // hauteur du fond + 1 au cas ou il ya un reste
            surface.blit(fond, (a * fond.get_width(),i * fond.get_height())) #on colle sur notre surface notre pattern
    fenetre.blit(surface,marge_debut) #on affiche le pattern dans la fenetre parente decale de la marge haut gauche

def barredevie(vie, vie_max, position, size, fenetre):
    "fonction barre de vie"
    hauteur = 4 #hauteur en pixel de la barre
    largeur = int(size[0]*.8) # large de 80% de la largeur du personnage
    fraction = int(vie / vie_max * largeur) # calcul de la largeur de pourcentage de vie restant
    fond = pygame.Surface((largeur,hauteur), pygame.SRCALPHA) # le fond de la barre transparente
    fond.fill((0,0,0,100)) # fond de couleur noir et d alpha 100 / 255
    barre_verte = pygame.Surface((fraction,hauteur), pygame.SRCALPHA)# le fond de la barre de vie verte transparente
    barre_verte.fill((39, 174, 96,255)) # fond de couleur verte

    position = [position[0] + (size[0]-largeur)//2, position[1] - 2 * hauteur] # on la positionne centrée au dessus du joueur
    fenetre.blit(fond, position) #on affiche le fond sur la fenetre
    fenetre.blit(barre_verte, position) # puis on affiche la barre verte sur la fenetre

def collision(objet1_position, objet1_size, objet2_position, objet2_size):
    # collision x
    # si position objet2 x + largeur objet2 > position objet1 x et si postion objet1x + largeur objet1x > position objet2 x
    #               [obj2] > [obj1]                                     [obj1] < [obj2]
    if ((objet2_position[0] + objet2_size[0]) > objet1_position[0]) and ((objet1_position[0] + objet1_size[0]) > objet2_position[0]):
        if ((objet2_position[1] + objet2_size[1]) > objet1_position[1]) and ((objet1_position[1] + objet1_size[1]) > objet2_position[1]):
            return True
    return False
class Personnage: #objet personnage
    "objet personnage"
    def __init__(self, fenetre):
        self.prefix = "perso/perso_" #dossier des sprites du personnage + prefixe nom fichier
        self.extension = ".png" #extension de l image
        self.image = 0 #image du sprite en cours
        self.images = 3 #image maximale du sprite
        self.vitesse_image = 2 #vitesse de defilement du sprite (divise par la valeur)
        self.moving = False #si le personnage bouge
        
        self.rect = pygame.image.load(realpath('perso', "perso_0"+self.extension)).get_rect()
        self.rect[0] = fenetre.get_size()[0]//2 #position de depart
        self.rect[1] = fenetre.get_size()[1]//2 #position de depart
        
        self.direction = 1 #direction du regard 1 = droite, gauche = -1
        self.vitesse = 5 #vitesse de deplacement (en pixel)
        self.vie = self.vie_max = 5 #points de vie et points de vie max (5max)
        self.damage = 0 #temps depuis le dernier degat
        self.damage_delay = 2 #temps en seconde entre les dégats que peux prendre le personnage
    def bouger(self,keys): #fonction bouger en fonction(de cle)
        "gere le mouvement du personnage en fonction de la touche appuyee"
        #les touches sont en qwerty donc ZQSD = WASD
        up    = K_w
        left  = K_a
        down  = K_s
        right = K_d
        if keys[up] or keys[left] or keys[down] or keys[right]: #si on bouge, on met la variable objet moving a vrai sinon a faux
            self.moving = True
        else:
            self.moving = False

        "le deplacement va s appuyer sur un facteur vitesse qui va diriger la vitesse en fonction de la touche appuyee ou -1 dirige la vitesse dans la direction contraire"
        facteur = [0,0]
        if keys[up]:
            facteur[1] = -1
        if keys[down]:
            facteur[1] = 1
        if keys[left]:
            facteur[0] = -1
        if keys[right]:
            facteur[0] = 1

        "on va mettre a jour la variable objet direction pour renverser ou pas l image"
        if facteur[0] != 0:
            self.direction = facteur[0]
            
        self.rect[0] = self.rect[0] + self.vitesse * facteur[0]
        self.rect[1] = self.rect[1] + self.vitesse * facteur[1]
    def afficher(self,fenetre):
        barredevie(self.vie, self.vie_max, [self.rect[0], self.rect[1]], [self.rect[2], self.rect[3]], fenetre) #voir la fonction barre de vie
        "afficher le personnage dans la fenetre"

        "il va falloir mettre a jour les sprites en boucle si on bouge"
        if self.moving:
            if self.image < self.images*self.vitesse_image + self.vitesse_image - 1 :
                self.image += 1
            else:
                self.image = 0
        else:
            self.image = 0
        
        numero = self.image // self.vitesse_image
        image = pygame.image.load(self.prefix + str(numero) + self.extension).convert_alpha() #on charge l image du sprite

        if self.direction == 1: #si la direction est vers la droite on renverse verticalement l image
            image = pygame.transform.flip(image, 1, 0)

        fenetre.blit(image,self.rect) #on affiche l image
    def verifier(self, poulets,fenetre):
        for poulet in poulets.tableau:
            delai = time.time() - self.damage
            if self.rect.colliderect(poulet) and delai > self.damage_delay:
                self.vie -= 1
                self.damage = time.time()
                
class Projectiles:
    def __init__(self):
        self.nombre = 0
        self.tableau = list()
        self.imagesrc = 'res/snowball.png'
        self.image = pygame.image.load(self.imagesrc).convert_alpha()
        self.size = self.image.get_size()
        self.vitesse = 10
        self.lastshoot = 0
        self.delaishoot = .4
        self.limiteshoot = int(20*self.vitesse)
    def verifier(self,personnage,keys,terrain,poulets):
        t_taille = terrain.get_size()
        delai = time.time() - self.lastshoot
        shootleft = K_LEFT
        shootright = K_RIGHT
        shoottop = K_UP
        shootdown = K_DOWN
        shootx = 0
        shooty = 0
        if (keys[shootleft] or keys[shootright] or keys[shoottop] or keys[shootdown]) and delai >= self.delaishoot:
            self.lastshoot = time.time()
            if keys[shootleft]:
                shootx = -1
            if keys[shootright]:
                shootx = 1
            if keys[shoottop]:
                shooty = -1
            if keys[shootdown]:
                shooty = 1
            add = [personnage.rect[0]+(personnage.rect[2] - self.size[0])//2, personnage.rect[1] + (personnage.rect[3] - self.size[1])//2, shootx, shooty, 0]
            #[x, y, directionx, directiony, distanceParcourue]
            #[0, 1,      2    ,     3     ,         4        ]
            self.tableau.append(add)
        i = 0
        while i < len(self.tableau):
            projectile = self.tableau[i]
            if (0 < projectile[0] < t_taille[0] or 0 < projectile[1] < t_taille[1]) and (projectile[4]*self.vitesse < self.limiteshoot):
                self.tableau[i][0] = self.tableau[i][0] + self.tableau[i][2] * self.vitesse
                self.tableau[i][1] = self.tableau[i][1] + self.tableau[i][3] * self.vitesse
                self.tableau[i][4] += 1
            else:
                self.tableau.pop(i)
                i -= 1
            a = 0
            while (a < len(poulets.tableau)) and (len(self.tableau)):
                poulet = poulets.tableau[a]
                touche = False
                ajouter = 0
                while (ajouter < self.vitesse) and (touche == False):
                    if(collision([poulet.rect[0],poulet.rect[1]], [poulet.rect[2], poulet.rect[3]],[projectile[0]+ajouter*projectile[2],projectile[1]+ajouter*projectile[3]],self.size)):
                        touche= True
                    ajouter += 1
                    #print("boucle",self.vitesse, ajouter < self.vitesse)
                if (poulet.vie > 0) and touche:
                    poulet.vie -= 1
                    self.tableau.pop(i)
                a += 1
            i += 1
    def afficher(self, fenetre):
        for projectile in self.tableau:
            fenetre.blit(self.image, (projectile[0]+self.vitesse*projectile[4]*projectile[2],projectile[1]+self.vitesse*projectile[4]*projectile[3]))

class Poulet:
    def __init__(self, fenetre):
        self.vie = self.vie_max = 2
        self.prefix = "poulet/poulet_" #dossier des sprites du personnage + prefixe nom fichier
        self.extension = ".png" #extension de l image
        self.image = 0 #image du sprite en cours
        self.images = 3 #image maximale du sprite
        self.vitesse_image = 4 #vitesse de defilement du sprite (divise par la valeur)
        self.surface = pygame.image.load(realpath('poulet', 'poulet_0.png')).convert_alpha()
        self.rect = self.surface.get_rect()


        self.rect[0] = self.rect[1] = 0
        origin = random.randint(0,3) # 0 <= N <= 3 : cote duquel arrive le poulet 0 haut 1 droite 2 bas 3 gauche
        if origin == 0:
            self.rect[0] = random.randint(0,fenetre.get_size()[0])
        if origin == 1:
            self.rect[0] = fenetre.get_size()[0]
            self.rect[1] = random.randint(0,fenetre.get_size()[1])
        if origin == 2:
            self.rect[0] = random.randint(0,fenetre.get_size()[0])
            self.rect[1] = fenetre.get_size()[0]
        if origin == 3:
            self.rect[1] = random.randint(0,fenetre.get_size()[1])
        
        self.direction = 0
        self.vitesse = 3
    def verifier(self, perso):
        #pour x
        #si difference entre position perso et position poulet < vitesse, poulet position = perso position

        # distance = math.sqrt(pow(abs(self.rect[0] - perso.rect[0]),2) + pow(abs(self.rect[1] - perso.rect[1]),2))
        
        #deplacement lineaire vers le poulet
        angle = math.atan2(abs(self.rect[1] - perso.rect[1]), abs(self.rect[0] - perso.rect[0]))
        
        if abs(self.rect[0] - perso.rect[0]) < self.vitesse:
            self.rect[0] = perso.rect[0]
        else:
            if perso.rect[0] < self.rect[0]:
                self.rect[0] -= int(math.cos(angle)*self.vitesse)
                self.direction = 1
            if perso.rect[0] > self.rect[0]:
                self.rect[0] += int(math.cos(angle)*self.vitesse)
                self.direction = 0

        if abs(self.rect[1] - perso.rect[1]) < self.vitesse:
            self.rect[1] = perso.rect[1]
        else:
            if perso.rect[1] < self.rect[1]:
                self.rect[1] -= int(math.sin(angle)*self.vitesse)
            if perso.rect[1] > self.rect[1]:
                self.rect[1] += int(math.sin(angle)*self.vitesse)

class Poulets:
    def __init__(self):
        self.nombre = 0
        self.tableau = list()
        self.dernier_spawn = 0
        self.limite_spawn = 10
        self.delai_spawn = 3
        self.morts = 0
    def verifier(self, fenetre, perso):
        if len(self.tableau) < self.limite_spawn:
            delai = time.time() - self.dernier_spawn
            if delai > self.delai_spawn:
                self.dernier_spawn = time.time()
                self.tableau.append(Poulet(fenetre))
                self.nombre += 1

        i = 0
        for poulet in self.tableau:
            poulet.verifier(perso)
            if poulet.vie <= 0:
                self.tableau.pop(i)
                self.morts += 1
                self.nombre -= 1
            i += 1
    def compteur(self,fenetre):
        " un compteur de score"
        font = pygame.font.Font(realpath('font', '8-BIT-WONDER.ttf'), 30) #on charge le font
        text = font.render(str(self.morts), True, (0,0,0)) #on fait un rendu du nombre de score en noir
        text_rect = text.get_rect() #on recupere le placement
        text_rect[0] = text_rect[1] = 20 #on modifie es coordonees x et y a 20
        fenetre.blit(text, text_rect) #on affiche donc le score en (20;20)
    def afficher(self, fenetre):
        for a in range(len(self.tableau)): #pour chaque poulet dans le tableau
            poulet = self.tableau[a]
            if poulet.vie < poulet.vie_max:
                barredevie(poulet.vie, poulet.vie_max, [poulet.rect[0], poulet.rect[1]], [poulet.rect[2], poulet.rect[3]], fenetre) #voir la fonction barre de vie

            "il va falloir mettre a jour les sprites en boucle si on bouge"
            if poulet.image < poulet.images*poulet.vitesse_image + poulet.vitesse_image -2 :
                poulet.image +=1
            else:
                poulet.image = 0

            numero = poulet.image // poulet.vitesse_image
            image = pygame.image.load(poulet.prefix + str(numero) + poulet.extension).convert_alpha() #on charge l image du sprite

            if poulet.direction: # si le poulet se dirige dans la direction opposée au sprite
                image = pygame.transform.flip(image, 1, 0) #on fait un mirroir horizontal sur l'image (eviter le moonwalk)
            fenetre.blit(image, poulet.rect) #on affiche le poulet en fonction de sa position

#tableaux de couleurs rgb
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (59,74,114)
belize = (41, 128, 185)
summersky = (30, 139, 195)
royal = (65, 131, 215)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
rose = (255,0,127)
pumpkin = (211, 84, 0)
red2 = (51,0,0)
poppy = (192, 57, 43)
grey = (20,20,20)
darkgray = (46,46,46)
edward = (171, 183, 183)

def realpath(path, filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path, filename)

#on initialise les font
pygame.font.init()
path = realpath('font', '8-BIT-WONDER.ttf')
print(path)
littleText = pygame.font.Font(path, 20) #la police d'écriture 8-BIT-WONDER.ttf en 20pt
font = pygame.font.Font(path, 30) #la police d'écriture 8-BIT-WONDER.ttf en 30pt

class Bouton:
    "classe pour creer un bouton"
    def __init__(self,width, height, x, y, bgcolor, text, img=''):
        self.img = img
        self.bgcolor = list(bgcolor) #on stocke la couleur de fond
        self.text = text #on stocke le texte
        
        lighter = 20 #couleur plus claire de 20 / 255 
        
        self.lightercolor = list()

        #on va creer une couleur plus claire comme ca quand on survole le bouton on change la couleur de fond
        for color in self.bgcolor:
            if (color + lighter) > 255:
                self.lightercolor.append(255) #max
            else:
                self.lightercolor.append(color + lighter) #sinon additionner (+ haut = + blanc)
        
        self.border = 5 #la bordure inferieure du bouton 5px
        self.size = [width, height]
        self.pos = [x, y]
        self.decalage = 5 #le decalage de l'ombre du texte

        self.offset = (0,0)
        self.ratio = 1
        self.incontainer = 0
    def afficher(self, fenetre, offset = (0,0), ratio = 1):
        self.ratio = ratio
        self.offset = offset
        leftoffset, topoffset = self.offset
        mouse = pygame.mouse.get_pos()

        if leftoffset + (self.pos[0]+self.size[0])*self.ratio > mouse[0] > leftoffset + self.pos[0]*self.ratio and topoffset + (self.pos[1]+self.size[1])*self.ratio > mouse[1] > topoffset + self.pos[1]*self.ratio: #si on survole le bouton
            color = self.lightercolor #on met une couleur de fond plus claire
        else:
            color = self.bgcolor #sinon la couleur normale
        
        texte = font.render(self.text, True, white) #on fait un rendu du texte

        #on va verifier la largeur du texte et s'il est plus grand que la largeur demandée alors la largeur du bouton sera celle du texte + marge (horizontale)
        marge = 20
        if self.size[0] < texte.get_size()[0]:
            self.size[0] = texte.get_size()[0] + marge
        
        texte_rect = texte.get_rect(center=(self.size[0]*0.5,self.size[1]*0.5 - (self.border//2))) # on prend en compte la bordure et on la soustrait pour aligner parfaitement le texte verticalement

        #on va creer dans l ordre
        # - ombre texte (20% transparente - noire)
        # - bordure (20% transparente - noire)
        shadow = font.render(self.text, True, black)
        surface_shadow = pygame.Surface(shadow.get_size())
        surface_shadow.fill(color)
        surface_shadow.blit(shadow, [0,0])
        surface_shadow.set_alpha(20*225//100)
        surface_shadow_rect = texte.get_rect(center=(self.size[0]*0.5 + self.decalage,self.size[1]*0.5 - (self.border//2))) # on prend en compte la bordure et on la soustrait pour aligner parfaitement le texte verticalemen

        if self.img == '':
            border = pygame.Surface((self.size[0], self.border))
            border.fill(black)
            border.set_alpha(20*225//100)
            border_rect = border.get_rect()
            border_rect[1] = self.size[1]-self.border

        #le code suivant va faire dans l'ordre :
        # - creer le bouton
        # - remplir le bouton avec la couleur de fond desiree si ce n'est pas une image
        # - on remplit avec l'image si elle est precisee
        # - on affiche l'ombre dans le bouton
        # - on affiche le texte dans le bouton
        # - on affiche la bordure dans le bouton si ce n'est pas une image
        # - on affiche le bouton dans la fenetre
        
        if self.img != '':
            image = pygame.image.load(self.img).convert_alpha()
            bouton = pygame.transform.scale(image, self.size)
        else:
            bouton = pygame.Surface(self.size)
            bouton.fill(color)
            bouton.blit(surface_shadow, surface_shadow_rect)
            bouton.blit(texte, texte_rect)
            bouton.blit(border, border_rect)
        
        fenetre.blit(bouton, self.pos)
    def click(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        leftoffset, topoffset = self.offset

        if leftoffset + (self.pos[0]+self.size[0])*self.ratio > mouse[0] > leftoffset + self.pos[0]*self.ratio and topoffset + (self.pos[1]+self.size[1])*self.ratio > mouse[1] > topoffset + self.pos[1]*self.ratio: #si on survole le bouton
            if click[0] == 1: # si on clique gauche dessus
                return True # alors on retourne vrai

class Pausemenu:
    def __init__(self):
        self.ispaused = 0
    def verifier(self, keys):
        esc = K_ESCAPE
        if keys[esc]:
            self.switchpause()
    def switchpause(self):
        self.ispaused = 1 - self.ispaused
        time.sleep(200/1000)