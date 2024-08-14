from  tkinter import *
from tkinter.ttk import *
import threading, time, json
import time
from battle import *        

import os 

PROGRAM_PATH = os.getcwd() # Store the program's path to access essential folders.
SPRITE_FOLDER_PATH=PROGRAM_PATH+"/Sprites" # Store path to sprites folder.
TEXTURE_FOLDER_PATH=PROGRAM_PATH+"/Sprites/Textures" # Store path to texture folder.
BATTLE_FOLDER_PATH=PROGRAM_PATH+"/Sprites/Battle" # Store path to texture folder.
UI_FOLDER_PATH=PROGRAM_PATH+"/Sprites/UI" # Store path to texture folder.


DATA_FOLDER_PATH=PROGRAM_PATH+"/Data" # Store path to data folder. 

MAP_SIZE = 40 
WINDOW_SIZE_HEIGHT = 600  
WINDOW_SIZE_WIDTH = 840  
GRID_SIZE = 40
VIEWPORT_SIZE_HEIGHT = WINDOW_SIZE_HEIGHT // GRID_SIZE  # 15
VIEWPORT_SIZE_WIDTH = WINDOW_SIZE_WIDTH // GRID_SIZE # 21



def create_sprites ( **kwargs): 
        image = None 
        try: 
            path = kwargs["path"]+f"/{kwargs['name']}"
            image = PhotoImage(file=path)
        except : 
            print('load error')
            pass
        return image






