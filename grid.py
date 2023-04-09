# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:28:58 2023

@author: gabch
"""

from random import randint

def init_grid():
    """initialise une grille de valeurs entre 1 et 4."""
    liste2D=[]
    for i in range(9):
        line=[]
        for j in range(9):
            line.append(randint(1,4))
        liste2D.append(line)
    return liste2D


def fill_from_top(g):
    """Remplace les cases vides de la première ligne par de nouvelles valeurs"""
    for i in range (len(g[1])):
        if g[0][i] == 0:
            g[0][i] = randint(1,4)

def affichage_monde(g):
    """Affiche la grille"""
    for i in range(len(g)):
        print(g[i])
        