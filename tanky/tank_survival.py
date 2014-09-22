#!/usr/bin/python
# -*-coding:Utf-8 -*

# Copyright (c) 2013 NOEL-BARON Léo
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Fichier principal du jeu, contenant la fonction principale (mainloop)
et son appel. A lancer pour démarrer le jeu.

"""


import sys
import pygame
from pygame.locals import *

from fonctions import *
from classes_jeu import Tank, Obus, Explosion
from classes_deco import MenuPrincipal

def jeu():
    # Initialisation
    pygame.init()
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    icon = pygame.transform.scale(charger_img("tankb1.png"), (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Tank Survival")
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    bg = pygame.Surface(fenetre.get_size())
    bg.fill((255, 255, 255))
    fenetre.blit(bg, (0, 0))
    pygame.display.flip()
    horloge = pygame.time.Clock()
    menu = None
    # menu = MenuPrincipal(fenetre) # menu d'entrée en jeu
    
    # Création et configuration des groupes
    tout = pygame.sprite.RenderUpdates()
    tanks = pygame.sprite.Group()
    obus = pygame.sprite.Group()
    Tank.containers = tout, tanks
    Obus.containers = tout, obus
    Explosion.containers = tout
    
    # Création du tank
    tank1 = Tank(charger_imgs("tankb1.png", "tankb2.png"))
    tank1.rect.bottomleft = fenetre.get_rect().bottomleft
    tank2 = Tank(charger_imgs("tankr1.png", "tankr2.png"))
    tank2.rect.topright = fenetre.get_rect().topright
    tank2.direction = 0
    tank2.image = pygame.transform.rotate(tank2.image, 180)
    
    continuer = True
    while continuer:
        if menu:
            continuer = menu.traiter() # AAAAAAAAAARGH ! ou pas ?
            continue
        for e in pygame.event.get():
            if e.type == QUIT:
                continuer = False
            if e.type == KEYDOWN:
                if e.key == K_RCTRL and not tank1.recharge:
                    Obus(tank1)
                    tank1.recharge = 50
                elif e.key == K_SPACE and not tank2.recharge:
                    Obus(tank2)
                    tank2.recharge = 50
        # Nettoyage de la fenêtre et mise à jour des objets de jeu
        tout.clear(fenetre, bg)
        tout.update()
        
        # Collisions
        print(ratio_collision(tank1.direction))
        tank1_col = pygame.sprite.spritecollide(tank1, obus, False,
                collided=pygame.sprite.collide_rect_ratio(
                ratio_collision(tank1.direction)))
        tank2_col = pygame.sprite.spritecollide(tank2, obus, False,
                collided=pygame.sprite.collide_rect_ratio(
                ratio_collision(tank2.direction)))
        tank_col = [(tank1, tank1_col), (tank2, tank2_col)]
        for tank, l_obus in tank_col:
            tank.sante -= len([o for o in l_obus if o.tank is not tank])
            for o in l_obus:
                if o.tank is not tank:
                    Explosion(o)
                    o.kill()
        if pygame.sprite.spritecollide(tank1, pygame.sprite.GroupSingle(tank2),
                False, collided=pygame.sprite.collide_circle_ratio(0.7)):
            # Ici on devrait calculer l'angle de la collision et réagir en
            # conséquence, mais bon...
            # On pourrait plus simplement séparer le traitement en plages
            # d'angles 0 - Pi/4 - 3Pi/4 - Pi.
            tank1.direction -= 180
            tank2.direction -= 180
        
        # Fin de jeu
        if tank1.sante == 0:
            print("Joueur 2 remporte la victoire !")
            tank1.kill()
            continuer = False
        if tank2.sante == 0:
            print("Joueur 1 est le meilleur !")
            tank2.kill()
            continuer = False
        
        # Mouvements des chars
        clavier = pygame.key.get_pressed()
        if clavier[K_UP]:
            tank1.bouger()
        if clavier[K_DOWN]:
            tank1.bouger(arriere=True)
        sens = clavier[K_LEFT] - clavier[K_RIGHT]
        if sens != 0 and (clavier[K_UP] or clavier[K_DOWN]):
            tank1.tourner(sens)
        if clavier[K_w]:
            tank2.bouger()
        if clavier[K_s]:
            tank2.bouger(arriere=True)
        sens = clavier[K_a] - clavier[K_d]
        if sens != 0 and (clavier[K_w] or clavier[K_s]):
            tank2.tourner(sens)
        
        tout.draw(fenetre)
        pygame.display.flip()
        horloge.tick(40)

if __name__ == "__main__":
    jeu()
    pygame.quit()
    sys.exit(0)