class Game(Tk):
    def __init__(self):
        
        super().__init__()
       
        
        with open("map_data.json") as file: 
            self.map_storage =  json.load(file)
        with open("monster_path_data.json") as file: 
            self.monster_path_storage = json.load(file)

        

        self.level_number = 1
        self.player_pos = [] 
        self.movement_allowed = True
        self.game_cycle = 0 

        self.player_direction = "none"
        
        self.terrain_map= self.map_storage[str(self.level_number)]
        self.monster_path_map= self.monster_path_storage[str(self.level_number)]

        
       
        #setting up game screen, canvas
        self.geometry(f"1000x800")
        self.configure(background= "yellow")
        self.resizable(False, False)      
        self.canvas = Canvas(self, width=WINDOW_SIZE_WIDTH, height=WINDOW_SIZE_HEIGHT, bg="green")
        self.canvas.pack(padx=10)
        self.menu_frame = Frame(self, bg= "blue")
        self.menu_frame.pack(expand=TRUE, fill=BOTH)

        
        self.load_main_menu()


        self.map_handler = Map(self)

        # load sprites
        self.sprite_dict = {"Textures":{}, "UI":{}, "Battle": {}}
        
        folder_names =os.listdir(SPRITE_FOLDER_PATH)
        print(folder_names)
        
        for folder in folder_names:
            path = {"Textures": TEXTURE_FOLDER_PATH, 
                    "UI": UI_FOLDER_PATH, 
                    "Battle": BATTLE_FOLDER_PATH}.get(folder)
            print(path)
            print(os.listdir(path))

            for file in os.listdir(path):
                
                self.sprite_dict[folder][file] = create_sprites(path = path , name = file)
        

            
        #self.sprite_dict['character'] = create_sprites(name= 'character')
  
        # binds arrow keys for moVEMENT        
        self.bind("<KeyPress>", lambda x : self.key_press(x))
        self.bind("<KeyRelease>", lambda x : self.key_release(x))

        self.game_loop()
        self.new_frame()
        self.mainloop()
        
        

        #self.fake_ass_menu=Menu(self) opens new window 
        #terrain_handler.terrain_load("level 1",self)


    def load_main_menu (self): 
        
        Label(self.menu_frame, text="Main Menu", font =("Arial",25)).pack(padx=50)

    def key_press (self, event):      
        self.player_direction = event


    def key_release (self,event):
        print("keyrealease")
        
        self.player_direction = "none"

    
        
        
    def entering_battle(self,monster_cord): 
        self.movement_allowed = False
        self.canvas.create_image(10 * GRID_SIZE, 6 * GRID_SIZE, 
                                 anchor=NW, image=self.sprite_dict["Textures"]['exclamation mark.png'])
        Battle(parent = self,monster_cord= monster_cord,sprite_dict=self.sprite_dict)
        
       

    def game_loop(self):
        
        

        self.monster_movement()

        result = self.player_movement(self.player_direction)
        if result == None: pass
        elif result[0] == "monster" :
            self.entering_battle(result[1])
            #self.after(3000, lambda : self.entering_battle(result[1]))
            return 
            
        elif result[0] == "teleport": 
            self.map_handler.next_level()
            self.map_handler.monster_path_load()
            self.new_frame()
            return
        elif result[0] == "wall" or result [0] == "border":
            pass 
        elif result[0] == True:
            self.player_pos = result[1]
        #hit wall so no movement 
    
        if self.movement_allowed:
            
            self.new_frame()
            self.after(25, lambda : self.game_loop())

    def monster_movement (self): 
        for key, list in self.monster_movement_cords_dict.items():  
            
            for monster_cord in self.terrain_cords_dict["monster"]:

                if (monster_cord[0],monster_cord[1])  in list:

                    new_monster_cord = {"D": (monster_cord[0],monster_cord[1]+1),
                                "U": (monster_cord[0],monster_cord[1]-1),
                                "L": (monster_cord[0]-1,monster_cord[1]),
                                "R": (monster_cord[0]+1,monster_cord[1])}.get(key)
                    
                    self.monster.remove(monster_cord)
                    self.monster.insert(0,new_monster_cord)
                    

    def player_movement( self, event):
        
        pixel_dist = 5
        direction = (0,0) if event == "none" else{
            "Up": (0, -pixel_dist),
            "Down": (0, pixel_dist),
            "Left": (-pixel_dist, 0),
            "Right": (pixel_dist, 0)
        }.get(event.keysym) 
        try:
            new_x = self.player_pos[0] + direction[0]
            new_y = self.player_pos[1] + direction[1]

            collision = self.collision_check(new_x,new_y)
            return collision
        except TypeError:
            return None
            
        
    def collision_check (self, new_x, new_y):
        for key, list in game_instance.terrain_cords_dict.items():
            if key != "grass":
                for value in list: 
                    obj_x = value[0]
                    obj_y = value[1]
                    
                    if new_x in range(obj_x-30, obj_x +30) and new_y in range(obj_y-30, obj_y +30) and key != "grass" and (abs(obj_y -new_y)!=GRID_SIZE ) and abs(obj_x -new_x)!=GRID_SIZE:
                        
                        print(abs(obj_x - new_x))
                        
                        
                        if key == "monster": 
                            print("monster")
                            return "monster", (obj_x, obj_y)
                        else: 
                            return (key,)
                            
        return (True, (new_x, new_y))



    def new_frame(self):
        self.canvas.configure(bg="green")
        self.canvas.delete("all")
        top_left_x = self.player_pos[0] - 10*GRID_SIZE # pos -10
        top_left_y = self.player_pos[1] - 7*GRID_SIZE  #pos - 7

        x_min = top_left_x - GRID_SIZE
        x_max = top_left_x + WINDOW_SIZE_WIDTH + 1
        y_min = top_left_y - GRID_SIZE
        y_max = top_left_y + WINDOW_SIZE_HEIGHT + 1

        for key, value_list in self.terrain_cords_dict.items():
            if key != 'grass':
                for value in value_list:
                    if x_min <= value[0] < x_max and y_min <= value[1] < y_max:
                        self.canvas.create_image(
                            value[0] - top_left_x,
                            value[1] - top_left_y,
                            anchor='nw',
                            image=self.sprite_dict["Textures"][f"{key}.png"]
                        )
        
        self.canvas.create_image(10 * GRID_SIZE, 7 * GRID_SIZE, 
                                 anchor=NW, image=self.sprite_dict["Textures"]['character.png'])

                            
