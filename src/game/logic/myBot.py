from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class MyBotLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.is_using_teleport_to_base = False
        
    def next_move(self, board_bot: GameObject, board: Board):

        props = board_bot.properties
        current_position = board_bot.position
        base = board_bot.properties.base

        # jika diamonds sudah 5
        if props.diamonds == 5:
            target_teleport_position = self.using_teleport(board_bot, board)
            if self.is_using_teleport_to_base:
                if self.goal_position != target_teleport_position:
                    self.goal_position = base
                else:
                    self.is_using_teleport = True

            elif not self.is_using_teleport_to_base:
                self.goal_position = target_teleport_position
                if target_teleport_position == current_position:
                    self.is_using_teleport = True

            else:
                self.goal_position = base

        else:
            # Jika tidak ada tujuan spesifik, pilih langkah terbaik (greedy)
            goal_from_base, min_distance_base = self.nearest_diamond_from_base(board_bot, board)
            goal_from_player, min_distance_player = self.nearest_diamond_from_bot(board_bot, board)
            min_distance = min(min_distance_base, min_distance_player)
            goal_button, is_using_button = self.using_button(board_bot, board, min_distance)

            if (board_bot.properties.milliseconds_left < 15000):
                if min_distance_base <= 5:
                    self.goal_position = goal_from_base
                else:
                    self.goal_position = base
            else : 
                    if is_using_button:
                        self.goal_position = goal_button
                    else:
                        self.goal_position = goal_from_player

        if self.goal_position:
            # Arahkan ke posisi tujuan
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y

    # jarak diamond terdekat dengan bot
    def nearest_diamond_from_bot(self, board_bot: GameObject, board: Board):
        diamonds = board.diamonds
        if board_bot.properties.diamonds == 4:
            blue_diamonds = [diamond for diamond in diamonds if diamond.properties.points == 1]
            if (len(blue_diamonds)>0):
                current_position = board_bot.position
                distances = [abs(current_position.x - diamond.position.x) + abs(board_bot.position.y - diamond.position.y) for diamond in blue_diamonds]
                nearest_diamond_index = distances.index(min(distances))
                diamond_from_bot = blue_diamonds[nearest_diamond_index].position
                min_distance_diamond_bot = distances[nearest_diamond_index]
            else :
                diamond_from_bot = board_bot.properties.base    
            return diamond_from_bot, min_distance_diamond_bot
        else:
            diamonds = [diamond for diamond in diamonds]
            current_position = board_bot.position
            distances = [abs(current_position.x - diamond.position.x) + abs(board_bot.position.y - diamond.position.y) for diamond in diamonds]
            nearest_diamond_index = distances.index(min(distances))
            diamond_from_bot = diamonds[nearest_diamond_index].position
            min_distance_diamond_bot = distances[nearest_diamond_index]
            return diamond_from_bot, min_distance_diamond_bot
    
    # jarak diamond terdekat dengan base
    def nearest_diamond_from_base(self, board_bot :GameObject, board: Board):
        # Check for diamonds
        base = board_bot.properties.base
        min_distance_diamond_base = 100000
        if(board_bot.properties.diamonds == 4):
            for gameObjects in board.game_objects:
                if (gameObjects.type == "DiamondGameObject" and gameObjects.properties.points == 1):
                    diamond_distance = abs(gameObjects.position.x - base.x) + abs(gameObjects.position.y - base.y)
                    if diamond_distance < min_distance_diamond_base:
                        min_distance_diamond_base = diamond_distance
                        diamond_from_base = gameObjects.position
            return diamond_from_base, min_distance_diamond_base
        else:
            for diamond in board.diamonds:
                diamond_distance = abs(diamond.position.x - base.x) + abs(diamond.position.y - base.y)
                if diamond_distance < min_distance_diamond_base:
                    min_distance_diamond_base = diamond_distance
                    diamond_from_base = diamond.position    
            return diamond_from_base, min_distance_diamond_base
        
    # jarak terdekat bot lawan    
    def nearest_enemy(self, board_bot: GameObject, board: Board, diamond_distance):
        min_distance_enemy = 100000
        current_position = board_bot.position
        nearest_enemy_position = None
        for enemy_bot in board.bots:
            if (enemy_bot != board_bot):
                if (5 * enemy_bot.properties.diamonds >= diamond_distance):
                    if (abs(enemy_bot.position.x - current_position.x) + abs(enemy_bot.position.y - current_position.y) < min_distance_enemy):
                        min_distance_enemy = abs(enemy_bot.position.x - current_position.x) + abs(enemy_bot.position.y - current_position.y)
                        nearest_enemy_position = enemy_bot.position
        return nearest_enemy_position, min_distance_enemy

    # gunakan teleport saat pulang ke base (diamond sudah berjumlah 5)
    def using_teleport(self, board_bot: GameObject, board: Board):
        base = board_bot.properties.base
        current_position = board_bot.position
        teleport_objects: List[Position] = []

        for game_object in board.game_objects:
            if game_object.type == "TeleportGameObject":
                teleport_objects.append(game_object.position)

        distance_teleport_first_from_bot = abs(teleport_objects[0].x - current_position.x) + abs(teleport_objects[0].y - current_position.y)
        distance_teleport_second_from_bot = abs(teleport_objects[1].x - current_position.x) + abs(teleport_objects[1].y - current_position.y)
        distance_teleport_first_from_base = abs(teleport_objects[0].x - base.x) + abs(teleport_objects[0].y - base.y)
        distance_teleport_second_from_base = abs(teleport_objects[1].x - base.x) + abs(teleport_objects[1].y - base.y)
        distance_bot_from_base = abs(current_position.x - base.x) + abs(current_position.y - base.y)

        if distance_teleport_first_from_bot <= distance_teleport_second_from_bot:
            if (distance_teleport_first_from_bot + distance_teleport_second_from_base) <= distance_bot_from_base:
                target_position = teleport_objects[0]
            else:
                target_position = base

        else:
            if (distance_teleport_second_from_bot + distance_teleport_first_from_base) <= distance_bot_from_base:
                target_position = teleport_objects[1]
            else:
                target_position = base

        return target_position

    # menggunakan button jika posisi diamonds jauh dari bot sehingga memungkinkan bot memperoleh diamond lebih dekat      
    def using_button(self, board_bot: GameObject, board: Board, min_distance: int):
        current_position = board_bot.position
        button_position: List[Position] = []

        for game_object in board.game_objects:
            if game_object.type == "DiamondButtonGameObject":
                button_position.append(game_object.position)
                break
        
        distance_bot_button = abs(current_position.x - button_position[0].x) + abs(current_position.y - button_position[0].y)

        if (min_distance > 5 and distance_bot_button < min_distance):
            is_using_button = True
        
        else:
            is_using_button = False

        return button_position[0], is_using_button
        
        
        
    
