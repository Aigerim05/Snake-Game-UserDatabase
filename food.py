import pygame
import random
from game_object import GameObject 
from game_object import Point 

class Food(GameObject):
    def __init__(self, point, color, tile_width):
        super().__init__([Point(point[0], point[1])],color, tile_width)
    
    def can_eat(self, head_location):
        result = None
        for point in self.points:
            if point.X == head_location.X and point.Y == head_location.Y:
                result = point
                break
        return result

    def get_random_coordinates(self, occupied_points=[]):
        occupied = []
        for i in occupied_points: occupied.append((i.X/20, i.Y/20))
        all_possible = []
        for i in range(20):
            for j in range(15):
                if (i, j) not in occupied:
                    all_possible.append((i*20, j*20))
        return random.choice(all_possible)
