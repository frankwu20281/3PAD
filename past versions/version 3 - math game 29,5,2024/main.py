from  tkinter import *
from tkinter.ttk import *
import random
import json 
from player import *
from battle import *
from map import *
from monster import *
MAP_SIZE = 40 
WINDOW_SIZE = 600  
GRID_SIZE = 40
VIEWPORT_SIZE = WINDOW_SIZE // GRID_SIZE  


class Game(Tk):
    def __init__(self):
        super().__init__()
        
        with open("map_data.json") as file: 
            self.map_storage =  json.load(file)
        with open("monster_path_data.json") as file: 
            self.monster_path_storage = json.load(file)

        

        self.level_number = 1
        self.player_pos = [] 
        
        self.terrain_map= self.map_storage[str(self.level_number)]
        self.monster_path_map= self.monster_path_storage[str(self.level_number)]

       
        #setting up game screen, canvas
        self.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
        self.resizable(False, False)      
        self.canvas = Canvas(self, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="orange")
        self.canvas.pack()

        # loading in all the different file classes
        self.monster_handler = Monster(self)
        self.player_handler = Player(self)
        self.battle_handler = Battle(self)

        # load sprites
        self.character_sprite = PhotoImage(file="sprites\Textures\character.png")
        self.wall_sprite = PhotoImage(file="sprites\Textures\wall.png")
        self.grass_full_sprite = PhotoImage(file="sprites\Textures\grass.png")

        self.reset_cord_storage()       
        
        self.load_terrain_map()
        # binds arrow keys for moVEMENT        
        self.bind("<KeyPress>", lambda x : self.player_movement(x) )
        self.focus_set()        
        self.bind('<Map>', lambda x : self.monster_loop(x))
           
        self.mainloop()

        #self.menu=Menu(self) opens new window 
        #terrain_handler.terrain_load("level 1",self)
    def load_terrain_map(self): 
        Map(self) 
        self.monster_handler.monster_path_load()
        self.new_frame()
        return
    
    def player_movement(self, event):
        
        run =self.player_handler.key_press(event)
   
        
        if type(run)== list:
            self.player_pos =run
            print(run)
        elif run == "battle time":
            print("battle time")
            Battle(self)
        elif run == "teleport": 
            # map shit
            pass
        
        self.new_frame()
        
        
        pass
    def reset_cord_storage (self): 
        self.monster = []
        self.walls = []
        self.map_border=[]
        self.teleport = []
        self.grass_full = []
        self.terrain_cords_dict = {"walls":self.walls, 
                                   "border":self.map_border,
                                   "teleport":self.teleport,
                                   "grass full":self.grass_full, 
                                   "monster": self.monster}
        
        
        self.monster_down= []
        self.monster_up= []
        self.monster_left= []
        self.monster_right= []
        self.monster_movement_cords_dict = {"down": self.monster_down, 
                                            "up":self.monster_up,
                                            "left": self.monster_left, 
                                            "right":self.monster_right}


    def monster_loop(self,event):
        
        self.monster_handler.move_monster_cords()
        self.new_frame()
        self.after(1000, lambda: self.monster_loop(event))
        
        self.unbind('<Map>')

    def new_frame(self):
        self.canvas.delete("all")
        #update player pos
        player_viewport_x = VIEWPORT_SIZE // 2
        player_viewport_y = VIEWPORT_SIZE // 2
        self.canvas.create_image(player_viewport_x * GRID_SIZE, player_viewport_y * GRID_SIZE, 
                                 anchor='nw', image=self.character_sprite)
        
        #update all terrain pos
        top_left_x = self.player_pos[0] - VIEWPORT_SIZE // 2
        top_left_y = self.player_pos[1] - VIEWPORT_SIZE // 2
        
        
        for key, list in self.terrain_cords_dict.items():
            for x in range(VIEWPORT_SIZE):
                for y in range(VIEWPORT_SIZE):
                    map_x = top_left_x + x
                    map_y = top_left_y + y
                    if (map_x, map_y) in list:
                        #if key == "grass full":
                            #self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                            #                        (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                            #                        fill="green" , width=0)
                            
                        if key == "walls":
                            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                    (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                    fill="grey" )
                            #self.canvas.create_image(x * GRID_SIZE, y * GRID_SIZE, 
                                # anchor='nw', image=self.wall_sprite)
                            
                        if key == "border": 
                            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                    (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                    fill="black" )
                        if key == "teleport": 
                            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                    (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                    fill="blue" )
                        if key == "monster": 
                            print(" list of current monster cords" ,list)
                            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                    (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                    fill="red" )
                        
        

        
class Cutscreens ():
    def __init__(self) -> None:
        pass


class Menu(): 
    def __init__(self, game_instance):
        pass

class fake_ass_menu(Tk):
    def __init__(self, game_instance):
        super().__init__()
        

        self.geometry('200x200')
        self.configure(background = "blue")

Game()

            
        