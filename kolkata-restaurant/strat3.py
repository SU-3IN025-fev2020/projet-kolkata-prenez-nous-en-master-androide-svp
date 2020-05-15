# -*- coding: utf-8 -*-

#restau le plus proche

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

        
def choixResto(nbPlayers,nbRestaus,posPlayers,goalStates,wallStates):
    
    c=None
    restau=[0]*nbPlayers
    for j in range(nbPlayers):
        mini=None
        for r in range(nbRestaus):
            test=astar.astar(posPlayers[j],goalStates[r],wallStates)
            if(mini==None or len(mini)>len(test)):
                mini=test
                c=r          
        print(c)
        restau[j]=c
    return restau
