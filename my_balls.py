# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:36:20 2023

@author: tibol
"""

import tkinter as tk
from random import randint
import re
import time

ALIGNEMENT_AVANCE = True
SIZE = 8
COLORS = ["green", "blue", "yellow", "red", "dark orchid", "orange"]
window = tk.Tk()
SCORE = 0
COUPS_JOUES = 0



class DragManager():
    """
    Classe qui permet de gérer le drag and drop, elle contient 4 méthodes (fonctions)
        - Une qui permet d'activer le glisser déposé
        - Une qui s'active quand on soulève une case
        - Une qui s'active lors du déplacement
        - Une qui s'active à la fin du déplacement
    """
    start_x, start_y = 0,0
    dragged = None

    def __init__(self,widget):
        """
        Nécessaire pour utiliser une classe, pas forcément très important à comprendre
        """
        self.widget = widget
        self.add_dragable(self.widget)
    
    def add_dragable(self, widget):
        """
        Prends en argument un widget (un bonbon) et lui assigne des actions quand on clique dessus
        """
        self.widget = widget
        self.widget.bind("<ButtonPress-1>", self.on_start)
        self.widget.bind("<B1-Motion>", self.on_drag)
        self.widget.bind("<ButtonRelease-1>", self.on_drop)
        self.widget["cursor"] = "hand1"
    
    def on_start(self, event):
        """
        Récupère les coordonnées auxquelles on commence le glissé déposé
        Garde égalment en mémoire quelle élément on déplace
        Le event qui est pris en argument est un évènement provoqué par l'utilisateur, il sera utilisé dans toutes les autres fonctions
        """
        DragManager.start_x, DragManager.start_y = event.widget.winfo_pointerxy() 
        dragged_item = event.widget.find_withtag("current")
        DragManager.dragged = (event.widget, dragged_item)

    def on_drag(self, event):
        """
        Calcul la longeur du déplacement à chaque instant et vérifie que l'on ne va pas trop loin, replace le curseur au bon endroit si on est trop loin
        """
        dx = event.widget.winfo_pointerx() - DragManager.start_x
        dy = event.widget.winfo_pointery() - DragManager.start_y

    def on_drop(self, event):
        """
        Gère le laché après déplacement, trivial.
        Je rigole, je vais expliquer plus enn détail dans la suite du code car c'est plus simple
        """
        widget = event.widget.winfo_containing(event.x_root, event.y_root) 
        candy = widget.find_withtag("candy") # Avec ces deux lignes on récupère l'indice du bonbon sur lequelle on se trouve

        dropped_color = widget.itemcget(candy[0], 'fill')
        dragged_color = DragManager.dragged[0].itemcget(DragManager.dragged[1], "fill") # On garde en mémoire les couleurs des deux bonbons avant modification
        
        dropped_id = self.get_widget_id(widget)
        dragged_id = self.get_widget_id(DragManager.dragged[0])
        # On test ici si le mouvement que le joueur souhaite réalisé est possible ou non. Si il ne l'est pas, on affiche un message dans la console et on quitte la fonction sans faire de modification
        if self.get_widget_id(widget) != (self.get_widget_id(DragManager.dragged[0]) - SIZE) and self.get_widget_id(widget) != (self.get_widget_id(DragManager.dragged[0]) + SIZE) and (self.get_widget_id(widget) != self.get_widget_id(DragManager.dragged[0]) - 1) and self.get_widget_id(widget) != (self.get_widget_id(DragManager.dragged[0]) + 1) :
            print("La case doit être échangé avec une case adjacente")
            return

        set_cell_color(dropped_id//SIZE, dropped_id%SIZE, dragged_color)
        set_cell_color(dragged_id//SIZE, dragged_id%SIZE, dropped_color)
        
        # Bon là j'ai un peu abusé, notre grille est un tableau 2D 
        # mais les identifiants sont en 1D (ils augmentent de 1 en 1). Donc on procède de la manière suivante :   
        # Je prend le quotient de la division euclienne pour connaitre la ligne (-1 pour les indices)
        # Je prends ensuite le reste pour connaitre la colonne (toujours -1)
        # Je modifie ensuite ces valeurs dans la grille pour que ça corresponde à la bonne couleur

        grid[(self.get_widget_id(widget) - 1 ) // SIZE][(self.get_widget_id(widget) - 1 ) % SIZE] = COLORS.index(dragged_color) + 1
        grid[(self.get_widget_id(DragManager.dragged[0]) - 1 )//SIZE][(self.get_widget_id(DragManager.dragged[0]) - 1 ) % SIZE] = COLORS.index(dropped_color) + 1
        
        liste_combis = detect_combi(grid,[0,0], [SIZE - 1, SIZE - 1])
        combo = 1
        global COUPS_JOUES
        COUPS_JOUES += 1
        while len(liste_combis) > 0:
            update_score(liste_combis, combo, COUPS_JOUES)
            remove_comb(liste_combis, grid)
            guillotiere(grid, liste_combis)
            fill_from_top(grid)
            liste_combis = detect_combi(grid,[0,0], [SIZE - 1, SIZE - 1])
            combo += 1
        for i in range(SIZE):
            for j in range(SIZE):
                set_cell_color(i, j, COLORS[grid[i][j] - 1])
                
                

    def get_widget_id(self, widget):
        """
        Cette fonction permet de récupérer le vrai nom d'un bonbon (un numéro entre 1 et 81).
        Argument : widget contenant le bonbon
        Retourne : l'ID du bonbon correspondant
        Fonctionnement :
            On utilise ce qui s'appelle un regex, un truc magique qui permet de chercher des choses dans des chaines de caractères. Ici, on cherche un numéro dans le nom. Or, ça le renvoie sous forme d'une liste de chaine de caractère qui réponde aux conditions définies dans le regex donc on utilise ensuite le list(map(int, l)) pour reconvertir tout ça en entier propre :D
            On retourne ensuite le premier element de la liste ou 1 si cette liste est vide
        """
        iden = list(map(int, re.findall(r'\d+', str(widget))))
        return iden[0] if iden != [] else 1 

class Gui:
    """
    Gestion de l'interface graphique
    """
    def __init__(self, window, size, grid):
        # Intensive grid generation here
        window.title(f"Omg candy crush V4 | Score : {SCORE}")

        for i in range(size):
            window.columnconfigure(i, weight=1, minsize=75)
            window.rowconfigure(i, weight=1, minsize=75) #Creation d'une grille de la bonne taille

            for j in range(size):
                frame = tk.Canvas(master=window,relief=tk.RAISED,borderwidth=0,width=110,height=110) # Dans chaque case, on ajoute une bonbon qui peut être déplacé
                a = DragManager(frame)
                frame.grid(row=i, column=j, padx=5, pady=5)
                c = frame.create_oval(0,0,55,55, fill=COLORS[grid[i][j]-1], tags="candy")

def set_cell_color(row, col, color):
    """
    Permet de changer la couleur d'un des éléments de la grille en prenant en argument les coordonnées x et y
    """
    focus = f".!canvas{row*SIZE + col + 1}"
    if row*SIZE + col + 1 == 1 :
        focus = ".!canvas"
    for canvas in window.winfo_children():
        if str(canvas) == focus:
            canvas.itemconfig(canvas.find_withtag("candy")[0] , fill=color)





def init_grid():
    """initialise une grille de valeurs entre 1 et 4."""
    liste2D=[]
    for i in range(SIZE):
        line=[]
        for j in range(SIZE):
            line.append(randint(1,6))
        liste2D.append(line)
    return liste2D


def remove_comb(liste, grille):
    for i in range(len(liste)):
        nvliste = liste[i]
        i=nvliste[0]
        j=nvliste[1]
        grille[i][j]=0
        set_cell_color(i, j, "snow")
    return grille




def fill_from_top(g):
    """Remplace les cases vides de la première ligne par de nouvelles valeurs"""
    for i in range (SIZE):
        for j in range(SIZE):
            if g[i][j] == 0:
                g[i][j] = randint(1,6)
                


def guillotiere(grille, liste_coord):#en référence à une célèbre place forte lyonnaise
    """
    """
    liste_a_traiter = liste_coord[::-1]
    liste_colonne_0 = []
    while len(liste_a_traiter) != 0:
        current_coords = liste_a_traiter.pop()
        liste_colonne_0.append(current_coords[1])
        for i in range(len(liste_a_traiter)-1,-1,-1):
            if liste_a_traiter[i][1] == current_coords[1]:
                del liste_a_traiter[i]
    while len(liste_colonne_0) != 0:
        colonne = []
        current_colonne = liste_colonne_0.pop()
        for i in range(len(grille)):
            colonne.append(grille[i][current_colonne])
        for j in range(len(colonne)):
            if j == 0 and colonne[j] == 0:  #aucune descente si 0 en haut
                pass
            elif colonne[j] == 0:
                colonne[0], colonne[1:j+1] = 0, colonne[0:j]
        for k in range(len(colonne)):
            grille[k][current_colonne] = colonne[k]
    return grille

def detect_combi(grille,coord_debut,coord_fin):
    liste_coord_combis = []
    liste_intermediaire = []
    for i in range(coord_debut[0], coord_fin[0] + 1):
        for j in range(coord_debut[1], coord_fin[1] + 1):
            if len(liste_coord_combis) == 0 or [i,j] not in liste_coord_combis:
                if len(detect_coord(grille, i, j)) != 0:
                    liste_coord_combis.extend(detect_coord(grille, i, j))
                    liste_intermediaire.append(detect_coord(grille, i, j)[0])
    return  liste_coord_combis

def detect_voisin(grille,liste_current,liste_bords,liste_traitee,liste_a_traiter):
    borne_gauche = -1
    borne_droite = 1
    borne_haute = -1
    borne_basse = 1
    x_case = liste_current[0]
    y_case = liste_current[1]
    liste_voisins = []
    if liste_bords[0] == True:
       borne_gauche = 0
    if liste_bords[1] == True:
        borne_droite = 0
    if liste_bords[2] == True:
       borne_haute = 0
    if liste_bords[3] == True:
        borne_basse = 0
    for i in range(borne_gauche,borne_droite + 1):
        if y_case + i != y_case and grille[x_case][y_case] == grille[x_case][y_case + i]:
            liste_voisins.append([x_case,y_case + i])
    for j in range(borne_haute,borne_basse +1):
            if x_case + j != x_case and grille[x_case][y_case] == grille[x_case + j][y_case]:
                liste_voisins.append([x_case + j,y_case])
    i = 0
    while i  < len(liste_voisins):
        if liste_voisins[i] in liste_traitee:
            del liste_voisins[i]
        elif liste_voisins[i] in liste_a_traiter:
            del liste_voisins[i]
        else:
            i += 1
    return liste_voisins


def detect_coord(grille,x,y):
    liste_a_traiter = [[x,y]]
    liste_traitee =[]
    while len(liste_a_traiter) != 0:
        current_coords = liste_a_traiter.pop()
        bord_gauche = False
        bord_droit = False
        bord_haut = False
        bord_bas = False
        if current_coords[0] == 0 and current_coords[1] == 0:
            bord_gauche = True
            bord_haut = True
        elif current_coords[0] == 0 and current_coords[1] == SIZE - 1:
            bord_haut = True
            bord_droit = True    
        elif current_coords[0] == SIZE - 1 and current_coords[1] == 0:
            bord_bas = True
            bord_gauche = True
        elif current_coords[0] == SIZE - 1 and current_coords[1] == SIZE - 1:
            bord_bas = True
            bord_droit = True
        elif current_coords[0] == 0:
            bord_haut = True
        elif current_coords[1] == 0:
            bord_gauche = True
        elif current_coords[1] == SIZE - 1:
            bord_droit = True
        elif current_coords[0] == SIZE - 1:
            bord_bas = True
        liste_traitee.append(current_coords)
        liste_bords = [bord_gauche,bord_droit,bord_haut,bord_bas]
        liste_voisins = detect_voisin(grille,current_coords,liste_bords,liste_traitee,liste_a_traiter)
        liste_a_traiter += liste_voisins
    if len(liste_traitee) < 3:
        liste_finale = []
    else:
        liste_finale = []
        liste_x = []
        liste_y = []
        for i in range(len(liste_traitee)):
            liste_x.append(liste_traitee[i][0])
            liste_y.append(liste_traitee[i][1])
        for i in range(SIZE):
            if liste_x.count(i) >= 3:
                liste_finale = liste_traitee
            if liste_y.count(i) >= 3:
                liste_finale = liste_traitee
    return liste_finale


"""def compte_score(liste_coordonnees):
    print(liste_coordonnees, "compte_score")
    nb_groupes = len(liste_coordonnees)
    global SCORE
    if nb_groupes < 3 :
        SCORE = SCORE + 0
    elif nb_groupes == 3 :
        SCORE = SCORE + nb_groupes**2 
    elif nb_groupes == 4 :
        SCORE = SCORE + nb_groupes**2+nb_groupes*2
    elif nb_groupes == 5 :
        SCORE = SCORE + nb_groupes**2+nb_groupes*3
    else : 
        SCORE = SCORE + nb_groupes**3
    print(SCORE,"compte_score")
    return SCORE"""

def compte_score(liste_coordonnees):
    for i in range(len(liste_coordonnees)+1):
        global SCORE
        if i < 3 :
            SCORE = SCORE + 0
        elif i < 5 :
            SCORE = SCORE + i
        else : 
            SCORE = SCORE + i**2 + i
    return SCORE


def update_score(liste_coord, combo, COUPS_JOUES):
    score = compte_score(liste_coord)
    window.title(f"Candy Crush| Coups joués : {COUPS_JOUES} | Score : {score}, COMBO : {combo}")


def test_detect_coord():
    # Test 1 : Cas combinaison de bonbons rouges, test en diagonale
    grille1 = [[1,1,1,1,1,1,1,1,1],[4,4,4,4,4,4,4,4,4],[2,2,2,2,3,2,2,2,2],[2,2,2,3,2,3,2,1,1],[4,4,3,3,3,3,3,4,4],[4,4,4,1,1,3,2,2,2],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[1,1,1,1,1,1,1,1,1]]
    
                #créer une grille arbitrairement avec des dispositions intéressantes pour tester la fonction detec_coord, 
                #En gros je crée une grille de jeu avec des 1, 2, 3 et 4, puis je choisis une position c''est-à dire une bille en particulier. 
                #Ensuite, moi je sais la liste de coordonnées qu'elle doit renvoyer
                #(je l'ai fait sur papier par exemple) et je compare le renvoi de la fonction avec les coordonnées que je vais entrer)
    i = 4
    j = 4
    print((detect_coord(grille1, i , j).sort()) == [[3,3],[3,5],[4,2],[4,3],[4,4],[4,5],[4,6],[5,5]].sort())
    
    #Test 2 : Cas aucune combinaison possible avec un bonbon rouge
    grille2 = [[1,3,3,1,1,1,1,1,1],[4,3,4,4,4,4,4,4,4],[2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,1,1],[4,4,4,4,4,4,4,4,4],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[1,1,1,1,1,1,1,1,1]]
   
    i = 0
    j = 1
    print((detect_coord(grille2, i, j)) == [])
    
    # Test 3 : Cas basique 3 bonbons alignés 
    grille3 = [[1,1,1,1,1,1,1,1,1],[4,4,4,4,4,4,4,4,4],[2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,1,1],[4,4,4,3,3,3,4,4,4],[4,4,4,1,1,2,2,2,2],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[3,3,3,3,3,3,3,3,3]]
    
    i = 4
    j = 3
    print((detect_coord(grille3, i, j)) == [[4,3],[4,4],[4,5]])
    
    #Test 4 : Cas bonbon seul
    grille4 = [[1,1,1,1,1,1,1,1,1],[4,3,4,4,4,4,4,4,4],[2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2],[4,4,4,4,4,4,4,4,4],[4,4,4,1,1,2,2,2,2],[4,4,4,1,1,1,2,2,2],[4,4,4,1,1,1,2,2,2],[3,3,3,3,3,3,3,3,3]]
    
    i = 1
    j = 1
    print((detect_coord(grille4, i, j)) == [])
    
test_detect_coord()

#def main():
"""Programme principal permettant le fonctionnement du programme, ne prend aucune entrée et ne renvoit rien"""
grid = init_grid()
liste_combis = detect_combi(grid,[0,0], [SIZE - 1, SIZE - 1])
while len(liste_combis) > 0:
    remove_comb(liste_combis, grid)
    guillotiere(grid, liste_combis)
    fill_from_top(grid)
    liste_combis = detect_combi(grid,[0,0], [SIZE - 1, SIZE - 1])
gui = Gui(window, SIZE, grid)
window.mainloop()
