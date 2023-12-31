from tkinter import *

from Vector import Vector
from Car import Car

class Graphics:
    def __init__(self, path_to_track, window_dimensions) -> None:
        self.root = Tk()
        self.main_screen = Canvas(width=window_dimensions[0], height=window_dimensions[1])
        self.main_screen.pack()

        track_image = PhotoImage(file=path_to_track)
        self.root.track_image = track_image
        self.main_screen.create_image(0, 0, image=track_image, anchor=NW)

        self.lap_time_text = self.main_screen.create_text(30, 30, text="Lap Time: No Lap Time", font=("ariel", 15), anchor=NW)

        self.car_sprite = 0
        self.gates = []
        self.raycasts = []

    def draw_car(self, car, color, car_size):
        self.main_screen.delete(self.car_sprite)
        
        car_vertices = car.get_vertices(car_size[0], car_size[1])
        self.car_sprite = self.main_screen.create_polygon(car_vertices[0].x, car_vertices[0].y,
                                                          car_vertices[1].x, car_vertices[1].y,
                                                          car_vertices[2].x, car_vertices[2].y,
                                                          car_vertices[3].x, car_vertices[3].y,
                                                          fill=color)

    def update_lap_time(self, time):
        self.main_screen.itemconfig(self.lap_time_text, text=f"Lap Time: {str(time)}")

    def draw_gates(self, gates, finish_line):
        for i in range (0, len(self.gates)):
            self.main_screen.delete(self.gates[i])

        self.gates = []
        
        for gate in gates:
            color = "red"
            if gate[1] == 1:
                color = "green"

            self.gates.append(self.main_screen.create_line(gate[0][0][0], gate[0][0][1], gate[0][1][0], gate[0][1][1], fill=color, width=3))

        self.gates.append(self.main_screen.create_line(finish_line[0][0], finish_line[0][1], finish_line[1][0], finish_line[1][1], fill="blue", width=5))

    def update_gate(self, index, status, gate):
        self.main_screen.delete(self.gates[index])
        
        color = "green"
        if status == 0:
            color = "red"

        self.gates[index] = self.main_screen.create_line(gate[0][0][0], gate[0][0][1], gate[0][1][0], gate[0][1][1], fill=color, width=3)

    def draw_raycasts(self, raycasts):
        for i in range (0, len(self.raycasts)):
            self.main_screen.delete(self.raycasts[i])
        
        for raycast in raycasts:
            color = "blue"
            if raycast[2] == 1:
                color = "light blue"

            self.raycasts.append(self.main_screen.create_line(raycast[0][0], raycast[0][1], raycast[1][0], raycast[1][1], width=2, fill=color))

    def update_window(self):
        self.root.update_idletasks()
        self.root.update()