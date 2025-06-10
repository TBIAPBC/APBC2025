import random
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player


class naive_markus(Player):

        #-#-#-#-#- RESET FUNCTION is called at beginning of game to inform about game parameters (map dimension, player ID, ..)        
        def reset(self, player_id, max_players, width, height):
                self.my_id = player_id
                self.player_name = "NaiveMarkus"
                self.max_players = max_players
                self.map_width = width
                self.map_height = height
                self.moves = [D.up, D.left, D.down, D.right, D.up_left, D.down_left, D.down_right, D.up_right]


        def round_begin(self, r):
                pass

        #-#-#-#-#-#- SET-MINE FUNCTION RETURNS LIST OF MINES
        # more information see move function
        def set_mines(self, status: Status):
                return []
        
        #-#-#-#-#-#- MOVE FUNCTION RETURNS LIST OF MOVES
        # Like with set_mines, this function recieves Status from Status-class from game_utils. The instances of Status-class 
        # save information on 
        #       1) player´s position, health ,.. (self.x, self.y, self.gold, self.health)
        #       2) game parameters
        #       3) information on sight and environment. Information derives from simulator.py 
        #       (self.map = visible part of map, self.goldPots = position of goldpot (x, y) in dict.-format)

        def move(self, status: Status):

                if status.goldPots:                
                        gold_pot_coordinates_list = list(status.goldPots.keys())
                        target_gold_coord = gold_pot_coordinates_list[0] # Nimm die erste Koordinate
                        gold_x, gold_y = target_gold_coord
                        
                        diff_x = gold_x - status.x
                        diff_y = gold_y - status.y

                        # for diagonal moves
                        if abs(diff_x) == abs(diff_y):
                                if diff_x and diff_y == 0:
                                        current_move = 0
                                elif diff_x < 0 and diff_y > 0:
                                        current_move = D.up_left
                                elif diff_x < 0 and diff_y < 0:
                                        current_move = D.down_left    
                                elif diff_x > 0 and diff_y > 0:
                                        current_move = D.down_right
                                elif diff_x < 0 and diff_y < 0:
                                        current_move = D.up_right

                        #for right/left
                        if abs(diff_x) > abs(diff_y):
                                if diff_x < 0:
                                        current_move = D.left
                                elif diff_x > 0:
                                        current_move = D.right

                        #for up/down
                        if abs(diff_x) < abs(diff_y):
                                if diff_y > 0:
                                        current_move = D.up
                                elif diff_y < 0:
                                        current_move = D.down

                if current_move == None:
                        current_move = random.choice(self.moves)
                
                return [current_move]


players = [naive_markus()]
