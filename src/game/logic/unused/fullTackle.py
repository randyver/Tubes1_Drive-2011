#STRATEGI FULL TACKLE MENGGUNAKAN ATTACK + DEFEND


from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction


class FullTackleLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        
    def next_move(self, board_bot: GameObject, board: Board):

        props = board_bot.properties
        current_position = board_bot.position
        base = board_bot.properties.base

        # jika diamonds sudah 5
        if props.diamonds == 5:
            self.goal_position = base
        else:
            # Jika tidak ada tujuan spesifik, pilih langkah terbaik (greedy)
            min_distance_enemy = 100000
            current_position = board_bot.position
            nearest_enemy_position = None
            for enemy_bot in board.bots:
                if (enemy_bot != board_bot):
                    current_enemy_distance = abs(enemy_bot.position.x - current_position.x) + abs(enemy_bot.position.y - current_position.y)
                    if (current_enemy_distance < min_distance_enemy):
                        min_distance_enemy = current_enemy_distance
                        nearest_enemy_position = enemy_bot.position
            if (min_distance_enemy > 1):
                # Kejar player lain jika masih jauh
                self.goal_position = nearest_enemy_position
            else:
                if (enemy_bot.properties.diamonds >= props.diamonds):
                    # Serang player dengan diamond lebih banyak
                    self.goal_position = nearest_enemy_position
                else:
                    # Menyelamatkan diri dari serangan musuh dengan melarikan diri ke kotak kosong
                    if(nearest_enemy_position.x == board_bot.position.x):
                        return Position(board_bot.position.y, board_bot.position.x + 1)
                    
                    elif(nearest_enemy_position.y == board_bot.position.y):
                        return Position(board_bot.position.y + 1, board_bot.position.x)

        if self.goal_position:
            # Arahkan ke posisi tujuan
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y