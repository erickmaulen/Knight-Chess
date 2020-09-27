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
    def __init__(self, stateDict = None, player=Player.PLAYERONE):
        if stateDict is None:
            raise Exception("CAN'T INITIALIZE WITHOUT A DICTIONARY!")
        self.root = Node(State(stateDict, myPlayer=player), player=player)

    def mcts(self, state = None):
        if state is not None:
            self.root = Node(state)

        begin = time.perf_counter()

        for i in range(150):
            current = self.tree_policy(self.root)

            #Simulacion
            delta = self.default_policy(current)
            self.backup(current, delta)

        bestChild = self.root.best_child()
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

            if player == Player.PLAYERTWO:
                player = Player.PLAYERONE
            else:
                player = Player.PLAYERONE
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

            node.winner += node.state.reward() + delta

            node = node.father
            

