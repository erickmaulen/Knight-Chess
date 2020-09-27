import math
import random as rand
import numpy as np
import copy
from datetime import datetime
from enums import Player
import logging

possibleMovements =[
    [1,2],
    [2,1],
    [2,-1],
    [1,-2],
    [-1,-2],
    [-2,-1],
    [-2,1],
    [-1,2]
]


class State:
    def __init__(self, jsonState: dict, myPiecesCount=None, enemyPiecesCount=None, myPlayer=Player.PLAYERONE):
        try:
            self.state = np.array(jsonState['ids'])
            #CAMBIAMOS LOS NONE POR ZEROS Y CAMBIAMOS EL TIPO A INT!
            self.state[self.state == None] = 0
            self.state = self.state.astype(int)

            self.myPieces = jsonState['my_knights_dict']
            self.enemyPieces = jsonState['enemy_knights_dict']

            self.myPlayer = myPlayer

            if myPiecesCount is None:
                self.myPiecesCount = len(self.myPieces)
            else:
                self.myPiecesCount = myPiecesCount
            
            if enemyPiecesCount is None:
                self.enemyPiecesCount = len(self.enemyPieces)
            else:
                self.enemyPiecesCount = enemyPiecesCount


        except Exception as e:
            print('THERE WAS AN ERROR WITH THE JSON FOR SOME REASON XD')
            print(e)

    def __repr__(self):
        return self.state

    ''' 
        get_actions:
            devolverá un arreglo con las posibles 
            acciones a partir de un estado.
            Lo que retornará sera:
                [x,y] donde x será una suma/resta para los lados
                      e y será una suma/resta para arriba/abajo  
    '''
    def get_actions(self, player, filter=None):
        actions = dict()

        if player == self.myPlayer: 
            enemy = Player.PLAYERTWO.value if self.myPlayer == Player.PLAYERONE else Player.PLAYERONE.value
            piecesDict = self.myPieces
        else:
            enemy = Player.PLAYERONE.value if self.myPlayer == Player.PLAYERONE else Player.PLAYERTWO.value
            piecesDict = self.enemyPieces


        for key in piecesDict:
            pos = piecesDict[key]

            #First, check which actions are possible.
            #Vertical Movements
            for movement in possibleMovements:
                # Calculate the Movements
                x = pos[1] + movement[0]
                y = pos[0] + movement[1]

                if (((x < 8 ) and (x >= 0)) and ((y < 8 ) and (y >= 0)) and 
                ((self.state[x][y] < enemy+100 and self.state[x][y] >= enemy))):
                    #Se puede colocar, lo anadimos a la lista.
                    if key not in actions:
                        actions[key] = []
                    elif filter is not None and len(filter) > 0:
                        #This means we got actions to avoid
                        if key in filter and [x,y] in filter[key]:
                            #la accion esta en el filtro
                            continue    
                    actions[key].append([movement[0],movement[1]]) # Agregamos la suma xd, poner x,y si es la pos
        

        if len(actions) == 0:
            for key in piecesDict:
                pos = piecesDict[key]

                #First, check which actions are possible.
                #Vertical Movements
                for movement in possibleMovements:
                    # Calculate the Movements
                    x = pos[1] + movement[0]
                    y = pos[0] + movement[1]
                    
                    if (((x < 8 ) and (x >= 0)) and ((y < 8 ) and (y >= 0)) and 
                    ((self.state[x][y] == 0))):
                        #Se puede colocar, lo anadimos a la lista.
                        if key not in actions:
                            actions[key] = []
                        elif filter is not None and len(filter) > 0:
                            #This means we got actions to avoid
                            if key in filter and [x,y] in filter[key]:
                                #la accion esta en el filtro
                                continue    
                        actions[key].append([movement[0],movement[1]]) # Agregamos la suma xd, poner x,y si es la pos

        return actions


    def transition(self, piece, destx, desty):

        enemy = Player.PLAYERTWO if self.myPlayer == Player.PLAYERONE else Player.PLAYERONE
        
        if int(piece) >= self.myPlayer.value and int(piece) < self.myPlayer.value+100:
            srcPos = self.myPieces[piece]
        else:
            srcPos = self.enemyPieces[piece]

        destPos = [(srcPos[1]+destx), (srcPos[0]+desty)]

        newState = np.array(self.state, copy=True)
        newState[srcPos[1]][srcPos[0]] = 0
        newState[destPos[0]][destPos[1]] = int(piece)

        newMyPieces = {}
        newMyPiecesCount = 0
        newEnemyPieces = {}
        newEnemyPiecesCount = 0

        for i in range(newState.shape[0]):
            for j in range(newState.shape[1]):
                value = newState[i][j]
                if value > 0:
                    if value >= enemy.value and value < enemy.value+100 : #Enemy's
                        newEnemyPieces[str(value)] = [j,i]
                        newEnemyPiecesCount += 1
                    else: #Mines
                        newMyPieces[str(value)] = [j,i]
                        newMyPiecesCount += 1

        asDictAll = {
            'ids':newState,
            'my_knights_dict':newMyPieces,
            'enemy_knights_dict':newEnemyPieces
        }

        return State(asDictAll, myPiecesCount=newMyPiecesCount, enemyPiecesCount=newEnemyPiecesCount, myPlayer=self.myPlayer)


    def isFinalState(self) -> bool:
        if self.enemyPiecesCount == 0 or self.myPiecesCount == 0:
            return True
        return False

    def reward(self, player=Player.PLAYERONE) -> int:
        #Who Won
        if self.enemyPiecesCount == 0 and self.myPiecesCount > 0:
            return 1
        elif self.enemyPiecesCount > 0 and self.myPiecesCount == 0:
            return -1
        
        
        rewardMatrix = np.array(
            [
                [-50,-40,-30,-30,-30,-30,-40,-50],
                [-40,-20,  0,  0,  0,  0,-20,-40],
                [-30,  0, 10, 15, 15, 10,  0,-30],
                [-30,  5, 15, 20, 20, 15,  5,-30],
                [-30,  0, 15, 20, 20, 15,  0,-30],
                [-30,  5, 10, 15, 15, 10,  5,-30],
                [-40,-20,  0,  5,  5,  0,-20,-40],
                [-50,-40,-30,-30,-30,-30,-40,-50]
            ]
        )

        totalReward = 0
        for piece in self.myPieces:
            pos = self.myPieces[piece]
            totalReward += rewardMatrix[pos[0]][pos[1]] * 0.002

        for piece in self.enemyPieces:
            pos = self.enemyPieces[piece]
            totalReward += rewardMatrix[pos[0]][pos[1]]*-0.002


        totalReward += (self.myPiecesCount - self.enemyPiecesCount) 
        
        return totalReward