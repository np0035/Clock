import math
import tkinter as tk
import config
import numpy as np
import time

from tkinter import Frame, Canvas, OptionMenu, StringVar
from config import settings, dynamic_vals
from utils import update_angles


class MainWindow:

    # Triggered when the user chooses a location from the menu
    def location_chosen_event(self):

        # Update the settings with the chosen location
        settings["current_loc"] = self.chosen_loc.get()

        # Redraw the clock
        self.draw()

    def draw(self):
        update_angles()
        sunrise_angle, day_extent, hand_angle = config.get_angle_vals()
        hand_angle = hand_angle * (np.pi/180)
        # Draw clock body
        # center = (300, 300)
        self.c.create_oval(50, 50, 550, 550, outline="white", width=20)
        self.c.create_oval(60, 60, 540, 540, fill="#000060")
        self.c.create_arc(60, 60, 540, 540, fill="yellow", start=sunrise_angle, extent=day_extent)

        delineations = np.linspace(start=0, stop=np.pi*2, num=25)
        angles = list(delineations)

        for i in angles:
            self.c.create_line(240*np.cos(i) + 300, 240*np.sin(i) + 300, 220*np.cos(i) + 300, 220*np.sin(i) + 300,
                               fill="black", width=5)

        # Draw clock hand
        lines = [[300, 310], [290, 300], [300, 70], [310, 300]]
        lines_rotated = []
        print(hand_angle)
        for p in lines:
            p = np.add(p, [-300, -300])
            x = p[0] * np.cos(hand_angle) - p[1] * np.sin(hand_angle)
            y = p[0] * np.sin(hand_angle) + p[1] * np.cos(hand_angle)
            p = [x, y]
            p = np.add(p, [300, 300])
            lines_rotated.append(list(p))

        self.c.create_polygon(*lines_rotated, fill="black")
        self.c.pack()

    def __init__(self):

        # Create window
        self.w = tk.Tk()
        self.w.title("Clock")
        self.c = Canvas(self.w, width=600, height=600, background="black")

        self.draw()

        # Create frame below the clock canvas
        f = Frame(self.w, background="white", width=600, height=200)
        f.pack()

        # Dropdown menu initialization
        # Set an initial value for the menu
        self.chosen_loc = StringVar()
        self.chosen_loc.set("Select location")

        # Fill in the menu with locations
        locations = [k for k in config.get_locations().keys()]

        # Create the menu and tie it to the location_chosen_event() callback
        self.location_chooser = OptionMenu(f, self.chosen_loc, *locations, command=lambda x: self.location_chosen_event())
        self.location_chooser.pack()


        # Main window loop - handles detection of user interaction
        self.w.mainloop()
