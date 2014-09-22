#!usr/bin/python
# -*- coding=Utf-8 -*-

import math

class Vecteur:
    """Classe représentant un vecteur de dimension finie n"""
    
    def __init__(self, *coords):
        """Constructeur de la classe"""
        self.coords = coords
    
    def __repr__(self):
        """Affiche le vecteur proprement"""
        return "(" + ", ".join([str(c) for c in self.coords]) + ")"
    
    def __getitem__(self, i):
        return self.coords[i]
    def __setitem__(self, i, a):
        self.coords[i] = a
    
    def __len__(self):
        """Dimension d'un vecteur"""
        return len(self.coords)
    
    def __rmul__(self, a):
        """LCE sur le vecteur"""
        coords = [a * c for c in self.coords]
        return Vecteur(*coords)
    
    def __add__(self, vect):
        """Addition de deux vecteurs"""
        coords = [c1 + c2 for c1, c2 in zip(self.coords, vect.coords)]
        return Vecteur(*coords)
    
    def __sub__(self, vect):
        """Soustraction de deux vecteurs"""
        coords = [c1 - c2 for c1, c2 in zip(self.coords, vect.coords)]
        return Vecteur(*coords)
    
    def __or__(self, vect):
        """Produit scalaire de deux vecteurs"""
        prods = [c1 * c2 for c1, c2 in zip(self.coords, vect.coords)]
        return sum(prods)
    
    @property
    def norme(self):
        """Norme du vecteur"""
        return math.sqrt(self | self)

def c_lineaire(scalaires, vecteurs):
    """Renvoie la combinaison linéaire des vecteurs coefficientés"""
    ret = Vecteur(*[0 for c in vecteurs[0].coords])
    for a, v in zip(scalaires, vecteurs):
        plus = a * v
        ret = ret + plus
    return ret

def schmidt(liste):
    """Orthonormalise selon Gram-Schmidt une liste de vecteurs"""
    orthonorm = []
    for i, e in enumerate(liste):
        u = e
        if i > 0:
            for j in range(i):
                u -= (e | orthonorm[j]) * orthonorm[j]
        orthonorm.append((1 / u.norme) * u)
    return orthonorm

def projortho(u, v):
    """Retourne la matrice de la projection orthogonale sur Vect{u, v}
    On commence par orthonormaliser (u, v), puis la projection de x
    sur (u', v') est <x|u'>.u' + <x|v'>.v'. On a donc
    M[i][j] = <p(e_i)|e_j>.
    
    """
    def proj(x, u, v):
        return (x | u) + (x | v)
    u_on, v_on = schmidt([u, v])
    print(u_on, v_on)
    mat = [[0] * 3] * 3
    for i in range(3):
        for j in range(3):
            e_i = Vecteur(*[i if k==(i-1) else 0 for k in range(3)])
            e_j = Vecteur(*[j if k==(j-1) else 0 for k in range(3)])
            mat[i][j] = (proj(e_i, u_on, v_on) | ej)
    return mat
