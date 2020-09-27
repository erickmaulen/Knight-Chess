import math
import random as rand
import numpy as np
import copy
import heapq as h
from datetime import datetime

from enums import Player

from State import State

class Node:
    def __init__(self, state: State, father=None, action={}, player=Player.PLAYER):
        self.state              = state
        self.triedActions       = dict()
        self.children           = []
        self.visit              = 0
        self.winner             = 0
        self.actThatGotMeHere   = action

        self.uct                = 0
        self.father             = father

        self.currentPlayer      = player

    def __lt__(self, otherNode):
        return self.uct > otherNode.uct

    def __le__(self, otherNode):
        return self.uct >= otherNode.uct

    def __repr__(self):
        return self.state.state

    def is_fully_expanded(self) -> bool:
        possibleActions = self.state.get_actions(self.currentPlayer, filter=self.triedActions)

        return len(possibleActions) <= 0

    def expand(self):
        #rand.seed(datetime.now())
        actions = self.state.get_actions(self.currentPlayer, filter=self.triedActions)
        #First, we randomly select a piece to move
        strPiece = rand.sample(list(actions), 1)[0]
        #We now have the dict string to acces the piece
        randomAction = rand.sample(actions[strPiece], 1)[0]

        #We add the action to the filter dictionary
        #So we avoid selecting it again!
        if strPiece not in self.triedActions:
            self.triedActions[strPiece] = []
        
        if randomAction not in self.triedActions[strPiece]:
            self.triedActions[strPiece].append(randomAction)

        #print(randomAction[0], randomAction[1])

        childNode = Node(state = self.state.transition(
                strPiece, 
                randomAction[0],
                randomAction[1]
            ),
            father = self,
            action = {strPiece:randomAction},
            player = Player.ENEMY if self.currentPlayer == Player.PLAYER else Player.PLAYER
        )

        self.children.append(childNode)

        return childNode


    def best_child(self):
        cont = 0
        bestChild : Node
        bestUCT = -10000000
        
        for child in self.children:
            #Constantes
            c = np.sqrt(2)

            #Variables
            N_v = self.visit
            N_v1 = child.visit
            Q_v = child.winner

            #calculos
            if N_v1 != 0:
                term1 = (Q_v / N_v1)
                term2 = c*(np.sqrt(2*((np.log(N_v))/N_v1)) )

                child.uct = term1+term2
            else:
                child.uct = np.inf
        
            if bestUCT < child.uct:
                bestChild = child
                bestUCT = child.uct

        if bestChild is None:
            return self
        return bestChild

