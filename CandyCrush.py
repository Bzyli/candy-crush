# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:22:45 2023

@author: mendes
"""

def score (liste_coordonnees):
    nb_groupes = len(liste_coordonnees)
    score = nb_groupes**2
    return score 

def affichage_score (score):
    print(score)

def test_detect_coord(grille, i, j):
    # Test 1 : Cas combinaison de bonbons rouges, test en diagonale
    grille1 = [[1,1,1,1,1,1,1,1,1],[4,4,4,4,4,4,4,4,4],[2,2,2,2,3,2,2,2,2],[2,2,2,3,2,3,2,1,1],[4,4,3,3,3,3,3,4,4],[4,4,4,1,1,3,2,2,2],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[1,1,1,1,1,1,1,1,1]]
    
                #créer une grille arbitrairement avec des dispositions intéressantes pour tester la fonction detec_coord, 
                #En gros je crée une grille de jeu avec des 1, 2, 3 et 4, puis je choisis une position c''est-à dire une bille en particulier. 
                #Ensuite, moi je sais la liste de coordonnées qu'elle doit renvoyer
                #(je l'ai fait sur papier par exemple) et je compare le renvoi de la fonction avec les coordonnées que je vais entrer)
    i = 5
    j = 5
    print(detect_coord(grille, i , j)) == [[5,3],[5,4],[4,4],[5,5],[5,6],[5,7],[4,6],[6,6],[5,8]]
    
    #Test 2 : Cas aucune combinaison possible avec un bonbon rouge
    grille2 = [[1,3,3,1,1,1,1,1,1],[4,3,4,4,4,4,4,4,4],[2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,1,1],[4,4,4,4,4,4,4,4,4],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[1,1,1,1,1,1,1,1,1]]
   
    i = 1
    j = 2
    print (detect_coord(grille, i, j)) == []
    
    # Test 3 : Cas basique 3 bonbons alignés 
    grille3 = [[1,1,1,1,1,1,1,1,1],[4,4,4,4,4,4,4,4,4],[2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,1,1],[4,4,4,3,3,3,4,4,4],[4,4,4,1,1,3,2,2,2],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[3,3,3,3,3,3,3,3,3]]
    
    i = 5
    j = 4
    print (detect_coord(grille, i, j)) == [[5,4],[5,5],[5,6]]
    
    #Test 4 : Cas bonbon seul
    grille4 = [[1,1,1,1,1,1,1,1,1],[4,3,4,4,4,4,4,4,4],[2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2],[4,4,4,4,4,4,4,4,4],[4,4,4,1,1,3,2,2,2],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[3,3,3,3,3,3,3,3,3]]
    
    i = 2
    j = 2
    print (detect_coord(grille, i, j)) == []
    
def remove_comb(liste): #récupere la liste de detect combi et remplace par des 0
    for k in range (len(liste)) :
        i = 0
        j = 0
    return liste_vide
    
    