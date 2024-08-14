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
       
       
       #opening files
        with open("game_data.json") as file: 
            self.game_data =  json.load(file)
        
        with open("map_data.json") as file: 
            self.map_storage =  json.load(file)
        
        with open("monster_path_data.json") as file: 
            self.monster_path_file = json.load(file)
        
        
         #setting up game screen, canvas
        self.geometry(f"1000x800")
        self.configure(background= "black")
        self.resizable(False, False)      
        
        self.player_data = {"position": [],
                            "health": 400,
                            "level": 1, 
                            "score": 0,
                            "items": {"mini heal": 10, "wooden sword": 10}}
        
        
        
        '''
        
        Login page
        
        '''
        
        
        Label(self, text= "Login page").pack()
        
        username_var = StringVar()
        username_entry = Entry(self, textvariable=username_var)
        username_entry.pack()        
        
        password_var = StringVar()
        password_entry = Entry(self, textvariable= password_var)
        password_entry.pack()
        
        
        Button(self, text ="login", command= lambda: self.login(username=username_var.get(), password= password_var.get(),new_user=False)).pack()
        Button(self, text ="New Account", command= lambda: self.login(username=username_var.get(), password= password_var.get(),new_user=True)).pack()
        
        self.login_text = StringVar()
        Label(self, textvariable= self.login_text).pack()


        self.mainloop()
        
        

        #self.fake_ass_menu=Menu(self) opens new window 
        #terrain_handler.terrain_load("level 1",self)

    def login(self,username: str, password: str, new_user: bool): 
        with open("player_data.json", "r") as f: 
            file = json.load(f)
            f.close()
        if password != "" and username != "":
            if not new_user:
                if username in file.keys():
                    if file[username]["password"] == password:
                        self.player_data = file[username]["data"]
                        print("login successful")
                        self.load_game(new_user= False, username = username) 
                        
                    else: 
                        self.login_text.set("wrong password to account")
                else:
                    self.login_text.set("not in saved accounts, make new account")
                    
            elif new_user:
                file[username] = {
                "password" : str(password), 
                "data": 
                    {
                        "position": [],
                        "health": 400,
                        "level": 1, 
                        "score": 0,
                        "items": {"mini heal": 10, "wooden sword": 10}
                    }}
                
                with open("player_data.json", 'w') as outfile: json.dump(file, outfile, indent= 5)
                self.load_game(new_user= False, username = username) 
                print("new accoutn made")
        else: 
            self.login_text.set("enter username and password")
            
        
        

            
                
    
    
    def load_game(self, new_user: bool , username: str):
        
        
        for widgets in self.winfo_children():
            widgets.destroy()
        
        self.canvas = Canvas(self, width=WINDOW_SIZE_WIDTH, height=WINDOW_SIZE_HEIGHT, bg="green")
        self.canvas.pack(padx=10)
        self.menu_frame = Frame(self, bg= "purple")
        self.menu_frame.pack(expand=TRUE, fill=BOTH)
        
        
        self.player_pos = [] 
        self.movement_allowed = True
        self.game_cycle = 0 

        self.player_direction = "none"

        

        self.terrain_cord_dict = {}
        self.monster_movement_dict = {"U" :[], 
                                      "D" :[], 
                                      "L": [],
                                      "R": []}
        # load map data 
        self.map_handler = Map(parent=self, terrain_cord_dict= self.terrain_cord_dict, player_data= self.player_data, monster_movement_dict = self.monster_movement_dict)

        self.map_handler.reset_cord_storage()
        self.map_handler.terrain_load()
        self.map_handler.monster_path_load()
        
        #auto save setup stuff
        
        if  new_user:
            with open("player_data.json", "r") as file: data =  json.load(file)
            for monster_name in self.game_data["monster data"].keys():
                self.terrain_cord_dict[monster_name] = data[username]["save data"][monster_name]
                
        self.auto_save(username=username)
        
       
        # load sprites
        self.sprite_dict = {"Textures":{}, "UI":{}, "Battle": {}}
        
        folder_names =os.listdir(SPRITE_FOLDER_PATH)
    
        
        for folder in folder_names:
            path = {"Textures": TEXTURE_FOLDER_PATH, 
                    "UI": UI_FOLDER_PATH, 
                    "Battle": BATTLE_FOLDER_PATH}.get(folder)

            for file in os.listdir(path):
                self.sprite_dict[folder][file] = create_sprites(path = path , name = file)
        
    
  
        # binds arrow keys for moVEMENT        
        self.bind("<KeyPress>", lambda x : self.key_press(x))
        self.bind("<KeyRelease>", lambda x : self.key_release(x))

        
        self.load_main_menu()
        self.game_loop()
        self.new_frame()
    
    
    def auto_save(self,username:str): 
        
        with open("player_data.json", "r") as file: 
            data =  json.load(file)
        
        monster_dict = {}
        for monster_name in self.game_data["monster data"].keys():
            monster_dict[monster_name] =  self.terrain_cord_dict[monster_name]
        

        data[username]["save data"] = monster_dict
        data[username]["data"] = self.player_data
        

        with open("player_data.json", "w") as outfile: 
            json.dump(data, outfile, indent=4)
            print("done")

        self.after(5000, lambda: self.auto_save(username=username))
       
        
        
    def load_main_menu (self): 
        
        
        Label(self.menu_frame, text="Main Menu", font =("Arial",25)).pack(padx=50)
        self.player_data_label = Label(self.menu_frame, text=self.player_data, font =("Arial",18),wraplength=800)
        self.player_data_label.pack(padx=50)

    def key_press (self, event):      
        self.player_direction = event


    def key_release (self, event):
        print("keyrealease")
        
        self.player_direction = "none"


    

    def monster_movement (self): 
        for key, list in self.monster_movement_dict.items():  
            try:
                for monster in self.game_data["monster data"].keys():
                    for monster_cord in self.terrain_cord_dict[monster]:
                        if (monster_cord[0],monster_cord[1])  in list:
                        

                            new_monster_cord = {"D": (monster_cord[0],monster_cord[1]+1),
                                        "U": (monster_cord[0],monster_cord[1]-1),
                                        "L": (monster_cord[0]-1,monster_cord[1]),
                                        "R": (monster_cord[0]+1,monster_cord[1])}.get(key)
                            
                            self.terrain_cord_dict[monster].remove(monster_cord)
                            self.terrain_cord_dict[monster].insert(0,new_monster_cord)
            except KeyError: 
                continue

        
    def game_loop(self):
        self.monster_movement()

        result = self.player_movement(self.player_direction)
        if result == None: pass
        elif result[0] in self.game_data["monster data"].keys():
            self.movement_allowed = False
            self.canvas.create_image(10 * GRID_SIZE, 6 * GRID_SIZE, 
                                 anchor=NW, image=self.sprite_dict["Textures"]['exclamation mark.png'])
            Battle(parent = self,monster_cord= result[1], sprite_dict=self.sprite_dict, monster_name= result[0], data = self.player_data)
        
            return 
            
        elif result[0] == "teleport": 
            self.map_handler.next_level()
            self.game_loop()
            self.new_frame()
            return
        elif result[0] == "wall" or result [0] == "border":
            pass 
        elif result[0] == True:
            self.player_data["position"] = result[1]
        #hit wall so no movement 
    
        if self.movement_allowed:
            self.player_data_label.config(text=self.player_data)
            self.new_frame()
            self.after(25, lambda : self.game_loop())
                    

    def player_movement( self, event):
        
        pixel_dist = 5
        direction = (0,0) if event == "none" else{
            "Up": (0, -pixel_dist),
            "Down": (0, pixel_dist),
            "Left": (-pixel_dist, 0),
            "Right": (pixel_dist, 0)
        }.get(event.keysym) 
        
        if direction == None: 
            return None
        else:
            new_x = self.player_data["position"][0] + direction[0]
            new_y = self.player_data["position"][1] + direction[1]
            collision = self.collision_check(new_x,new_y)
            return collision
       
            
        
    def collision_check (self, new_x, new_y):
        for key, list in self.terrain_cord_dict.items():
            if key not in self.game_data["terrain states"]["non solids"]:
                for value in list: 
                    obj_x = value[0]
                    obj_y = value[1]
                    
                    if new_x in range(obj_x-30, obj_x +30) and new_y in range(obj_y-30, obj_y +30) and key != "grass" and (abs(obj_y -new_y)!=GRID_SIZE ) and abs(obj_x -new_x)!=GRID_SIZE:
                        
                        if key in self.game_data["monster data"].keys() : 
                            print("monster")
                            return key, (obj_x, obj_y)
                        else: 
                            return (key,)
                  
        return (True, (new_x, new_y))



    def new_frame(self):
        self.canvas.configure(bg="green")
        self.canvas.delete("all")
        top_left_x = self.player_data["position"][0] - 10*GRID_SIZE # pos -10
        top_left_y = self.player_data["position"][1] - 7*GRID_SIZE  #pos - 7

        x_min = top_left_x - GRID_SIZE
        x_max = top_left_x + WINDOW_SIZE_WIDTH + 1
        y_min = top_left_y - GRID_SIZE
        y_max = top_left_y + WINDOW_SIZE_HEIGHT + 1

        
        
        #for key, value_list in self.terrain_cord_dict.items(): 
         #   if key in self.game_data["monster data"].keys()
        x = []
        for key, value_list in self.terrain_cord_dict.items():
            if key in self.game_data["terrain states"]["non solids"]:
                x.insert(0,(key, value_list))
            else:
                x.append((key, value_list))
        
        
        for key, value_list in x:
            
            
            for value in value_list:
              
                if x_min <= value[0] < x_max and y_min <= value[1] < y_max  and key != "grass": # remember to change this !!!!
                    
                    
                    
                    self.canvas.create_image(
                        value[0] - top_left_x,
                        value[1] - top_left_y,
                        anchor='nw',
                        image=self.sprite_dict["Textures"][f"{key}.png"]
                    )
        
        self.canvas.create_image(10 * GRID_SIZE, 7 * GRID_SIZE, 
                                 anchor=NW, image=self.sprite_dict["Textures"]['character.png'])

                            