class Map():
    def __init__(self, x):
        global game_instance
        game_instance = x
        
        game_instance.player_pos = []
        self.reset_cord_storage()
        self.spawn_location()
        self.terrain_load()
        self.monster_path_load()

    def delete_monster_cord(self, monster_cord):
        for cord in game_instance.monster: 
            if monster_cord == cord: 
                print('deleted')
                game_instance.monster.remove(monster_cord)
                return


    def monster_path_load(self):
        
        direction = { 
            "D" : [(0,1), (0, 40)],
            "U" : [(0,1), (-39, 1)],
            "L" : [(-39, 1), (0, 1)],
            "R" : [(0, 40), (0, 1)]
        }


        

  

        y_cord = 0
        for x_line in game_instance.monster_path_storage[str(game_instance.level_number)]:
            x_cord = 0 
            for obj in x_line: 

                if obj == "D" or obj == "U" or obj ==  "L"  or obj == "R":

                    x_start, x_end = direction.get(obj)[0][0],direction.get(obj)[0][1]
                    y_start, y_end = direction.get(obj)[1][0],direction.get(obj)[1][1]
                    
                    tuple_range = [(x_cord+x, y_cord+y) for x in range(x_start, x_end) for y in range(y_start, y_end)]
                    
                    game_instance.monster_movement_cords_dict[obj].extend(tuple_range)
                    
                x_cord += GRID_SIZE
            y_cord += GRID_SIZE
        
        print("new monster path loaded in ")
        
    def next_level (self): 
        game_instance.level_number= 2
        game_instance.player_pos = []
        self.reset_cord_storage()
        self.spawn_location()
        self.terrain_load()
        game_instance.game_loop()
        
    
    def reset_cord_storage (self):
        
        game_instance.terrain_cords_dict = {"wall":[], 
                                   "border":[],
                                   "teleport":[],
                                   "grass":[], 
                                   "monster": []}
        game_instance.monster = game_instance.terrain_cords_dict["monster"]
        game_instance.wall = game_instance.terrain_cords_dict["wall"]
        game_instance.map_border =game_instance.terrain_cords_dict["border"]
        game_instance.teleport = game_instance.terrain_cords_dict["teleport"]
        game_instance.grass_full = game_instance.terrain_cords_dict["grass"]
        
        
        game_instance.monster_movement_cords_dict = {"D":[], 
                                            "U":[],
                                            "L": [], 
                                            "R":[]}
        
        game_instance.monster_down=  game_instance.monster_movement_cords_dict["D"]
        game_instance.monster_up= game_instance.monster_movement_cords_dict["U"]
        game_instance.monster_left= game_instance.monster_movement_cords_dict["L"]
        game_instance.monster_right= game_instance.monster_movement_cords_dict["R"]


    def spawn_location (self):
        game_instance.terrain_map= game_instance.map_storage[str(game_instance.level_number)]
        y_cord = 0
        for x_line in game_instance.terrain_map:
            x_cord = 0
            for obj in x_line:
                if obj == "x": 
                    game_instance.player_pos = [x_cord*GRID_SIZE,y_cord*GRID_SIZE]
                    game_instance.grass_full.append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                    print("spawn pos found")
                    
                    return
                x_cord+=1
            y_cord+=1
        if not game_instance.player_pos:
            game_instance.player_pos = [MAP_SIZE // 2, MAP_SIZE // 2]
            print('error loadinng in spawn pos')


    def terrain_load(self):
        y_cord = 0
    
        for x_line in game_instance.map_storage[str(game_instance.level_number)]:
           
            x_cord = 0
            for obj in x_line:
                if (x_cord,y_cord) != tuple(game_instance.player_pos):
                    
                    if obj == "." or obj == "M" or obj == "x":
                        game_instance.grass_full.append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                        
                    if obj == "w": 
                        game_instance.wall.append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                    if obj == "=":
                        game_instance.map_border.append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                    if obj == "T": 
                        game_instance.teleport.append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                    if obj == "M":
                        print('mosnter added')
                        game_instance.monster.append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                    
                x_cord+=1
                
            y_cord+=1
        
        print('terrain loaded in')

    

class Math():
    def __init__(self,x) :
        global game_instance 
        game_instance =x

    def check_answer (self,var1, var2,user_answer): 
        if var1 + var2 == user_answer: 
            return True
        else: 
            return False
    def create_question (self): 

        var1 = random.randint(1,10)
        var2 = random.randint(1,10)
        game_instance.math_question_label.config(text=f"{var1}+{var2}")
        return var1, var2



class Cutscreens ():
    def __init__(self) -> None:
        pass



class fake_ass_menu(Tk):
    def __init__(self, game_instance):
        super().__init__()
        

        self.geometry('200x200')
        self.configure(background = "blue")

    

Game()
            
        