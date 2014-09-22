# -*- coding:Utf-8 -*-

# Jeu de la vie, version optimisée
# (c) Léo Noël-Baron 2014

import pygame
from pygame.locals import *
from random import random
from time import clock
from math import sin, pi, sqrt

class Monde:
    
    """Cette classe implémente le monde dans lequel se déroule le jeu.
    Elle est principalement une classe-enveloppe de dictionnaire.
    
    """
    
    def __init__(self, larg, haut, i_max):
        """Constructeur de la classe"""
        self._monde = [[0] * haut for i in range(larg)]
        self.largeur = larg
        self.hauteur = haut
        self.i_max = i_max
        self.vivants = []
    
    def __getitem__(self, coords):
        """Retourne l'état d'une cellule donnée"""
        x, y = coords
        return self._monde[x][y]
        
    def dessiner(self):
        def hsl_rgb(couleur):
            h, s, l = couleur
            c = (1 - abs(2*l - 1)) * s
            x = c * (1 - abs((h*6)%2 - 1))
            rgb = []
            if h < 1/6:
                rgb = [c, x, 0]
            elif h < 2/6:
                rgb = [x, c, 0]
            elif h < 3/6:
                rgb = [0, c, x]
            elif h < 4/6:
                rgb = [0, x, c]
            elif h < 5/6:
                rgb = [x, 0, c]
            else:
                rgb = [c, 0, x]
            m = l - 1/2*c
            return [255*(rgb[0] + m), 255*(rgb[1] + m), 255*(rgb[2] + m)]
        def f(x):
            # return (255*sin(x*pi), 255*sin(x*pi), 255*sin(x*pi))
            # return (0, 0, x*255)
            h = x if x < 0.8 else 0.8
            s = 0.2+x/1.5
            l = x**(1/2)/2
            if x > 0.8:
                s = l = 1-x
            return hsl_rgb((h, s, l))
            # return (255*x**(1/3)*sin(x*pi), 255*x*sin(x*pi), 255*sin(x*pi))
        for x in range(self.largeur):
            for y in range(self.hauteur):
                c_x = x / 250 - 2.1
                c_y = y / 250 - 1.2
                z_r = z_i = 0
                i = 0
                while i < self.i_max:
                    i += 1
                    tmp = z_r
                    z_r = z_r*z_r-z_i*z_i+c_x
                    z_i = 2*z_i*tmp+c_y
                    if z_r*z_r+z_i*z_i >= 4:
                        break
                self._monde[x][y] = f(i/self.i_max)
            print("Ligne", x, "sur", self.largeur)
                

def main():
    monde = Monde(700, 600, 150)
    start = clock()
    monde.dessiner()
    pygame.init()
    ecran = pygame.display.set_mode((monde.largeur, monde.hauteur))
    pygame.display.set_caption("Mandelbrot")
    bg = pygame.Surface(ecran.get_size())
    bg = bg.convert()
    bg.fill((250, 250, 250))
    ecran.blit(bg, (0, 0))
    tourne = True
    for y in range(monde.hauteur):
        for x in range(monde.largeur):
            if monde[(x, y)]:
                bg.set_at((x, y), monde[(x, y)])
    print("Dessiné en", round(clock() - start, 3), "secondes")
    pygame.image.save(bg, "mandelbroute.png")
    while tourne:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                tourne = False
                break
        ecran.blit(bg, (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main()
