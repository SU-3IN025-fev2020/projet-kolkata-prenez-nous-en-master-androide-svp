'''
Created on 20 mars 2020

@author: Denis
'''

import heapq

def astar(pos_initiale, pos_finale, obstacles):
    """
    Implémente l'algorithme A* et retourne le meilleur chemin pour atteindre
    pos_finale à partir de pos_initiale
    IMPORTANT : à utiliser en conjonction avec la fonction reconstruire_chemin qui 
    est codée juste après
    
    Paramètres:
    pos_initiale, pos_finale : (int, int)
    obstacles : list( (int, int) )
    
    Retour:
    list( (int, int) )
    """
    
    frontiere = []
    reserve = dict()
    chemin = dict()
    
    # pos_initiale est notre point de départ
    # frontiere sera constituée de tuples de la forme (f, position) avec f le coût total pour atteindre position depuis pos_intiale
    # cela permet à heapq de trier tout seul nos positions en fonction de leur f
    heapq.heappush(frontiere, (0, pos_initiale) )
    
    # reserve sert à la fois de réserve et de dictionnaire permettant
    # de stocker les g, reserve[pos] contiendra donc le g de pos
    # pour pos_initiale, on l'initialise alors à 0
    reserve[pos_initiale] = 0
    
    # on boucle tant que frontiere n'est pas vide
    while len(frontiere) > 0:
        
        g, pos_actuelle = heapq.heappop(frontiere)
        
        # si on a trouvé la pos_finale, on peut sortir de la fonction
        if pos_actuelle == pos_finale:
            return reconstruire_chemin(chemin, pos_initiale, pos_finale)
        
        # sinon, on étend les cases voisines
        voisins = [ (pos_actuelle[0], pos_actuelle[1] + 1), 
                  (pos_actuelle[0] + 1, pos_actuelle[1]), 
                  (pos_actuelle[0] - 1, pos_actuelle[1]), 
                  (pos_actuelle[0], pos_actuelle[1] - 1) ]
        
        # on élimine les cases impossibles, ie les obstacles et celles qui sortent de la fenêtre
        voisins_possibles = [ voisins[i] for i in range(len(voisins)) if voisins[i] not in obstacles 
                            and voisins[i][0] >= 0 and voisins[i][0] <= 20 and voisins[i][1] >= 0 and voisins[i][1] <= 20 ]
           
        for voisin in voisins_possibles:
            
            if voisin not in reserve:
                
                # on calcule f pour voisin
                reserve[voisin] = g + 1   
                h = distManhattan(voisin, pos_finale)
                f = h + reserve[voisin]
                
                # et on l'ajoute dans frontiere
                heapq.heappush(frontiere, (f, voisin) )
                
                # on sauvegarde la case par laquelle voisin est accessible
                # cela permettra de reconstruire le vrai chemin plus tard
                chemin[voisin] = pos_actuelle
    
    return reconstruire_chemin(chemin, pos_initiale, pos_finale)


def reconstruire_chemin(chemin, pos_initiale, pos_finale):
    """
    Permet de reconstruire le vrai chemin calculé par l'algo de A*
    
    Paramètres:
    chemin : dict( (int, int) -> (int, int) )
    pos_initiale, pos_finale : (int, int)
    
    Retour:
    list( (int,int) )
    """
    
    # on part de la fin et on rembobine jusqu'au début
    pos_actuelle = pos_finale
    vrai_chemin = []
    
    while pos_actuelle != pos_initiale:
        
        vrai_chemin.insert(0, pos_actuelle)
        # on va chercher la "position parent" de notre pos_actuelle
        pos_actuelle = chemin[pos_actuelle]
    
    vrai_chemin.insert(0, pos_actuelle)
    return vrai_chemin


def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2)
