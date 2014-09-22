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

"""Fichier contenant les utilitaires, fonctions et constantes."""


import os.path
import math
import pygame

LARGEUR = 800
HAUTEUR = 600

dir = os.path.split(os.path.abspath(__file__))[0]
def charger_img(adresse, alpha=True):
    """Charge et convertit une image"""
    adresse = os.path.join(dir, 'ressources', adresse)
    try:
        surface = pygame.image.load(adresse)
    except pygame.error:
        raise SystemExit("Impossible de charger l'image '{}' : {}".format(
                adresse, pygame.get_error()))
    return surface.convert_alpha() if alpha else surface.convert()

def charger_imgs(*adresses):
    """Charge et renvoie une liste d'image"""
    imgs = []
    for adresse in adresses:
        imgs.append(charger_img(adresse))
    return imgs

def ratio_collision(direction):
    """Calcule le ratio de réduction de la zone de collision, en
    fonction de l'angle directionnel.
    Le ratio est minimal pour tous angles multiples de Pi / 2.
    Il vaut 1 pour tous angles multiples de Pi.
    
    """
    return 1 - abs(math.sin(direction * (math.pi / 90)) * 0.25)
