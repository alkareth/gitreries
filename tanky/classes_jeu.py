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

"""Fichier contenant les classes de jeu, qui représentent les objets
physiques du jeu (tank, obus).

"""


import os.path
from math import cos, sin, radians
import pygame

from fonctions import charger_img

class Tank(pygame.sprite.Sprite):
    
    """Classe représentant le tank d'un joueur"""
    def __init__(self, images):
        """Constructeur du tank"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.direction = 180 # direction en degrés (0° = sud)
        self.vitesse = 5
        self.vitesse_angulaire = 3
        self.recharge = 0 # temps de recharge
        self.sante = 3
        self.images = images
        self.image = images[0]
        self.iflag = 0
        self.rect = self.image.get_rect()
    
    def bouger(self, arriere=False):
        """Fait avancer ou reculer le tank"""
        v = int(self.vitesse / 2) if arriere else self.vitesse
        a = radians(self.direction + 180) if arriere else radians(
                self.direction)
        self.rect.move_ip(v * sin(a), v * cos(a))
        if self.iflag == 0:
            self.image = self.images[1]
            self.iflag = 1
        else:
            self.image = self.images[0]
            self.iflag = 0
        self.image = pygame.transform.rotate(self.image, self.direction - 180)
    
    def tourner(self, sens):
        """Effectue une rotation"""
        center = self.rect.center
        rot = sens * self.vitesse_angulaire
        self.direction += rot
        self.direction %= 360
        self.rect = self.image.get_rect(center=center)
    
    def update(self):
        """Exécute les actions nécessaires à chaque tour de boucle"""
        if self.recharge > 0:
            self.recharge -= 1

class Obus(pygame.sprite.Sprite):
    
    """Classe représentant un obus tiré par un tank"""
    def __init__(self, tank):
        """Constructeur de l'obus"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.tank = tank
        self.direction = tank.direction
        self.vitesse = 10
        self.reste = 50
        self.image = charger_img("obus.png")
        self.image = pygame.transform.rotate(self.image, self.direction)
        self.rect = self.image.get_rect(center=tank.rect.center)
    
    def update(self):
        """Fait avancer l'obus à chaque tour de boucle"""
        v = self.vitesse
        a = radians(self.direction)
        self.rect.move_ip(v * sin(a), v * cos(a))
        if self.reste:
            self.reste -= 1
        else:
            Explosion(self)
            self.kill()

class Explosion(pygame.sprite.Sprite):
    
    """Classe représentant l'explosion due à un obus"""
    def __init__(self, obus):
        """Constructeur de l'explosion"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.obus = obus
        self.images = [charger_img(os.path.join("explo",
                "explo" + str(i+1) + ".png")) for i in range(9)]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=obus.rect.center)
    
    def update(self):
        """Anime l'explosion"""
        if self.images:
            self.image = self.images.pop(0)
        else:
            self.kill()
