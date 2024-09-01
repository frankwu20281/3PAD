from  tkinter import *
from tkinter.ttk import *
import random
import json 
MAP_SIZE = 40 
WINDOW_SIZE = 600  
GRID_SIZE = 40
VIEWPORT_SIZE = WINDOW_SIZE // GRID_SIZE  

class Game(Tk):
    def __init__(self):
        super().__init__()
        self.level_number = 1
        with open("map_data.json") as file: 
            self.map_storage =  json.load(file)
        with open("monster_path_data.json") as file: 
            self.monster_path_storage = json.load(file)

        self.terrain_map= self.map_storage[str(self.level_number)]
        self.monster_path_map= self.monster_path_storage[str(self.level_number)]

        self.start = False
        self.player_pos = [] 
       
        #setting up game screen, canvas
        self.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
        self.resizable(False, False)      
        self.canvas = Canvas(self, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="green")
        self.canvas.pack()


        #creates map and player movement things
         #terrain_handler = Map(self)
        player_handler = Player()
        self.monster_handler = Monster(self)

        # load sprites
        self.character_sprite = PhotoImage(file="sprites\Textures\character.png")
        self.wall_sprite = PhotoImage(file="sprites\Textures\wall.png")
        self.grass_full_sprite = PhotoImage(file="sprites\Textures\grass.png")
    
        
        # varables to store cords of things
        self.monster = []
        self.walls = []
        self.map_border=[]
        self.teleport = []
        self.grass_full = []
        self.terrain_cords_dict = {"walls":self.walls, "border":self.map_border,"teleport":self.teleport,"grass full":self.grass_full, "monster": self.monster}
        
        

        self.monster_movement_cords_dict = {"down": [], "up":[],"left": [], "right":[]}
        self.monster_down= self.monster_movement_cords_dict["down"]
        self.monster_up= self.monster_movement_cords_dict["up"]
        self.monster_left= self.monster_movement_cords_dict["left"]
        self.monster_right= self.monster_movement_cords_dict["right"]
        


        # binds arrow keys for moVEMENT        
        self.bind("<KeyPress>", lambda x : player_handler.key_press(x, self))
        self.focus_set()


        Map(self)
        
        self.bind('<Map>', lambda x : self.monster_loop(x))
           
        

        print(self.start)

        
      
        
        self.mainloop()

        #self.menu=Menu(self) opens new window 
        #terrain_handler.terrain_load("level 1",self)

    def monster_loop(self,event):
        
        
        self.monster_handler.move_monster_cords( self)
        
        self.after(2000, lambda: self.monster_loop(event))
        self.unbind('<Map>')
    def new_frame(self):
        self.canvas.delete("all")
        self.terrain_cords_dict = {"walls":self.walls, "border":self.map_border,"teleport":self.teleport,"grass full":self.grass_full, "monster": self.monster}

        
        self.update_terrain_pos()
        self.update_player_pos()
        
        
        
        
    def update_player_pos (self):
        player_viewport_x = VIEWPORT_SIZE // 2
        player_viewport_y = VIEWPORT_SIZE // 2
        self.canvas.create_image(player_viewport_x * GRID_SIZE, player_viewport_y * GRID_SIZE, 
                                 anchor='nw', image=self.character_sprite)
 
    def update_terrain_pos(self):
                
        top_left_x = self.player_pos[0] - VIEWPORT_SIZE // 2
        top_left_y = self.player_pos[1] - VIEWPORT_SIZE // 2
        
        
        for key, list in self.terrain_cords_dict.items():
            for x in range(VIEWPORT_SIZE):
                for y in range(VIEWPORT_SIZE):
                    map_x = top_left_x + x
                    map_y = top_left_y + y
                    if (map_x, map_y) in list:
                        if key == "walls":
                            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                    (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                    fill="grey" )
                            #self.canvas.create_image(x * GRID_SIZE, y * GRID_SIZE, 
                                # anchor='nw', image=self.wall_sprite)
                            
                        elif key == "border": 
                            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                    (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                    fill="black" )
                        elif key == "teleport": 
                            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                    (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                    fill="blue" )
                        elif key == "monster": 
                            print(" list of current monster cords" ,list)
                            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                                                    (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                                                    fill="red" )
        


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
            if  self.collision_check(new_x,new_y,game_instance):
                game_instance.player_pos = [new_x, new_y]
                game_instance.new_frame()
            

    def collision_check (self, new_x, new_y, game_instance):
        for key, list in game_instance.terrain_cords_dict.items():
            if key == "teleport":
                if (new_x,new_y) in list: 
                    self.teleport(game_instance)
                    print("telepro")
                    return False
            elif key =="monster":
                if (new_x,new_y) in list:
                    Battle(game_instance)
                    print("battle time")
                    return False
            elif key != "teleport" and key != "grass full":
                if (new_x,new_y) in list: 
                    return False
        return True
        
    def teleport(self,game_instance):
        game_instance.level_number = 2
        
        print("next lebvel")
        Map(game_instance)

        


    
    
