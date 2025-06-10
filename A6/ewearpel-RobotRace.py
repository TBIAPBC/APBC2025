import random

from game_utils import GameParameters
from game_utils import nameFromPlayerId
from game_utils import Direction as D, TileStatus, Map
from player_base import Player
from heapq import heappop, heappush


class NaivePlayer(Player):
	def reset(self, player_id, max_players, width, height):
		self.player_name = "RennigNaive"
		self.moves = [D.up, D.left, D.down, D.right, D.up, D.up_left, D.down_left,
						D.down_right, D.up_right]
		self.ourMap = Map(width, height)
		self.prev_pos = None
		self.stuck_count = 0

	def round_begin(self, r):
		"""Reset state at the beginning of each round"""
		self.prev_pos = None
		self.stuck_count = 0
		self.last_gold_pos = None


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



class AdvancedPlayer(Player):
    def reset(self, player_id, max_players, width, height):
        self.player_name = "RennigAdvanced"
        self.map = Map(width, height)
        self.w, self.h = self.map.width, self.map.height
        self.dirs = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]
        self.dir_map = {d: i for i, d in enumerate(self.dirs)}
        self.center = (self.w // 2, self.h // 2)
        self.cache = {}
        self.Directions = {
            0: D.up,
            1: D.down,
            2: D.left,
            3: D.right,
            4: D.up_left,
            5: D.up_right,
            6: D.down_left,
            7: D.down_right
        }

    def round_begin(self, r):
        self.cache.clear()

    def set_mines(self, status):
        return []

    def heuristic(self, a, b):
        wall_density = self.get_wall_density(a)
        
        dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
        base_dist = max(dx, dy)
        
        if wall_density > 0.4:  # In tight spaces
            manhattan = dx + dy
            return manhattan + (manhattan * wall_density)
        else:
            return base_dist

    def astar(self, start, goal, allow_jump=False):
        cache_key = (start, goal, allow_jump)
        if cache_key in self.cache:
            return self.cache[cache_key]

        open_set = [(0, start, [])]
        visited = {start: 0}

        while open_set:
            f, pos, path = heappop(open_set)

            if pos == goal:
                result = path + [pos]
                self.cache[cache_key] = result
                return result

            if visited.get(pos, float('inf')) < len(path):
                continue

            x, y = pos
            for dx, dy in self.dirs:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < self.w and 0 <= ny < self.h):
                    continue

                tile = self.status.map[nx, ny].status
                new_path = path + [pos]

                if str(tile) in ['.', '_']:
                    cost = len(new_path) + 1
                    if cost < visited.get((nx, ny), float('inf')):
                        visited[(nx, ny)] = cost
                        h = self.heuristic((nx, ny), goal)
                        heappush(open_set, (cost + h, (nx, ny), new_path))

                elif allow_jump and str(tile) == '#':
                    jx, jy = nx + dx, ny + dy
                    if (0 <= jx < self.w and 0 <= jy < self.h and
                            str(self.status.map[jx, jy].status) in ['.', '_']):
                        cost = len(new_path) + 5  # Adlhart-style jump cost = 5
                        if cost < visited.get((jx, jy), float('inf')):
                            visited[(jx, jy)] = cost
                            h = self.heuristic((jx, jy), goal)
                            heappush(open_set, (cost + h, (jx, jy), new_path))

        return []

    def path_cost(self, path):
        if len(path) < 2:
            return 0
        cost = 0
        for i in range(1, len(path)):
            dx = abs(path[i][0] - path[i - 1][0])
            dy = abs(path[i][1] - path[i - 1][1])
            if dx == 2 or dy == 2:
                cost += 5  # jump cost
            else:
                cost += 1
        return cost

    def competitor_threat(self, gold_pos):
        my_pos = (self.status.x, self.status.y)
        my_dist = len(self.astar(my_pos, gold_pos, False))

        min_enemy_dist = float('inf')
        for other in self.status.others:
            if other:
                enemy_dist = len(self.astar((other.x, other.y), gold_pos, False))
                min_enemy_dist = min(min_enemy_dist, enemy_dist)

        return min_enemy_dist < my_dist * 0.75

    def get_wall_density(self, pos, radius=3):
        wall_count = 0
        total = 0
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x, y = pos[0] + dx, pos[1] + dy
                if 0 <= x < self.w and 0 <= y < self.h:
                    total += 1
                    if str(self.status.map[x, y].status) == '#':
                        wall_count += 1
        return wall_count / total if total > 0 else 0

    def move(self, status):
        self.status = status
        pos = (status.x, status.y)
        
        wall_density = self.get_wall_density(pos)
        
        max_steps = int(7 * (1 - wall_density))
        center_steps = int(3 * (1 - wall_density)) + 1
        
        if not status.goldPots:
            center_path = self.astar(pos, self.center, False)
            return ([self.Directions[self.dir_map[(center_path[i][0] - center_path[i-1][0], 
                    center_path[i][1] - center_path[i-1][1])]] 
                    for i in range(1, min(center_steps, len(center_path)))]) if len(center_path) > 1 else []

        gold_pos = list(status.goldPots.keys())[0]
        gold_val = list(status.goldPots.values())[0]

        path_normal = self.astar(pos, gold_pos, False)
        path_jump = self.astar(pos, gold_pos, True) if status.params.jumps_ok else []

        cost_normal = self.path_cost(path_normal) if path_normal else float('inf')
        cost_jump = self.path_cost(path_jump) if path_jump else float('inf')

        best_path = []
        best_cost = float('inf')
        max_cost_threshold = 25
        min_profit_margin = 20

        if path_normal and cost_normal < max_cost_threshold and gold_val - cost_normal > min_profit_margin:
            best_path = path_normal
            best_cost = cost_normal

        if path_jump and cost_jump < best_cost and cost_jump < max_cost_threshold and gold_val - cost_jump > min_profit_margin:
            best_path = path_jump
            best_cost = cost_jump

        if self.competitor_threat(gold_pos):
            best_path = self.astar(pos, self.center, False)[:2]

        if not best_path or gold_val - best_cost <= min_profit_margin:
            best_path = self.astar(pos, self.center, False)[:2]

        moves = []
        current = pos

        for next_pos in best_path[1:min(max_steps + 1, len(best_path))]:
            if len(moves) >= 7:
                break

            dx = next_pos[0] - current[0]
            dy = next_pos[1] - current[1]

            if str(status.map[next_pos[0], next_pos[1]].status) not in ['.', '_']:
                break

            if max(abs(dx), abs(dy)) == 2:
                dir_idx = self.dir_map.get((dx // 2, dy // 2), 0)
                moves.extend([dir_idx, dir_idx])
            else:
                moves.append(self.dir_map.get((dx, dy), 0))

            current = next_pos

        direction_moves = [self.Directions[move] for move in moves]
        return direction_moves


players = [AdvancedPlayer()]

