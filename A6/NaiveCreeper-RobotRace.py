#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player


class NaiveCreep(Player):
    #where simple naive player, gets stuck by chance, but doesn't run into walls
	def reset(self, player_id, max_players, width, height):
	    self.player_name = "CreepMeep"
	    self.moves = [D.up, D.left, D.down, D.right, D.up_left, D.down_left, D.down_right, D.up_right]
	    
	def round_begin(self, r):
		pass


	def set_mines(self, status):
	
		
		raise NotImplementedError("'setting mines' not implemented in '%s'." % self.__class__)
	
	
	def move(self, status):
	    my_sigth = []
	    move = []
	    meme = (0,0)
	    dic_move = {(0,1):D.up, (-1,0):D.left, (0,-1):D.down, (1,0):D.right,  (-1,1):D.up_left, (-1,-1):D.down_left, (1,-1):D.down_right, (1,1):D.up_right}
	    pos_x = 0 
	    pos_y = 0
	    
	    #get all the Tiles within one step reach
	    for x in range(status.x-1,status.x+2):
	        for y in range(status.y-1,status.y+2):
	            #try function if player starts an edge or corner
	            try:
	                #check with they are a wall or not, when not add them
	                if(status.map[x,y].status != TileStatus.Wall and (x != 0 and y != 0)):
	                    pos_y = y-status.y
	                    pos_x = x-status.x
	                    my_sigth.append((pos_x,pos_y))
	            except:
	                continue
	    #don't know why, but own position(0,0) is added, although I have an exception in the if function 
	    if meme in my_sigth:
	        my_sigth.remove(meme)
	    
	    #one random direction is chosen an from the dictonary put into the move list
	    move.append(dic_move.get(my_sigth[random.randint(0, (len(my_sigth)-1))]))
	    
	    return move


players = [NaiveCreep()]
