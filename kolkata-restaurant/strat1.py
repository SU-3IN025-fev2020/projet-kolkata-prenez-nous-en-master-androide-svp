# -*- coding: utf-8 -*-

#Strategie aleatoire

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

def choixResto(nbPlayers,nbRestaus):
    restau=[0]*nbPlayers
    for j in range(nbPlayers):
        c = random.randint(0,nbRestaus-1)
        print(c)
        restau[j]=c
    return restau
        

def move():
    row,col = posPlayers[j]
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
    if (row,col) == restau[j]:
        #o = players[j].ramasse(game.layers)
        game.mainiteration()
        print ("Le joueur ", j, " est à son restaurant.")
        # goalStates.remove((row,col)) # on enlève ce goalState de la liste
        
            
