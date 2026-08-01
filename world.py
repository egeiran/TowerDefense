import pygame
import random
from enemy_data import ENEMY_SPAWN_DATA
import constants as c

class World():
    def __init__(self, level_data,  map_img: pygame.Surface) -> None:
        """
        Initialize a World object.

        Parameters:
        - level_data: Data for the current game level.
        - map_img: Pygame surface representing the game map.
        """
        self.level = 1
        self.game_speed = 1
        # set every frame by the game loop: how long the last frame took,
        # relative to c.REFERENCE_FPS
        self.frame_scale = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoints = []
        self.level_data = level_data
        self.image = map_img
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def process_data(self):
        """
        Process level data to extract tile map and waypoints.
        """
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for object in layer["objects"]:
                    waypoint_data = object["polyline"]
                    self.process_waypoints(waypoint_data)
    
    def process_waypoints(self, waypoint_data):
        """
        Process waypoint data and append waypoints to the waypoints list.

        Parameters:
        - waypoint_data: Data representing waypoints.
        """
        for point in waypoint_data:
             temp_x = point.get("x")
             temp_y = point.get("y")
             self.waypoints.append((temp_x, temp_y  ))

    def process_enemies(self):
        """
        Process enemy data and create a list of enemies to spawn for the current level.
        """
        if self.level <= c.TOTAL_LEVELS:
            enemies = ENEMY_SPAWN_DATA[self.level - 1]
            for enemy_type in enemies:
                enemies_to_spawn = enemies[enemy_type]
                for enemy in range(enemies_to_spawn):
                    self.enemy_list.append(enemy_type)
        #randomize list to shuffle enemies
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        """
        Check if the current level is complete (all enemies killed or missed).

        Returns:
        - True if the level is complete, False otherwise.
        """
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True
    
    def reset_level(self):
        """
        Reset level-related variables for a new level.
        """
        # reset enemy variables
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
        

    def draw(self, screen: pygame.Surface):
        """
        Draw the game map on the specified surface.

        Parameters:
        - screen: The Pygame surface to draw on.
        """
        screen.blit(self.image, (0,0))