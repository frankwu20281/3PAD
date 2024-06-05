import tkinter as tk
import random
import math

class RouletteGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        self.wheel = self.canvas.create_oval(50, 50, 350, 350, outline="black", fill="green")
        self.ball = self.canvas.create_oval(200, 50, 220, 70, fill="red")
        self.spin_button = tk.Button(master, text="Spin", command=self.spin_wheel)
        self.spin_button.pack()

    def spin_wheel(self):
        angle = random.randint(0, 359)  # Generate a random angle
        self.move_ball(angle)

    def move_ball(self, angle):
        center_x = 200
        center_y = 200
        radius = 150
        x = center_x + radius * math.sin(math.radians(angle))
        y = center_y - radius * math.cos(math.radians(angle))
        self.canvas.coords(self.ball, x - 10, y - 10, x + 10, y + 10)
        angle += 10
        if angle < 360:
            self.master.after(50, self.move_ball, angle)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Roulette Wheel")
    game = RouletteGame(root)
    root.mainloop()
