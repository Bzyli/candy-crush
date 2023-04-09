import tkinter as tk
import random
import re

window = tk.Tk()
g = [[3, 1, 2, 4, 3, 4, 2, 4, 1],[1, 2, 2, 1, 3, 3, 3, 5, 6],[1, 3, 2, 3, 4, 1, 1, 3, 4],[2, 3, 1, 2, 3, 4, 1, 1, 4],[1, 3, 3, 2, 3, 3, 4, 1, 1],[1, 2, 4, 4, 4, 3, 1, 4, 3],[4, 4, 4, 4, 2, 2, 3, 4, 2],[4, 2, 4, 3, 2, 1, 3, 4, 2],[1, 3, 4, 2, 2, 2, 2, 2, 2]]
color = ["green", "blue", "yellow", "red", "purple", "brown"]
score = 0

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
        if self.get_widget_id(widget) != (self.get_widget_id(DragManager.dragged[0]) - 9) and self.get_widget_id(widget) != (self.get_widget_id(DragManager.dragged[0]) +9) and (self.get_widget_id(widget) != self.get_widget_id(DragManager.dragged[0]) -1) and self.get_widget_id(widget) != (self.get_widget_id(DragManager.dragged[0]) + 1) :
            print("La case doit être échangé avec une case adjacente")
            return

        set_cell_color(dropped_id//9, dropped_id%9, dragged_color)
        set_cell_color(dragged_id//9, dragged_id%9, dropped_color)
        
        # Bon là j'ai un peu abusé, notre grille est un tableau 2D 
        # mais les identifiants sont en 1D (ils augmentent de 1 en 1). Donc on procède de la manière suivante :   
        # Je prend le quotient de la division euclienne pour connaitre la ligne (-1 pour les indices)
        # Je prends ensuite le reste pour connaitre la colonne (toujours -1)
        # Je modifie ensuite ces valeurs dans la grille pour que ça corresponde à la bonne couleur
        g[(self.get_widget_id(widget)-1 )//9][(self.get_widget_id(widget)-1 )%9] = color.index(dragged_color) + 1
        g[(self.get_widget_id(DragManager.dragged[0])-1 )//9][(self.get_widget_id(DragManager.dragged[0])-1 )%9] = color.index(dropped_color) + 1

    def get_widget_id(self, widget):
        """
        Cette fonction permet de récupérer le vrai nom d'un bonbon (un numéro entre 1 et 81).
        Argument : widget contenant le bonbon
        Retourne : l'ID du bonbon correspondant
        Fonctionnement :
            On utilise ce qui s'appelle un regex, un truc magique qui permet de cherche des choses dans des chaines de caractères. Ici, on cherche un numéro dans le nom. Or, ça le renvoie sous forme d'une liste de chaine de caractère qui réponde aux conditions définies dans le regex donc on utilise ensuite le list(map(int, l)) pour reconvertir tout ça en entier propres :D
            On retourne ensuite le premier element de la liste ou 1 si cette liste est vie
        """
        id = list(map(int, re.findall(r'\d+', str(widget))))
        return id[0] if id != [] else 1 

class Gui:
    """
    Gestion de l'interface graphique
    """
    def __init__(self, window, size, grid):
        # Intensive grid generation here
        window.title(f"Omg candy crush V4 | Score : {score}")

        for i in range(size):
            window.columnconfigure(i, weight=1, minsize=75)
            window.rowconfigure(i, weight=1, minsize=75) #Creation d'une grille de la bonne taille

            for j in range(size):
                frame = tk.Canvas(master=window,relief=tk.RAISED,borderwidth=0,width=110,height=110) # Dans chaque case, on ajoute une bonbon qui peut être déplacé
                a = DragManager(frame)
                frame.grid(row=i, column=j, padx=5, pady=5)
                c = frame.create_oval(0,0,55,55, fill=color[grid[i][j]-1], tags="candy")

def set_cell_color(row, col, color):
    """
    Permet de changer la couleur d'un des éléments de la grille en prenant en argument les coordonnées x et y
    """
    focus = f".!canvas{row*9 + col}"
    if row*9 + col == 1 :
        focus = ".!canvas"
    for canvas in window.winfo_children():
        if str(canvas) == focus:
            canvas.itemconfig(canvas.find_withtag("candy")[0] , fill=color)

def update_score(new):
    score = new
    window.title(f"Candy Crush| Score : {score}")

gui = Gui(window, 9, g)
window.mainloop()