class Map():
    def __init__(self, game_instance):
        
        game_instance.terrain_cords_dict = {"walls":[], "border":[],"teleport":[],"grass full":[], "monster": []}
        game_instance.walls = game_instance.terrain_cords_dict["walls"]
        game_instance.map_border= game_instance.terrain_cords_dict["border"]
        game_instance.teleport = game_instance.terrain_cords_dict["teleport"]
        game_instance.grass_full = game_instance.terrain_cords_dict["grass full"]
        game_instance.monster = game_instance.terrain_cords_dict["monster"]

        game_instance.player_pos = []

        self.spawn_location(game_instance)
        self.terrain_load(game_instance)
        game_instance.start = True
        


    def spawn_location (self, game_instance):
        game_instance.terrain_map= game_instance.map_storage[str(game_instance.level_number)]
        y_cord = 0
        for x_line in game_instance.terrain_map:
            x_cord = 0
            for obj in x_line:
                if obj == "x": 
                    game_instance.player_pos = [x_cord,y_cord]
                    print("spawn pos found")
                    return
                x_cord+=1
            y_cord+=1
        if not game_instance.player_pos:
            game_instance.player_pos = [MAP_SIZE // 2, MAP_SIZE // 2]
            print('error loadinng in spawn pos')


    def terrain_load(self,game_instance):
        y_cord = 0
        print("stawrt")
        for x_line in game_instance.map_storage[str(game_instance.level_number)]:
            print(y_cord)
            x_cord = 0
            for obj in x_line:
                if (x_cord,y_cord) != tuple(game_instance.player_pos):
                    print(obj)
                    if obj == "w": 
                        game_instance.walls.append((x_cord,y_cord))
                    elif obj == "=":
                        game_instance.map_border.append((x_cord,y_cord))
                    elif obj == "T": 
                        game_instance.teleport.append((x_cord,y_cord))
                    elif obj == ".":
                        game_instance.grass_full.append((x_cord,y_cord))
                    elif obj == "M":
                        print('mosnter added')
                        game_instance.monster.append((x_cord,y_cord))
                x_cord+=1
                
            y_cord+=1
        
        game_instance.monster_handler.monster_path_load(game_instance)
        game_instance.new_frame()
        print('terrain loaded in')
        
        
class Cutscreens ():
    def __init__(self) -> None:
        pass

class Monster(): 
    
    def __init__(self, game_instance) :
        pass
         
        
    def monster_path_load(self, game_instance):
        y_cord = 0
        for x_line in game_instance.monster_path_storage[str(game_instance.level_number)]:
            x_cord = 0 
            for obj in x_line: 
                if obj == "D": 
                    game_instance.monster_movement_cords_dict["down"].append((x_cord,y_cord))
                elif obj == "U": 
                    game_instance.monster_movement_cords_dict["up"].append((x_cord,y_cord))
                elif obj == "L": 
                    game_instance.monster_movement_cords_dict["left"].append((x_cord,y_cord))
                elif obj == "R": 
                    game_instance.monster_movement_cords_dict["right"].append((x_cord,y_cord))
                x_cord += 1
            y_cord += 1
            print(game_instance.monster_movement_cords_dict)


    def move_monster_cords(self, game_instance): 

        for monster_cord in game_instance.monster: 
            print("old monster cord" + str(monster_cord))
            direction = {"down": (monster_cord[0],monster_cord[1]+1),
                         "up": (monster_cord[0],monster_cord[1]-1),
                         "left": (monster_cord[0]-1,monster_cord[1]),
                         "right": (monster_cord[0]+1,monster_cord[1])}
            
            for key, list in game_instance.monster_movement_cords_dict.items():
                for direction_cord in list: 
                    if tuple(direction_cord) == monster_cord: 
                        print("found " , key)
                        
                        new_monster_cord = direction[key]
                        if not self.collison_check(new_monster_cord, game_instance):
                       
                            print("new monster cords", new_monster_cord)
                            print("monster list" ,game_instance.monster)
                            game_instance.monster.remove(monster_cord)
                            game_instance.monster.append(new_monster_cord)
                        
                        
                        print("monster list after" ,game_instance.monster)
                        #if not self.collison_check(new_monster_cord, game_instance): 
        
            
        game_instance.new_frame()
                        


           
           
            
            
            
    
    def collison_check(self, new_monster_cord, game_instance): 
        new_x, new_y = new_monster_cord[0], new_monster_cord[1]

        for key, list in game_instance.terrain_cords_dict.items():
            
            if key != "teleport" and key != "grass full":
                
                if (new_x,new_y) == tuple(game_instance.player_pos):
                    Battle(game_instance)
                    print("battle time monster col")
                    return "battle time"
                elif (new_x,new_y) in list: 

                    print('hit something ')
                    return True
    
        return False


    
class Battle():
    def __init__(self, game_instance):    
        game_instance.canvas.delete("all")
        game_instance.canvas.configure(bg="red")
        game_instance.canvas.create_rectangle(0,0,1 *GRID_SIZE,1*GRID_SIZE ,fill="grey" )
            

class Menu(): 
    def __init__(self, game_instance):
        pass

class fake_ass_menu(Tk):
    def __init__(self, game_instance):
        super().__init__()
        

        self.geometry('200x200')
        self.configure(background = "blue")




Game()


"""
        #self.player = self.canvas.create_rectangle(0, 0, GRID_SIZE, GRID_SIZE, fill="blue")

        for i in range(40):
            line = ""
            for a in range (40):
                line += "."
            print (line)
        """
            
        