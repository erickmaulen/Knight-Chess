## THIS IS WHERE THE MAGIC HAPPENS XD ##
import random
import json
from OwervanzController import OwervanzSearchTree
from Node import Node
from State import State
import sys
import logging 


""" 
moveDict = { #dar vuelta valores
    "1,2" : 0,
    "2,1" : 1,
    "2,-1" : 2,
    "1,-2" : 3,
    "-1,-2" : 4,
    "-2,-1" : 5,
    "-2,1" : 6,
    "-1,2" : 7
} 
"""

moveDict = {
    "1,2" : 1,
    "2,1" : 0,
    "1,-2" : 6,
    "-2,1" : 3,
    "2,-1" : 7,
    "-1,2" : 2,
    "-1,-2" : 5,
    "-2,-1" : 4
}


if __name__ == "__main__":
    log = logging.getLogger()

    #jsn = json.loads(sys.argv[1])
    jso = open('caca.json', 'r').read()
    jsn = json.loads(jso)
    #log.warning('CURRENT STATE IS: ', sys.argv[1])

    ovc = OwervanzSearchTree(jsn)

    result = ovc.mcts()

    key = list(result)[0]
    move = str(result[key][0]) + "," + str(result[key][1])

    log.warning('KEY, MOVE: ', key, move)


    action = {
        "knight_id": int(key),
        "knight_movement": moveDict[move]
    }

    print(json.dumps(action))

    del ovc



