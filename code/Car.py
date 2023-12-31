import numpy as np
import math
import random

from Matrix import Matrix
from Vector import Vector

class Car:
    def __init__(self, max_speed, acceleration, brake_force, turning_speed, drag, starting_position, steering_to_speed_ratio) -> None:
        self.speed = 0
        self.rotation = 0
        self.position = Vector(starting_position[0], starting_position[1])

        self.max_speed = max_speed
        self.acceleration = acceleration
        self.brake_force = brake_force
        self.turning_speed = turning_speed
        # Drag is inverse the smaller it is the more drag there is
        self.drag = drag
        # 0 - 1, the higher this is the less the steering is affected by speed
        self.steering_to_speed_ratio = steering_to_speed_ratio
        self.starting_position = starting_position

    def update_position(self, acceleration, steering, delta_time):
        if acceleration >= 0:
            self.speed += acceleration*self.acceleration*delta_time
        elif acceleration < 0:
            self.speed += acceleration*self.brake_force*delta_time

        self.speed -= (self.speed/self.drag)*delta_time

        if self.speed < 0: 
            self.speed = 0
        elif self.speed > self.max_speed:
            self.speed = self.max_speed

        steering_value = steering*(-self.steering_to_speed_ratio*(self.speed/self.max_speed) + 1)
        if self.speed == 0:
            steering_value = 0

        self.rotation += (steering_value*self.turning_speed)*delta_time
        rotation_in_rad = (self.rotation*math.pi)/180

        self.position.x += math.cos(rotation_in_rad)*self.speed*delta_time
        self.position.y += math.sin(rotation_in_rad)*self.speed*delta_time

    def get_vertices(self, length, width):
        vertices = np.array([Vector(-width/2, -length/2), Vector(-width/2, length/2), 
                             Vector(width/2, length/2), Vector(width/2, -length/2)])

        rotation_matrix = Matrix.generate_rotation_matrix(self.rotation)
        for i in range (0, 4):
            vertices[i] = rotation_matrix * vertices[i]
            vertices[i] += self.position

        return vertices
    
    def reset_position(self, random_pos=False, gates=None):
        if random_pos == False:
            self.position.x = self.starting_position[0]
            self.position.y = self.starting_position[1]
            self.rotation = 0
        else:
            random_index = random.randrange(0, len(gates))
            
            pos1 = gates[random_index][0][0]
            pos2 = gates[random_index][0][1]

            self.position.x = (pos1[0] + pos2[0])/2
            self.position.y = (pos1[1] + pos2[1])/2
            self.rotation = (math.atan2((pos1[0] - pos2[0]), (pos2[1] - pos1[1])))*(180/math.pi)
        
        self.speed = 0