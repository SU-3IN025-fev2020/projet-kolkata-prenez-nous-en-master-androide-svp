# -*- coding: utf-8 -*-

#meme restau

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

def choixResto(nbPlayers,nbRestaus,iteration,restau):
    if(iteration==0):
        for j in range(nbPlayers):
            c = random.randint(0,nbRestaus-1)
            print(c)
            restau[j]=c
        return restau
    return restau
        
        
