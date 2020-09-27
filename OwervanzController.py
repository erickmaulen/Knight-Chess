import math
import random as rand
import numpy as np
import copy
from datetime import datetime
from enums import Player

from Node import Node
from State import State

import time

class OwervanzSearchTree:
    def __init__(self, stateDict = None):
        if stateDict is None:
            self.root : Node
        else:
            self.root = Node(State(stateDict), player=Player.PLAYER)

    def timer(self, begin, stop):
        current = time.perf_counter()
        if current-begin >= stop:
            return True
        else:
            return False

    def mcts(self, state = None):
        if state is not None:
            self.root = Node(state)

        begin = time.perf_counter()

        while not self.timer(begin, 1):
            #begin = time.perf_counter()
            current = self.tree_policy(self.root)
            #end = time.perf_counter()
            #print('tree finished in: ', end-begin, " seconds")

            #Simulacion
            #begin = time.perf_counter()
            delta = self.default_policy(current)
            #end = time.perf_counter()
            #print('default finished in: ', end-begin, " seconds")

            #backUp
            #begin = time.perf_counter()
            self.backup(current, delta)
            #end = time.perf_counter()

        bestChild = self.root.best_child()
        keyMovement = list(bestChild.actThatGotMeHere)[0]


        keyPos = self.root.state.myPieces[keyMovement]
        keyMovedTo = [self.root.state.myPieces[keyMovement][0]+bestChild.actThatGotMeHere[keyMovement][0], self.root.state.myPieces[keyMovement][1]+bestChild.actThatGotMeHere[keyMovement][1]]
        
        print(keyMovement, bestChild.actThatGotMeHere[keyMovement])
        print(keyPos, keyMovedTo)

        print(self.root.state.state)
        print(bestChild.state.state)

        print(bestChild.state.state[keyMovedTo[0]][keyMovedTo[1]])

        return bestChild.actThatGotMeHere

        
    def default_policy(self, node: Node) -> int:
        state = node.state

        player = node.currentPlayer

        while not state.isFinalState():
            actions = state.get_actions(player=player)
            if len(actions) <= 0:
                print(actions)
            key = rand.sample(list(actions), 1)[0]
            action = rand.sample(actions[key], 1)[0]

            state = state.transition(
                key, 
                action[0], 
                action[1]
            )

            #print('Player: ', player, ' moves: ', key, action[0], action[1])
            if player == Player.ENEMY:
                player = Player.PLAYER
            else:
                player = Player.ENEMY

        print('defaukl polici')
        return state.reward()

    def tree_policy(self, node: Node) -> Node:
        while not node.state.isFinalState():
            if node.is_fully_expanded():
                node = node.best_child()
            else:
                return node.expand()
        
        return node

    def backup(self, node, delta):
        while node is not None:
            node.visit  += 1
            if node.currentPlayer == Player.ENEMY:
                delta = abs(delta)*-1
            else:
                delta = abs(delta)

            node.winner += node.state.reward() + delta

            node = node.father
            

