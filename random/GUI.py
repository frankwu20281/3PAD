import tkinter as tk
import random

# Constants
MAP_SIZE = 40  # Total grid size of the map
WINDOW_SIZE = 400  # Visible window size in pixels
GRID_SIZE = 20  # Size of each cell in pixels
VIEWPORT_SIZE = WINDOW_SIZE // GRID_SIZE  # Number of visible cells in the viewport
TERRAIN_ITEMS = 100  # Number of terrain items
MONSTER_COUNT = 10  # Number of monsters

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokemon-like Game")
        self.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
        self.resizable(False, False)
        
        self.canvas = tk.Canvas(self, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="white")
        self.canvas.pack()

        # Load character image
        self.character_image = tk.PhotoImage(file="sprites\character.png")

        self.terrain = []
        self.create_terrain()
        
        
        
        self.monsters = self.place_monsters()
        self.bind("<KeyPress>", self.on_key_press)
        self.focus_set()
        
        self.draw_viewport()
    
    def create_terrain(self):
        self.player_pos = [MAP_SIZE // 2, MAP_SIZE // 2]  # Start player at the center of the map
        for _ in range(TERRAIN_ITEMS):
            x, y = random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1)
            if (x, y) != tuple(self.player_pos):
                self.terrain.append((x, y))
    
    def place_monsters(self):
        monsters = []
        while len(monsters) < MONSTER_COUNT:
            x, y = random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1)
            if (x, y) != tuple(self.player_pos) and (x, y) not in self.terrain and (x, y) not in monsters:
                monsters.append((x, y))
        return monsters
    
    def draw_viewport(self):
        self.canvas.delete("all")
        top_left_x = self.player_pos[0] - VIEWPORT_SIZE // 2
        top_left_y = self.player_pos[1] - VIEWPORT_SIZE // 2
        
        for x in range(VIEWPORT_SIZE):
            for y in range(VIEWPORT_SIZE):
                map_x = top_left_x + x
                map_y = top_left_y + y
                if (map_x, map_y) in self.terrain:
                    self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                 (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                 fill="grey")
        
        player_viewport_x = VIEWPORT_SIZE // 2
        player_viewport_y = VIEWPORT_SIZE // 2
        self.canvas.create_image(player_viewport_x * GRID_SIZE, player_viewport_y * GRID_SIZE, 
                                 anchor='nw', image=self.character_image)
        
        for monster in self.monsters:
            monster_viewport_x = monster[0] - top_left_x
            monster_viewport_y = monster[1] - top_left_y
            if 0 <= monster_viewport_x < VIEWPORT_SIZE and 0 <= monster_viewport_y < VIEWPORT_SIZE:
                self.canvas.create_rectangle(monster_viewport_x * GRID_SIZE, monster_viewport_y * GRID_SIZE,
                                             (monster_viewport_x + 1) * GRID_SIZE, (monster_viewport_y + 1) * GRID_SIZE,
                                             fill="red")

    def on_key_press(self, event):
        direction = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }.get(event.keysym)

        if direction:
            new_x = self.player_pos[0] + direction[0]
            new_y = self.player_pos[1] + direction[1]

            if 0 <= new_x < MAP_SIZE and 0 <= new_y < MAP_SIZE:
                if (new_x, new_y) not in self.terrain:
                    self.player_pos = [new_x, new_y]
                    if (new_x, new_y) in self.monsters:
                        self.open_math_challenge((new_x, new_y))
                    self.draw_viewport()

    def open_math_challenge(self, monster_pos):
        challenge = MathChallenge(self)
        self.wait_window(challenge)
        if challenge.success:
            self.monsters.remove(monster_pos)
            self.draw_viewport()

class MathChallenge(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Math Challenge")
        self.geometry("300x150")
        self.success = False
        
        self.problem, self.answer = self.generate_problem()
        self.label = tk.Label(self, text=f"Solve: {self.problem}")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(self)
        self.entry.pack(pady=10)
        self.entry.focus_set()
        
        self.submit_button = tk.Button(self, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=10)
    
    def generate_problem(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        problem = f"{num1} + {num2}"
        answer = num1 + num2
        return problem, answer
    
    def check_answer(self):
        try:
            if int(self.entry.get()) == self.answer:
                self.success = True
                self.destroy()
            else:
                self.label.config(text=f"Try again: {self.problem}")
        except ValueError:
            self.label.config(text=f"Invalid input. Solve: {self.problem}")

if __name__ == "__main__":
    game = Game()
    game.mainloop()
