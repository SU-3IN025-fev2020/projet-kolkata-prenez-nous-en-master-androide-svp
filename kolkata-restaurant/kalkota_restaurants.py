# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys
import astar
import strat1
import strat2


    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 20 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates] 
    
    #-------------------------------
    # initialisation des gains
    #-------------------------------
    gains=[0]*nbPlayers
    

    for i in range(iterations):
    
    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------
        posPlayers = initStates

    
        for j in range(nbPlayers):
            x,y = random.choice(allowedStates)
            players[j].set_rowcol(x,y)
            game.mainiteration()
            posPlayers[j]=(x,y)
        
        
        #-------------------------------
        # chaque joueur choisit un restaurant
        #-------------------------------

        #restau=strat1.choixResto(nbPlayers,nbRestaus)
        restau=strat2.choixResto(nbPlayers,nbRestaus,iterations)
        remplissage=[0]*nbRestaus
       

        
        
        
        #-------------------------------
        # Boucle principale de déplacements 
        #-------------------------------
    
        enRoute=[-1]*nbPlayers
        while -1 in enRoute:
            for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
                if(enRoute[j]==-1):
                
                    row,col = posPlayers[j]

                    #x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
                    
                    #creation du chemin avec A*
                    
                    chemin=astar.astar(posPlayers[j],goalStates[restau[j]],wallStates)
                    if(len(chemin)>1):
                        x_inc,y_inc = chemin[1]
                    else:
                        x_inc,y_inc=posPlayers[j]
                    
                    
                    next_row = x_inc
                    next_col = y_inc
                    #next_row = row+x_inc
                    #next_col = col+y_inc
                    # and ((next_row,next_col) not in posPlayers)
                    if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                        players[j].set_rowcol(next_row,next_col)
                        print ("pos :", j, next_row,next_col)
                        game.mainiteration()
            
                        col=next_col
                        row=next_row
                        posPlayers[j]=(row,col)
                    
              
                
                    
                    # si on est à l'emplacement d'un restaurant, on s'arrête
                    if (row,col) == goalStates[restau[j]]:
                        #o = players[j].ramasse(game.layers)
                        game.mainiteration()
                        enRoute[j]=restau[j]
                        print ("Le joueur ", j, " est à son restaurant.")
                        remplissage[restau[j]]+=1
                        print ("Le restaurant ", restau[j], " compte ", remplissage[restau[j]]," clients.")
                        #goalStates.remove((row,col)) # on enlève ce goalState de la liste
                        
                        #break
        #-------------------------------
        # FIN Boucle principale de déplacements 
        #-------------------------------                 
        
        for rem in range(len(remplissage)):
            if(remplissage[rem]==0):
                pass
            elif(remplissage[rem]==1):
                for jou in range(len(enRoute)):
                    if(enRoute[jou]==rem):
                        gains[jou]+=1
            else:
                tabClients=[]
                for jou in range(len(enRoute)):
                    if(enRoute[jou]==rem):
                        tabClients.append(jou)
                clientContent=random.choice(tabClients)
                gains[clientContent]+=1
        print ("gains : ", gains)
        print ("frequentation : ", remplissage)        
                    
    
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


