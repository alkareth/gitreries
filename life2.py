# -*- coding:Utf-8 -*-

# Jeu de la vie, version optimisée
# (c) Léo Noël-Baron 2014

import pygame
from pygame.locals import *
from random import random
from time import sleep

class Monde:
    
    """Cette classe implémente le monde dans lequel se déroule le jeu.
    Elle est principalement une classe-enveloppe de dictionnaire.
    
    """
    
    def __init__(self, larg, haut):
        """Constructeur de la classe"""
        self._monde = [[0] * haut for i in range(larg)]
        self.largeur = larg
        self.hauteur = haut
        self.vivants = []
    
    def __str__(self):
        """Méthode de représentation"""
        ret = "_|"
        for i in range(self.largeur):
            ret += str(i).ljust(2)
        ret += "\n"
        for y in range(self.hauteur):
            ret += str(y).ljust(2)
            for x in range(self.largeur):
                ret += "o " if self[(x, y)] else "  "
            ret += "\n"
        return ret
    
    def __getitem__(self, coords):
        """Retourne l'état d'une cellule donnée"""
        x, y = coords
        return self._monde[x][y]
    
    def get_voisins(self, coords):
        """Retourne les voisins d'une cellule donnée"""
        x, y = coords
        voisins = []
        if y != 0:
            if x != self.largeur - 1:
                voisins.append((x+1, y-1)) # ymin xmax
            if x != 0:
                voisins.append((x-1, y-1)) # ymin xmin
            voisins.append((x, y-1))       # ymin
        if y != self.hauteur - 1:
            if x != self.largeur - 1:
                voisins.append((x+1, y+1)) # ymax xmax
            if x != 0:
                voisins.append((x-1, y+1)) # ymax xmin
            voisins.append((x, y+1))       # ymax
        if x != self.largeur - 1:
            voisins.append((x+1, y))       #      xmax
        if x != 0:
            voisins.append((x-1, y))       #      xmin
        return voisins
    
    def vivre(self, coords):
        """Fait vivre une cellule"""
        x, y = coords
        self._monde[x][y] = 1
        self.vivants.append(coords)
    
    def mourir(self, coords):
        """Fait mourir une cellule"""
        x, y = coords
        self._monde[x][y] = 0
        try:
            self.vivants.remove(coords)
        except ValueError:
            pass
    
    def randomiser(self, densite):
        """Fait vivre aléatoirement les cellules du monde"""
        for y in range(self.largeur):
            for x in range(self.largeur):
                if random() < densite:
                    self.vivre((x, y))
                else:
                    self.mourir((x, y))
    
    def vit(self, coords):
        """Renvoie le destin d'une cellule au prochain tour"""
        voisins = self.get_voisins(coords)
        v_vifs = [self[v] for v in voisins].count(1)
        if v_vifs == 3:
            return 1
        elif v_vifs == 2:
            return self[coords]
        else:
            return 0
    
    def boucler(self):
        """Calcule un tour de jeu"""
        maj = [list(li) for li in self._monde]
        potentiels = list(self.vivants)
        for c in self.vivants: # les vivants possibles sont les voisins
            potentiels.extend(self.get_voisins(c))
            # for v_c in vois_c:
                # if not v_c in potentiels:
                    # potentiels.append(v_c)
        for c in potentiels: # à opti
            x, y = c
            if self.vit(c):
                maj[x][y] = 1
                if not c in self.vivants:
                    self.vivants.append(c)
            else:
                maj[x][y] = 0
                if c in self.vivants:
                    self.vivants.remove(c)
        self._monde = maj

def main():
    monde = Monde(150, 150)
    pygame.init()
    horloge = pygame.time.Clock()
    ecran = pygame.display.set_mode((4*monde.largeur, 4*monde.hauteur))
    pygame.display.set_caption("Lifegame")
    bg = pygame.Surface(ecran.get_size())
    bg = bg.convert()
    bg.fill((250, 250, 250))
    ecran.blit(bg, (0, 0))
    nb = 1
    tourne = True
    lance = False
    gomme = False
    while tourne:
        horloge.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                tourne = False
                break
            elif pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                coords = (int(x/4), int(y/4))
                monde.vivre(coords)
            elif pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                coords = (int(x/4), int(y/4))
                monde.mourir(coords)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                lance = not lance
                print("démarré" if lance else "arrêté")
            elif event.type == KEYDOWN and event.key == K_c:
                monde.randomiser(-1)
                print("monde nettoyé")
            elif event.type == KEYDOWN and event.key == K_r:
                monde.randomiser(0.3)
                print("monde initialisé")
            bg.fill((250, 250, 250))
            for y in range(monde.hauteur):
                for x in range(monde.largeur):
                    if monde[(x, y)]:
                        pygame.draw.rect(bg, (0, 0, 0), (4*x, 4*y, 4, 4))
            ecran.blit(bg, (0, 0))
            pygame.display.flip()
        if lance:
            monde.boucler()
            bg.fill((250, 250, 250))
            for y in range(monde.hauteur):
                for x in range(monde.largeur):
                    if monde[(x, y)]:
                        pygame.draw.rect(bg, (0, 0, 0), (4*x, 4*y, 4, 4))
            ecran.blit(bg, (0, 0))
            pygame.display.flip()
            print("itération", nb)
            nb += 1

if __name__ == "__main__":
    main()
