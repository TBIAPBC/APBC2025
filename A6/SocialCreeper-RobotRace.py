#!/usr/bin/env python3

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

#my pseudo graph
class MyMap():
    def __init__(self, map_atr, pos):
        self.map_atr = map_atr
        self.pos = pos
        self.gold = (0,0)
        self.me = (0,0)
        self.Up = (0,0)
        self.Right = (0,0)
        self.Down = (0,0)
        self.Left = (0,0)
        self.DnLeft = (0,0)
        self.DnRight = (0,0)
        self.UpLeft = (0,0)
        self.UpRight = (0,0)
        self.tileValue = 9999999
        self.path = 999999999
        self.prevN = (0,0)
        self.move = D.up


class Creep(Player):
	def reset(self, player_id, max_players, width, height):
	    self.player_name = "Creep"
	    self.moves = [D.up, D.left, D.down, D.right, D.up_left, D.down_left, D.down_right, D.up_right]

	def round_begin(self, r):
		pass


	def set_mines(self, status):
		raise NotImplementedError("'setting mines' not implemented in '%s'." % self.__class__)
	
	
	def move(self, status):
	    me = (status.x, status.y)
	    the_map = []
	    move = []
	    
	    #dictonary for the moves
	    dic_move = {(0,1):D.up, (-1,0):D.left, (0,-1):D.down, (1,0):D.right,  (-1,1):D.up_left, (-1,-1):D.down_left, (1,-1):D.down_right, (1,1):D.up_right}

	    #position of the gold
	    for n in status.goldPots.keys():
	        gldPot = n
	    
	    #traversing the map
	    for x in range(status.map.width):
	        for y in range(status.map.height):
	            #wall are not added to my list
	            if(status.map[x,y].status == TileStatus.Wall):
	                continue
	            the_map.append(MyMap(status.map[x,y],(x, y)))
	            #values for each tile
	            if(the_map[-1].map_atr.status == TileStatus.Empty):
	                the_map[-1].tileValue = 1
	            if(the_map[-1].map_atr.status == TileStatus.Unknown):
	                the_map[-1].tileValue = 50
	            #my own position
	            if((x,y) == me):
	                the_map[-1].me = me
	                
        #my function to calculate the path
	    move = (pathSeeker(the_map, dic_move, me, gldPot))
	    #my function to extract the moves
	    move = Mover(move, gldPot, me)
        
        #returning the first 5 moves 
	    return move[:5]

def Mover(vis, gldPot, me):
    moves = []
    path = 99999999
    to_go = (0,0)
    counter = 0
    
    #extraction tho moves from the visited liste
    for n in vis[:]:
        if n.pos == gldPot:
            path = n.path
            moves.append(n.move)
            to_go = n.prevN
            vis.remove(n)
            while(to_go != me):
                for nodes in vis[:]:
                    if to_go == nodes.pos:
                        to_go = nodes.prevN
                        path = nodes.path
                        moves.insert(0, nodes.move)
                        vis.remove(nodes)
                        break
            break
            
    return moves



