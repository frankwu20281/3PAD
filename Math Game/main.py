from  tkinter import *
from tkinter.ttk import *

from player import *  
from battle import *        
from map import *       
from monster import *   
from menu import *   
import os 
#os.system('xset r off')

import json 
MAP_SIZE = 40 
WINDOW_SIZE_HEIGHT = 600  
WINDOW_SIZE_WIDTH = 800  
GRID_SIZE = 40
VIEWPORT_SIZE_HEIGHT = WINDOW_SIZE_HEIGHT // GRID_SIZE  
VIEWPORT_SIZE_WIDTH = WINDOW_SIZE_WIDTH // GRID_SIZE 

        
    


class Game(Tk):
    def __init__(self):
        
        super().__init__()
       
        
        with open("map_data.json") as file: 
            self.map_storage =  json.load(file)
        with open("monster_path_data.json") as file: 
            self.monster_path_storage = json.load(file)

        

        self.level_number = 1
        self.player_pos = [] 
        self.moving = True

        
        self.terrain_map= self.map_storage[str(self.level_number)]
        self.monster_path_map= self.monster_path_storage[str(self.level_number)]

        
       
        #setting up game screen, canvas
        self.geometry(f"{600*2}x800")
        self.resizable(False, False)      
        self.canvas = Canvas(self, width=WINDOW_SIZE_WIDTH, height=WINDOW_SIZE_HEIGHT, bg="orange")
        self.canvas.pack()
        self.menu_frame = Frame(self, bg= "blue")
        self.menu_frame.pack()


        # load sprites
        self.character_sprite = PhotoImage(file="sprites\character.png")
        self.wall_sprite = PhotoImage(file="sprites\wall.png")
        self.grass_full_sprite = PhotoImage(file="sprites\grass_full.png")
        self.fuck = PhotoImage(file="sprites\Tilted_Towers.png")
        self.monster_image = PhotoImage(file="sprites\o.png")


        # loading in all the different file classes
        self.menu_handler = Menu(self)
        self.monster_handler = Monster(self)
        self.player_handler = Player(self)

        self.battle_handler = Battle(self)

        self.map_handler = Map(self)
        
        

        #self.load_terrain_map()
        # binds arrow keys for moVEMENT        
        self.bind("<KeyPress>", lambda x : self.player_movement(x) )
        #self.bind("<KeyRelease>", lambda x : self.player_stop_movement(x))
          
        self.bind('<Map>', lambda x: self.monster_loop())
        
        
        

       
        self.mainloop()

        #self.fake_ass_menu=Menu(self) opens new window 
        #terrain_handler.terrain_load("level 1",self)


    
    def player_stop_movement(self, event):
        self.moving = False

        
    def player_movement(self, event):
        
        result = self.player_handler.key_press(event)
        self.moving = True
        
        if type(result)== list:
            self.player_pos = result
            print(result)
        elif result == "battle time":
            print("battle time")
            self.menu_handler.load_battle_menu()
            self.battle_handler.battle_screen() 
            self.moving = False
            return
        elif result == "teleport": 
            self.map_handler.next_level()
            
            return
        
        self.moving = True
        self.new_frame()
        #if self.moving == True:
            #self.after(300,lambda :self.player_movement(event))



    def monster_loop(self):
        
        if self.moving == True:
            self.monster_handler.move_monster_cords()
            self.new_frame()
            self.after(1000, lambda: self.monster_loop())
        
        self.unbind('<Map>')

    def new_frame(self):
        self.canvas.delete("all")
        self.canvas.configure(bg="green")
        #update player pos
        player_viewport_x = VIEWPORT_SIZE_WIDTH //2 #VIEWPORT_SIZE // 2
        player_viewport_y = VIEWPORT_SIZE_HEIGHT // 2
        self.canvas.create_image(player_viewport_x * GRID_SIZE, player_viewport_y * GRID_SIZE, 
                                 anchor='nw', image=self.character_sprite)
        
        #update all terrain pos
        top_left_x = self.player_pos[0] - VIEWPORT_SIZE_WIDTH // 2
        top_left_y = self.player_pos[1] - VIEWPORT_SIZE_HEIGHT // 2
        
        
        for key, list in self.terrain_cords_dict.items():
            for x in range(VIEWPORT_SIZE_WIDTH):
                for y in range(VIEWPORT_SIZE_HEIGHT):
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



class fake_ass_menu(Tk):
    def __init__(self, game_instance):
        super().__init__()
        

        self.geometry('200x200')
        self.configure(background = "blue")

Game()
            
        