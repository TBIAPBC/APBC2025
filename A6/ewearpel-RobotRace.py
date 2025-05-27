import random
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
from shortestpaths import AllShortestPaths
from collections import deque
import numpy as np

class NaivePlayer(Player):
	def reset(self, player_id, max_players, width, height):
		self.player_name = "RennigNaive"
		self.moves = [D.up, D.left, D.down, D.right, D.up, D.up_left, D.down_left,
						D.down_right, D.up_right]
		self.ourMap = Map(width, height)
		self.prev_pos = None

	def round_begin(self, r):
		pass


	def set_mines(self, status):
		"""
		Called to ask the player to set mines

		@param self the Player itself
		@param status the status
		@returns list of coordinates on the board

		The player answers with a list of positions, where mines
		should be set.

		Cost of setting mines:
		setting a mine in move distance k (as-the-eagle-flies, i.e.
		ignoring obstacles) to the player causes k actions.
		Actions are charged as usual.

		If a player does not define the method, this step is
		skipped.
		"""

		return []

	def move(self, status):
		if not status.goldPots:
			self.prev_pos = (status.x, status.y)
			return [self.random_safe_move(status)]

		# find the nearest gold pot by Manhattan distance
		target = min(status.goldPots.keys(), key=lambda pos: abs(pos[0] - status.x) + abs(pos[1] - status.y))
		gx, gy = target

		# compute direction priorities sorted by closeness to the target
		def move_priority(move):
			mx, my = move.as_xy()
			new_x = status.x + mx
			new_y = status.y + my
			return abs(gx - new_x) + abs(gy - new_y)

		# try all directions sorted by how close they move us to the target
		directions = list(D)
		directions.sort(key=move_priority)

		for move in directions:
			mx, my = move.as_xy()
			new_x = status.x + mx
			new_y = status.y + my
			if self.is_safe(new_x, new_y, status):
				if self.prev_pos is not None and (new_x, new_y) == self.prev_pos:
					continue
				self.prev_pos = (status.x, status.y)
				return [move]

		# fallback: try a random safe move
		self.prev_pos = (status.x, status.y)
		return [self.random_safe_move(status)]

	def random_safe_move(self, status):
		directions = list(D)
		random.shuffle(directions)

		for direction in directions:
			new_x = status.x + direction.as_xy()[0]
			new_y = status.y + direction.as_xy()[1]

			if self.is_safe(new_x, new_y, status):
				if self.prev_pos is not None and (new_x, new_y) == self.prev_pos:
					continue
				return direction

		return D.stay



	def is_safe(self, x, y, status):
		if not (0 <= x < status.map.width and 0 <= y < status.map.height):
			return False

		for other in self.status.others:
			if other != None:
				x_other, y_other = (other.x, other.y)
				self.ourMap[x_other, y_other].status = TileStatus.Wall

		tile = status.map[x, y]
		return tile.status not in [TileStatus.Wall, TileStatus.Mine]







players = [ NaivePlayer() ]
