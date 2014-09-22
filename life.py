# -*- coding:Utf-8 -*-

# Jeu de la vie

from random import random
from tkinter import *

LARG = 400
HAUT = 400

grille = [[0] * LARG for i in range(HAUT)]
it = 0

def boucler(grille):
    maj = [list(li) for li in grille]
    for y in range(HAUT):
        for x in range(LARG):
            maj[y][x] = destin(x, y, grille)
    return maj

def destin(x, y, grille):
    """Fonction principale, condition de vie ou de mort"""
    voisins = []
    if y != 0:
        if x != LARG-1:
            voisins.append(grille[y-1][x+1]) # ymin xmax
        if x != 0:
            voisins.append(grille[y-1][x-1]) # ymin xmin
        voisins.append(grille[y-1][x])       # ymin
    if y != HAUT-1:
        if x != LARG-1:
            voisins.append(grille[y+1][x+1]) # ymax xmax
        if x != 0:
            voisins.append(grille[y+1][x-1]) # ymax xmin
        voisins.append(grille[y+1][x])       # ymax
    if x != LARG-1:
        voisins.append(grille[y][x+1])       #      xmax
    if x != 0:
        voisins.append(grille[y][x-1])       #      xmin
    if voisins.count(1) == 3:
        return 1
    elif voisins.count(1) == 2:
        return grille[y][x]
    else:
        return 0

# VERSION CONSOLE #######################################################
# def afficher(grille):
    # ret = "_|"
    # for i in range(LARG):
        # ret += str(i).ljust(2)
    # ret += "\n"
    # for y in range(HAUT):
        # ret += str(y).ljust(2)
        # for x in range(LARG):
            # ret += "o " if grille[y][x] else "  "
        # ret += "\n"
    # print(ret)

# print("----- Jeu de la vie -----")
# afficher(grille)
# entree = input(">>> ")
# while entree != "/quit":
    # if entree.startswith("/life"):    # fait naître une cellule
        # x, y = (int(i) for i in entree.split()[1:])
        # grille[y][x] = 1
    # elif entree.startswith("/dest"):  # calcule le destin d'une cellule
        # x, y = (int(i) for i in entree.split()[1:])
        # print(destin(x, y, grille))
    # elif entree.startswith("/rand"):  # randomise la grille selon un coeff <= 1
        # dens = float(entree.split()[1])
        # for y in range(HAUT):
            # for x in range(LARG):
                # grille[y][x] = 1 if random() < dens else 0
    # elif entree.startswith("/reset"): # réinitialise la grille
        # grille = [[0] * LARG for i in range(HAUT)]
        # it = 0
    # else:                             # entrée pour faire avancer le temps
        # grille = boucler(grille)
        # it += 1
    # print("Itération " + str(it))
    # afficher(grille)
    # entree = input(">>> ")

# VERSION FENETREE ######################################################
lance = False
def randomiser(grille=grille):
    for y in range(HAUT):
        for x in range(LARG):
            grille[y][x] = 1 if random() < 0.3 else 0
def lancer():
    global lance
    lance = not lance
    if lance:
        iterer()
def iterer(grille=grille):
    global lance
    print(canevas)
    canevas.delete(ALL)
    maj = [list(li) for li in grille]
    for y in range(HAUT):
        for x in range(LARG):
            vie = destin(x, y, grille)
            if vie:
                canevas.create_line(x, y, x+1, y+1, fill="blue")
            maj[y][x] = vie
    grille = maj
    if lance:
        fenetre.after(500, iterer)

fenetre = Tk()
fenetre.title("Jeu de la Vie")
canevas = Canvas(fenetre, bg="white", height=400, width=400)
canevas.pack(side=LEFT)
print(canevas)
b_quit = Button(fenetre, text="Quitter", command=fenetre.quit)
b_quit.pack(side=BOTTOM)
b_iter = Button(fenetre, text="Itérer/Stoper", command=lancer).pack()
b_rand = Button(fenetre, text="Randomiser", command=randomiser).pack()
fenetre.mainloop()
fenetre.destroy()
