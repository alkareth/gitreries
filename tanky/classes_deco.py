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

"""Fichier contenant les classes déooratives (menu...).

"""

import os.path
import pygame
from pygame.locals import *

from __init__ import VERSION
from fonctions import charger_img, charger_imgs

class EltMenu(pygame.sprite.Sprite):

    """Classe représentant un item cliquable du menu"""
    def __init__(self, images, parent, pos, fonction):
        """Constructeur de l'élément"""
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(topleft=(parent.rect.top + pos[0],
                parent.rect.left + pos[1]))
        self.dessus = False
        self.fonction = fonction
    
    def update(self):
        """Vérifie la position de la souris"""
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.dessus = True
            self.image = self.images[1]
            self.image.blit(self.images[0], (0, 0))
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            self.dessus = False
            self.image = self.images[0]
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        
class MenuPrincipal(pygame.sprite.Sprite):

    """Classe représentant le premier menu affiché en jeu"""
    def __init__(self, fenetre):
        """Constructeur du menu"""
        pygame.sprite.Sprite.__init__(self)
        self.fenetre = fenetre
        self.image = charger_img(os.path.join("mp", "menu_principal.png"))
        self.rect = self.image.get_rect(center=fenetre.get_rect().center)
        self.menu = pygame.sprite.RenderUpdates()
        # Ajout des items du menu
        items = ["jouer2", "joueria", "credits", "quitter", "hover"]
        adresses = [os.path.join("mp", it + ".png") for it in items]
        jouer2, joueria, credits, quitter, hover = charger_imgs(*adresses)
        self.menu.add(
            EltMenu((jouer2, hover), self, (200, 20), self.jouer2),
            EltMenu((joueria, hover), self, (200, 100), self.jouer2)
            # EltMenu((jouer2, hover), self, (200, 20), self.jouer2)
            # EltMenu((jouer2, hover), self, (200, 20), self.jouer2)
        )
    
    def jouer2(self):
        pass
    
    def traiter(self):
        fenetre = self.fenetre
        continuer = True
        for e in pygame.event.get():
            if e.type == QUIT:
                continuer = False
        bg = pygame.Surface(fenetre.get_size())
        bg.fill((255, 255, 255))
        fenetre.blit(bg, (0, 0))
        bg.blit(self.image, self.rect)
        fenetre.blit(self.image, self.rect)
        if pygame.font:
            font = pygame.font.Font(None, 14)
            version = font.render("Version " + VERSION, 0, (10, 10, 10))
            textpos = version.get_rect(bottomright=fenetre.get_rect().bottomright)
            fenetre.blit(version, textpos)
        self.menu.update()
        self.menu.clear(fenetre, bg)
        self.menu.draw(fenetre)
        pygame.display.flip()
        return continuer