def pathSeeker(graph, dic_move, me, gldPot):
    move = []
    unVis = []
    Vis = []
    Layer1 = []
    Layer2 = []
    
    #added my own postion to visiter and setting the path to 0
    for positions in graph:
        if(positions.me == me):
            positions.path = 0
            Vis.append(positions)
        unVis.append(positions)
    
    #My own BFS algo for the path calculation
    while(len(unVis) != 0):
        if(len(Vis) == 1):
            Layer1.append(Vis[0])
        
        for L1 in Layer1:
            for L2 in unVis[:]:
                if(L1.pos[0] == L2.pos[0] and L1.pos[1]+1 == L2.pos[1]):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((0,1))
                    L2.path = L1.path + L2.tileValue
                    Layer2.append(L2)
                    unVis.remove(L2)
                if(L1.pos[0]+1 == L2.pos[0] and L1.pos[1] == L2.pos[1]):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((1,0))
                    L2.path = L1.path + L2.tileValue                    
                    Layer2.append(L2)
                    unVis.remove(L2)                
                if(L1.pos[0]-1 == L2.pos[0] and L1.pos[1] == L2.pos[1]):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((-1,0))
                    L2.path = L1.path + L2.tileValue                    
                    Layer2.append(L2)
                    unVis.remove(L2)                
                if(L1.pos[0] == L2.pos[0] and L1.pos[1]-1 == L2.pos[1]):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((0,-1))
                    L2.path = L1.path + L2.tileValue                    
                    Layer2.append(L2)
                    unVis.remove(L2)                
                if(L1.pos[0]+1 == L2.pos[0] and L1.pos[1]+1 == L2.pos[1]):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((1,1))
                    L2.path = L1.path + L2.tileValue + 0.5
                    Layer2.append(L2)
                    unVis.remove(L2)                
                if(L1.pos[0]+1 == L2.pos[0] and L1.pos[1]-1 == L2.pos[1]):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((1,-1))
                    L2.path = L1.path + L2.tileValue + 0.5                    
                    Layer2.append(L2)
                    unVis.remove(L2)                
                if(L1.pos[0]-1 == L2.pos[0] and L1.pos[1]+1 == L2.pos[1]):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((-1,1))
                    L2.path = L1.path + L2.tileValue + 0.5                    
                    Layer2.append(L2)
                    unVis.remove(L2)                
                if(L1.pos[0]-1 == L2.pos[0] and L1.pos[1]-1 == L2.pos[1]):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((-1,-1))
                    L2.path = L1.path + L2.tileValue + 0.5                    
                    Layer2.append(L2)
                    unVis.remove(L2)                    
        
        for L1 in Layer1:
            for L2 in Layer2:
                if(L1.pos[0] == L2.pos[0] and L1.pos[1]+1 == L2.pos[1] and L2.path > L1.path + L2.tileValue):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((0,1))
                    L2.path = L1.path + L2.tileValue
                if(L1.pos[0]+1 == L2.pos[0] and L1.pos[1] == L2.pos[1] and L2.path > L1.path + L2.tileValue):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((1,0))
                    L2.path = L1.path + L2.tileValue
                if(L1.pos[0]-1 == L2.pos[0] and L1.pos[1] == L2.pos[1] and L2.path > L1.path + L2.tileValue):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((-1,0))
                    L2.path = L1.path + L2.tileValue
                if(L1.pos[0] == L2.pos[0] and L1.pos[1]-1 == L2.pos[1] and L2.path > L1.path + L2.tileValue):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((0,-1))
                    L2.path = L1.path + L2.tileValue
                if(L1.pos[0]+1 == L2.pos[0] and L1.pos[1]+1 == L2.pos[1] and L2.path > L1.path + L2.tileValue):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((1,1))
                    L2.path = L1.path + L2.tileValue + 0.5
                if(L1.pos[0]+1 == L2.pos[0] and L1.pos[1]-1 == L2.pos[1] and L2.path > L1.path + L2.tileValue):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((1,-1))
                    L2.path = L1.path + L2.tileValue + 0.5
                if(L1.pos[0]-1 == L2.pos[0] and L1.pos[1]+1 == L2.pos[1] and L2.path > L1.path + L2.tileValue):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((-1,1))
                    L2.path = L1.path + L2.tileValue + 0.5
                if(L1.pos[0]-1 == L2.pos[0] and L1.pos[1]-1 == L2.pos[1] and L2.path > L1.path + L2.tileValue):
                    L2.prevN = L1.pos
                    L2.move = dic_move.get((-1,-1))
                    L2.path = L1.path + L2.tileValue + 0.5
        
        
        for n in Layer1:
            Vis.append(n)
        
        Layer1.clear()
        for n in Layer2:
            Layer1.append(n)
        
        Layer2.clear()
        
    return Vis




players = [Creep()]
