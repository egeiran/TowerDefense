import pygame
import math
from pygame.math import Vector2 
from enemy_data import ENEMY_DATA
from world import World
import constants as c

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type: str, waypoints: list, images: dict) -> None:
        """
        Initialize an Enemy object.

        Parameters:
        - enemy_type: Type of the enemy.
        - waypoints: List of waypoints representing the enemy's path.
        - images: Dictionary containing images for different enemy types.
        """
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed =  ENEMY_DATA.get(enemy_type)["speed"]
        self.dmg =  ENEMY_DATA.get(enemy_type)["damage"]
        self.reward =  ENEMY_DATA.get(enemy_type)["reward"]
        self.enemy_type = enemy_type
        self.angle = 0

        self.original_image = images.get(enemy_type)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos 

    def move(self, world: World):
        """
        Move the enemy along its path.

        Parameters:
        - world: The game world.
        """
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint ])
            self.movement = self.target - self.pos
        else:
            self.kill()
            world.health -= self.dmg
            world.missed_enemies += 1

        dist = self.movement.length()
        step = self.speed * world.game_speed * world.frame_scale
        if dist >= step:
            self.pos += self.movement.normalize() * step
        else:
            if dist != 0:
                 self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        """
        Rotate the enemy to face its next waypoint.
        """
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint ])
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos 
    
    def check_alive(self, world: World):
        """
        Check if the enemy is still alive and update the game world accordingly.

        Parameters:
        - world: The game world.
        """
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += self.reward
            self.kill()

    def update(self, world: World):
        """
        Update the enemy's state in the game world.

        Parameters:
        - world: The game world.
        """
        self.check_alive(world)
        self.rotate()
        self.move(world) 