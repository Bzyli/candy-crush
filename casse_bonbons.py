from random import randint 
import tkinter as tk #utilisé uniquement pour l'affichage
import re #utilisé uniquement pour l'affichage et de la magie noire
import time

WINDOW = tk.Tk()
GRID = []
SIZE = 8 #taille de la grille
COLORS = ["green", "blue", "yellow", "red", "dark orchid", "orange"] #couleur des bonbons, modifiable avec les noms de couleurs supportées par tkinter
SCORE = 0
COUPS_JOUES = 0

#Partie POO (Programmation Orientée Objet), utilisée pour l'affichage

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
        
        dropped_id = self.get_widget_id(widget) - 1
        dragged_id = self.get_widget_id(DragManager.dragged[0]) - 1
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

        GRID[(self.get_widget_id(widget) - 1 ) // SIZE][(self.get_widget_id(widget) - 1 ) % SIZE] = COLORS.index(dragged_color) + 1
        GRID[(self.get_widget_id(DragManager.dragged[0]) - 1 )//SIZE][(self.get_widget_id(DragManager.dragged[0]) - 1 ) % SIZE] = COLORS.index(dropped_color) + 1
        
        actualise_grille(GRID)


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



#Partie itérative, partie algorithmique

def set_cell_color(row, col, color):
    """
    Permet de changer la couleur d'un des éléments de la grille en prenant en argument les coordonnées x et y
    
    Paramètres:
    ----------
    row : int
        numéro de la ligne, coordonnée x
    col : int
        numéro de la colonne, coordonnée y
    color : str
        nom de la couleur

    Retour:
    -------
    Aucun car modifie directement l'objet dans la grille

    """
    
    focus = f".!canvas{row*SIZE + col + 1}"
    if row*SIZE + col + 1 == 1 :
        focus = ".!canvas"
    for canvas in WINDOW.winfo_children():
        if str(canvas) == focus:
            canvas.itemconfig(canvas.find_withtag("candy")[0] , fill=color)


def init_grid():
    """
    Fonction qui initialise une grille de valeurs aléatoires entre 1 et 6.
    
    Retour:
    -------
    grid : list
        grille qui sera affichée au joueur et contenant une valeur numérique dans chaque case correspondant à une couleur.

    """
    grid=[]
    for i in range(SIZE):
        line=[]
        for j in range(SIZE):
            line.append(randint(1,6))
        grid.append(line)
    return grid

def actualise_grille(grid):
    """
    Fonction qui actualise la grille du jeu après chacun des coups du joueur

    Paramètre:
    ----------
    grid : list
        grille de jeu après échange de deux bonbons

    Retour:
    -------
    Aucun car modifie directement la grille et ses valeurs

    """
    global COUPS_JOUES #étant en POO on est obligés d'utiliser des variables globales pour conserver leur valeur à chaque coup
    liste_combis = detect_combi(grid,[0,0], [SIZE - 1, SIZE - 1])
    combo = 1
    COUPS_JOUES += 1
    while len(liste_combis) > 0:
        time.sleep(1)
        remplacement_comb(grid, liste_combis)
        update_score(liste_combis, combo, COUPS_JOUES)
        liste_combis = detect_combi(grid,[0,0], [SIZE - 1, SIZE - 1])
        combo += 1
        
def affiche_grille(grid):
    """
    Fonction qui s'occupe de l'affichage de la grille sur notre interface graphique

    Paramètres:
    ----------
    grid : list
        grille de jeu
    
    Retour :
    --------
    Rien, agit sur l'interface graphique
    """
    for i in range(SIZE):
        for j in range(SIZE):
            set_cell_color(i, j, COLORS[grid[i][j] -1])

def remplacement_comb(grid, liste_combis):
    """
    Fonction qui remplace la combinaison dans la grille par les nouveaux bonbons qui tombent du dessus

    Paramètres:
    ----------
    grid : list
        grille de jeu
    liste_combis : list
        liste des coordonées de la combinaison

    Retour:
    -------
    Aucun car agit directement sur la grille et la modifie

    """
    remove_comb(liste_combis, grid)
    guillotiere(grid, liste_combis)
    fill_from_top(grid)
    affiche_grille(grid)


def remove_comb(liste_combis, grille):
    """
    Fonction qui remplace par des 0 toutes les valeurs des cases impliquées dans une combinaison

    Paramètres:
    ----------
    liste_combis : list
        liste des coordonées de la combinaison
    grille : list
        grille de jeu

    Retour:
    -------
    Aucun car modifie directement la grille passée en paramètre

    """
    for indice in range(len(liste_combis)):
        nvliste = liste_combis[indice]
        i = nvliste[0]
        j = nvliste[1]
        grille[i][j] = 0


def fill_from_top(grid):
    """
    Fonction qui remplace les zéros (cases vides) par un chiffre aléatoire entre 1 et 6 correspondant à un nouveau bonbon

    Paramètres:
    ----------
    grid : list
        grille de jeu

    Retour:
    -------
    Aucun car modifie directement la grille passée en paramètre

    """
    for i in range (SIZE):
        for j in range(SIZE):
            if grid[i][j] == 0:
                grid[i][j] = randint(1,6)
                


def guillotiere(grille, liste_coord):#en référence à une célèbre place forte lyonnaisle. Cf : https://youtu.be/QaPeaDvNFRo
    """
    Fonction qui fait descendre (de police) les bonbons à la place des cases vides afin de faire remonter les cases vides
    
    Paramètres:
    ----------
    liste_coord : list
        liste des coordonées de la combinaison
    grille : list
        grille de jeu

    Retour:
    -------
    Aucun car modifie directement la grille passée en paramètre
    
    
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


def detect_combi(grille,coord_debut,coord_fin):
    """
    Fonction qui permet de détecter les coordonées de toutes les combinaisons entre deux points de la grille, sera toujours utilisée sur la grille en entière car plus simple à implémenter mais permet une optimisation du temps de calcul si utilisé sur une zone précise

    Paramètres:
    ----------
    grille : list
        grille de jeu
    coord_debut : list
        coordonées du coin haut gauche de la zone à vérifier
    coord_fin : list
        coordonées du coin bas droit de la zone à vérifier

    Retour:
    -------
    liste_coord_combis : list
        liste contenant les coordonnées de toutes les cases faisant partie d'une combinaison

    """
    liste_coord_combis = []
    for i in range(coord_debut[0], coord_fin[0] + 1):
        for j in range(coord_debut[1], coord_fin[1] + 1):
            if len(liste_coord_combis) == 0 or [i,j] not in liste_coord_combis:
                if len(detect_coord(grille, i, j)) != 0:
                    liste_coord_combis.extend(detect_coord(grille, i, j))
    return  liste_coord_combis


def detect_voisin(grille,liste_current,liste_bords,liste_traitee,liste_a_traiter):
    """
    Fonction qui déteccte les voisins de la case actuelle et qui renvoie la liste de ces voisins

    Paramètres:
    ----------
    grille : list
        grille de jeu
    liste_current : list
        liste des coordonnées actuelles
    liste_bords : list
        liste permettant de savoir si la case sur laquelle on se trouve est sur un bord
    liste_traitee : list
        liste des coordonnées déjà explorées
    liste_a_traiter : list
        liste des coordonnées à explorer

    Retour:
    -------
    liste_voisins : list
        liste contenant les voisins de la case actuelle et qui ont la même valeur que celle-ci, contient uniquement des cases non visitées ou qui ne sont pas déjà prévues d'être visitées

    """
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
    """
    Fonction qui renvoie la liste des coordonnées d'une possible combinaison autour du bonbon de coordonées x,y
    
    Paramètres:
    ----------
    grille : list
        grille de jeu
    x : int
        coordonnée x de la case autout de laquelle regarder s'il existe une combinaison
    y : int
        coordonnée y de la case autout de laquelle regarder s'il existe une combinaison

    Retour
    -------
    liste_finale : list
        list contenant les coordonnées de la combinaison, vide si aucune combinaison, ou combinaison invalide comme définie dans les règles

    """
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
        for i in range(SIZE): #permet d'assurer qu'il y ait bien au moins une ligne ou une colonne de trois dans la combinaison
            if liste_x.count(i) >= 3:
                liste_finale = liste_traitee
            if liste_y.count(i) >= 3:
                liste_finale = liste_traitee
    return liste_finale


def compte_score(liste_coordonnees):
    """
    Fonction qui calcule le score en fonction de la longueur de la liste des coordonées de la combinaison, utilisant les règles définies dans le rapport/readme

    Paramètre:
    ----------
    liste_coordonnees : list
        liste des coordonées de la combinaison

    Retour:
    -------
    SCORE : int
        nombre correspondant au score pour ce coup/combinaison, variable globale à cause de la contrainte de la POO

    """
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
    """
    Fonction qui permet de mettre à jour le score dans le nom de la fenêtre Tkinter, fait appel à compte_score pour calculer le score

    Paramètres:
    ----------
    liste_coord : list
        liste des coordonées de la combinaison
    combo : int
        nombre de combo effectués
    COUPS_JOUES : int
        nombre de coups totaux effectués

    Retour:
    -------
    Aucun car actualise directement le titre de la fenêtre tkinter

    """
    score = compte_score(liste_coord)
    WINDOW.title(f"Candy Crush| Coups joués : {COUPS_JOUES} | Score : {score}, COMBO : {combo}")


def test_detect_coord():
    """
    Fonction permettant de tester la fonction detect_coord, affiche True dans la console pour chaque test réussi

    Retour:
    -------
   Aucun, que des prints dans la console

    """
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


test_detect_coord() #appel le test de la fonction avant l'exécution du programme principal



def main():
    """
    Programme principal permettant le fonctionnement du programme, ne prend aucune entrée et ne renvoit rien, permet de s'assurer que la grille affichée au joueur ne contient aucune combinaison
    """
    global GRID
    GRID = init_grid()
    liste_combis = detect_combi(GRID,[0,0], [SIZE - 1, SIZE - 1])
    while len(liste_combis) > 0:
        remplacement_comb(GRID, liste_combis)
        liste_combis = detect_combi(GRID,[0,0], [SIZE - 1, SIZE - 1])
    gui = Gui(WINDOW, SIZE, GRID)
    WINDOW.mainloop()
    
if __name__ == "__main__":
    main()
