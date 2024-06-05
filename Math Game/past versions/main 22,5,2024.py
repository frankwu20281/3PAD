from  tkinter import *
from tkinter.ttk import *
import random
import json 
MAP_SIZE = 40 
WINDOW_SIZE = 600  
GRID_SIZE = 20  
VIEWPORT_SIZE = WINDOW_SIZE // GRID_SIZE  
class Game(Tk):
    def __init__(self):
        super().__init__()

        #with open("data.json") as file: 
            #self.map_storage =  json.load(file)
        self.terrain_map= ["w=======================================",
"=.....w................................=",
"=.....w................................=",
"=.....w................................=",
"=.....w................................=",
"=..............wwwwwwwwwww.............=",
"=..............w.........w.............=",
"=..............w.........w.............=",
"=..............w.........w.............=",
"=..............w.....wwwww.............=",
"=..............w..wwww.................=",
"=..............w..w....................=",
"=..............w..w.......M............=",
"=...................wx.................=",
"=......................................=",
"=................w......T..............=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"=......................................=",
"========================================"
]

        terrain_handler = Map()
        player_handler = Player()

        self.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
        self.resizable(False, False)
        
        self.canvas = Canvas(self, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="green")
        self.canvas.pack()
        # load sprites
        self.character_sprite = PhotoImage(file="sprites\character.png")
    
        
        self.spawn_location()
        self.terrain = {"walls":[], "map border":[]}
        self.walls = self.terrain["walls"]

        self.map_border= self.terrain["map border"]

        """
        for i in range(40):
            line = ""
            for a in range (40):
                line += "."
            print (line)
        """
            
        
        #self.player = self.canvas.create_rectangle(0, 0, GRID_SIZE, GRID_SIZE, fill="blue")
        
        self.bind("<KeyPress>", lambda x : player_handler.key_press(x, self))
        self.focus_set()

        #self.menu=Menu(self)


        terrain_handler.terrain_load("level 1",self)


        self.new_frame()
        self.mainloop()
    
    def key_press(self, event):
        direction = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }.get(event.keysym)

        if direction: 
            new_x = self.player_pos[0] + direction[0]
            new_y = self.player_pos[1] + direction[1]
            self.player_pos = [new_x, new_y]
            self.new_frame()

    def spawn_location (self):
        self.player_pos = []
        y_cord = 0
        for x_line in self.terrain_map:
            x_cord = 0
            for obj in x_line:
                if obj == "x": 
                    self.player_pos = [x_cord,y_cord]
                    return
                x_cord+=1
            y_cord+=1
        if not self.player_pos:
            self.player_pos = [MAP_SIZE // 2, MAP_SIZE // 2]


        
    '''

    temp function, just used to see player movement and test collision
    
    '''
    def random_terrain(self): 
        for _ in range(100):
            x, y = random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1)
            if (x, y) != tuple(self.player_pos):
                self.terrain.append((x, y))
        
        with open('data.json','w') as file: json.dump(self.terrain_map, file, indent= 2)

    def new_frame(self):
        self.canvas.delete("all")
        top_left_x = self.player_pos[0] - VIEWPORT_SIZE // 2
        top_left_y = self.player_pos[1] - VIEWPORT_SIZE // 2
        
        for key, list in self.terrain.items():
            for x in range(VIEWPORT_SIZE):
                for y in range(VIEWPORT_SIZE):
                    map_x = top_left_x + x
                    map_y = top_left_y + y
                    if (map_x, map_y) in list:
                        self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                    (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                    fill="grey" if key == "walls" else "black")
        
        
        player_viewport_x = VIEWPORT_SIZE // 2
        player_viewport_y = VIEWPORT_SIZE // 2
        self.canvas.create_image(player_viewport_x * GRID_SIZE, player_viewport_y * GRID_SIZE, 
                                 anchor='nw', image=self.character_sprite)
        

class Player(): 
    def key_press(self, event,game_instance):
        direction = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }.get(event.keysym)

        if direction: 
            new_x = game_instance.player_pos[0] + direction[0]
            new_y = game_instance.player_pos[1] + direction[1]
            if self.collision(new_x,new_y,game_instance):
                game_instance.player_pos = [new_x, new_y]
                game_instance.new_frame()
            

    def collision (self, new_x, new_y, game_instance):
        for key, list in game_instance.terrain.items():
            if (new_x,new_y) in list: 
                return False
        return True
        

    
    
class Map():
    def terrain_load(self, level_number,game_instance):
        y_cord = 0
        for x_line in game_instance.terrain_map:
            x_cord = 0
            for obj in x_line:
                if (x_cord,y_cord) != tuple(game_instance.player_pos):
                    if obj == "w": 
                    
                        game_instance.walls.append((x_cord,y_cord))
                    elif obj == "=":
                        game_instance.map_border.append((x_cord,y_cord))
                x_cord+=1
            y_cord+=1


class Menu(Tk):
    def __init__(self, game_instance):
        super().__init__()
        
        self.geometry('200x200')
        self.configure(background = "blue")




Game()
        