class Map():

    def __init__(self, parent, terrain_cord_dict, player_data, monster_movement_dict):
        
        super().__init__()
        
        self.game_instance = parent
        
        self.player_data = player_data
        self.terrain_cord_dict = terrain_cord_dict
        self.monster_movement_dict = monster_movement_dict
        
        with open("monster_path_data.json", "r") as file: 
            self.monster_path_file = json.load(file)

        


    def delete_monster_cord(self, monster_cord, name):
        for cord in self.terrain_cord_dict[name]: 
            if monster_cord == cord: 

                self.terrain_cord_dict[name].remove(monster_cord)
                return
    def monster_path_load(self):

        direction = { 
            "D" : [(0,1), (0, 40)],
            "U" : [(0,1), (-39, 1)],
            "L" : [(-39, 1), (0, 1)],
            "R" : [(0, 40), (0, 1)]
        }

        y_cord = 0
        for x_line in self.monster_path_file[str(self.player_data["level"])]:
            x_cord = 0 
            for obj in x_line: 

                if obj == "D" or obj == "U" or obj ==  "L"  or obj == "R":

                    x_start, x_end = direction.get(obj)[0][0],direction.get(obj)[0][1]
                    y_start, y_end = direction.get(obj)[1][0],direction.get(obj)[1][1]
                    
                    tuple_range = [(x_cord+x, y_cord+y) for x in range(x_start, x_end) for y in range(y_start, y_end)]
                    
                    self.monster_movement_dict[obj].extend(tuple_range)
                    
                x_cord += GRID_SIZE
            y_cord += GRID_SIZE

    def next_level (self): 
        self.player_data["level"]+= 1
        self.player_data["position"] = []
        self.reset_cord_storage()
        self.terrain_load()
        self.monster_path_load()
        
        
    
    def reset_cord_storage (self):
        
        file_list = os.listdir(TEXTURE_FOLDER_PATH)

        for file_name in file_list: 

            self.terrain_cord_dict[file_name.replace(".png", "")] = []
        for key in self.monster_movement_dict: 
            self.monster_movement_dict[key] = [] 


    
        

    def terrain_load(self):
        with open("game_data.json", "r") as file: 
            codes =  json.load(file)["terrain codes"]
        y_cord = 0
        
        for x_line in self.game_instance.map_storage[str(self.player_data["level"])]:
           
            x_cord = 0
            for obj in x_line:
                if (x_cord*40,y_cord*40) != tuple(self.player_data["position"]):
                    
                    #self.terrain_cord_dict["grass"].append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                    sprite_name = codes.get(obj)
                    if sprite_name in self.game_instance.game_data["monster data"].keys() or sprite_name == "teleport":
                        self.terrain_cord_dict[sprite_name].append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                        self.terrain_cord_dict["grass"].append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                    elif sprite_name == "spawn": 
                        self.player_data["position"] = [x_cord*GRID_SIZE,y_cord*GRID_SIZE]
                        self.terrain_cord_dict["grass"].append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                    else:
                        self.terrain_cord_dict[sprite_name].append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                
                else: 
                    print('at player pos')
                x_cord+=1 
            y_cord+=1        
        
        print()
        print('terrain loaded in')
        

    




class Cutscreens ():
    def __init__(self) -> None:
        pass



class fake_ass_menu(Tk):
    def __init__(self, game_instance):
        super().__init__()
        

        self.geometry('200x200')
        self.configure(background = "blue")

    

Game()
            
        