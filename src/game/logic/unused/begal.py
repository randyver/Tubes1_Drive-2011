# STRATEGI MEMBEGAL LAWAN DI DEPAN BASE

from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction


class BegalLogic(BaseLogic):
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

        # Jika sudah di dalam base musuh
        else:
            # Jika tidak ada tujuan spesifik, pilih langkah terbaik (greedy)
            target_base = None
            max_enemy_diamond = -1
            current_position = board_bot.position
            for enemy_bot in board.bots:
                if (enemy_bot != board_bot):
                    # Mencari musuh dengan diamond terbanyak
                    if (max_enemy_diamond < enemy_bot.properties.diamonds):
                        max_enemy_diamond = enemy_bot.properties.diamonds
                        target_base = enemy_bot.properties.base

            # Jika sampai di base musuh
            if (abs(target_base.x - current_position.x) + abs(target_base.y - current_position.y) == 0):
                self.goal_position = enemy_bot.position

                # Tunggu dia datang, langsung tackle
                if (abs(enemy_bot.position.x - current_position.x) + abs(enemy_bot.position.y - current_position.y) < 2):
                    self.goal_position = enemy_bot.position
            else:
                # Incar basenya 
                self.goal_position = target_base

        if self.goal_position:
            # Arahkan ke posisi tujuan
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y