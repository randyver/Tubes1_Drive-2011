import random
from typing import Optional
import math

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class MyBotLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    # def next_move(self, board_bot: GameObject, board: Board):
    #     props = board_bot.properties
    #     # Analyze new state
    #     if props.diamonds == 5:
    #         # Move to base
    #         base = board_bot.properties.base
    #         self.goal_position = base
    #     else:
    #         # Find nearest diamond
    #         delta_x, delta_y = self.directions[0]
    #         # self.goal_position = self.find_nearest_diamond(board_bot, board)

    #     # current_position = board_bot.position
    #     # if self.goal_position:
    #     #     # We are aiming for a specific position, calculate delta
    #     #     delta_x, delta_y = get_direction(
    #     #         current_position.x,
    #     #         current_position.y,
    #     #         self.goal_position.x,
    #     #         self.goal_position.y,
    #     #     )
    #     # else:
    #     #     # No diamond or base found, just roam around
    #     #     delta = self.directions[self.current_direction]
    #     #     delta_x = delta[0]
    #     #     delta_y = delta[1]
    #     #     if random.random() > 0.6:
    #     #         self.current_direction = (self.current_direction + 1) % len(
    #     #             self.directions
    #     #         )
    #     return delta_x, delta_y
        
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position

        if props.diamonds >= 4 or props.milliseconds_left < 10000:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Jika tidak ada tujuan spesifik, pilih langkah terbaik (greedy)
            goal_from_base, min_distance_base = self.nearest_diamond_from_base(board_bot, board)
            goal_from_player, min_distance_player = self.nearest_diamond_from_player(current_position, board)
            if min_distance_base > min_distance_player:
                self.goal_position = goal_from_player
            else:
                self.goal_position = goal_from_base
            # self.goal_position = goal_from_player

        if self.goal_position:
            # Arahkan ke posisi tujuan
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        # else:
        #     # Jika tidak ada tujuan, bergerak secara acak (roaming)
        #     delta = self.directions[0]  # Pilih arah ke depan
        #     delta_x = delta[0]
        #     delta_y = delta[1]

        return delta_x, delta_y

    def nearest_diamond_from_player(self, current_position: Position, board: Board):
        diamonds = board.diamonds
        if not diamonds:
            return None

        distances = [abs(current_position.x - diamond.position.x) + abs(current_position.y - diamond.position.y) for diamond in diamonds]
        nearest_diamond_index = distances.index(min(distances))
        
        return diamonds[nearest_diamond_index].position, distances[nearest_diamond_index]
    
    def nearest_diamond_from_base(self, board_bot :GameObject, board: Board):
        # Check for diamonds
        base = board_bot.properties.base
        min_distance = 100000
        for diamond in board.diamonds:
            diamond_distance = abs(diamond.position.x - base.x) + abs(diamond.position.y - base.y)
            if diamond_distance < min_distance:
                min_distance = diamond_distance
                target = diamond.position    
        return target,min_distance