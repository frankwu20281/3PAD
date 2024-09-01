"""
Code created by Frank Wu 
"""

# Import modules that the game needs to be able to work.
from  tkinter import *
from tkinter.ttk import *
from battle import *        
import  json, os



PROGRAM_PATH = os.getcwd() # Store the program's path to access essential folders.
SPRITE_FOLDER_PATH=PROGRAM_PATH+"/Sprites" # Store path to sprites folder.
TEXTURE_FOLDER_PATH=PROGRAM_PATH+"/Sprites/Textures" # Store path to texture folder.
BATTLE_FOLDER_PATH=PROGRAM_PATH+"/Sprites/Battle" # Store path to monster battling textures folder.
UI_FOLDER_PATH=PROGRAM_PATH+"/Sprites/UI" # Store path to UI textures folder.


DATA_FOLDER_PATH=PROGRAM_PATH+"/Data" # Store path to data folder. 

FPS = 40
MAP_SIZE = 40 
WINDOW_SIZE_HEIGHT = 600  
WINDOW_SIZE_WIDTH = 840  
GRID_SIZE = 40
VIEWPORT_SIZE_HEIGHT = WINDOW_SIZE_HEIGHT // GRID_SIZE  # 15
VIEWPORT_SIZE_WIDTH = WINDOW_SIZE_WIDTH // GRID_SIZE # 21
BG_COLOUR = "#2b7d9b"
ACCENT_COLOUR = "#191919"
LOGIN_UI_COLOUR = "#323645"



def create_sprites (path:str, name:str): 
    """
    Create a sprite image from a file.

    Args:
       
        - path (str): Path to the folder containing the image.
        - name (str): Name of the image file.

    Returns:
        PhotoImage: The loaded image, or None if the image couldn't be loaded.
    """

    image = None 
    try: 
        path = path+f"/{name}"
        image = PhotoImage(file=path)
    except : 
        print('load error')
        pass
    return image


class Game(Tk):
    """
    The main class for the game, login screen, most of the backend components and map exporation code 
    is found in this class.

    Args:
        Tk : Lets the class use functions from the Tkinter and Tkinter.ttk modules 
    """
    
    def __init__(self):
        """
        Runs when game is started up. Loads all necessary Json files and creates login page for user to login to game
        
        """
        super().__init__()
       
       
       #opening files
        with open("game_data.json") as file: 
            self.game_data =  json.load(file)
        
        
        
         #setting up game screen, canvas
         
        
        self.geometry(f"1000x800")
        self.configure(background= "Black")
        self.resizable(False, False)      
        self.title("Number Beasts")
        
        self.player_data = {"position": [],
                            "health": 600,
                            "level": 1, 
                            "score": 0,
                            "high score": 0,
                            "deaths": 0,
                            "items": {"mini heal": 10, "wooden sword": 10, "insta kill": 100}}
        
        # load sprites
        self.sprite_dict = {"Textures":{}, "UI":{}, "Battle": {}}
        
        folder_names =os.listdir(SPRITE_FOLDER_PATH)
    
        
        for folder in folder_names:
            path = {"Textures": TEXTURE_FOLDER_PATH, 
                    "UI": UI_FOLDER_PATH, 
                    "Battle": BATTLE_FOLDER_PATH}.get(folder)

            for file in os.listdir(path):
                self.sprite_dict[folder][file] = create_sprites(path = path , name = file)
        
        '''
        
        Login page
        
        '''
        
        login_canvas = Canvas(self)
        login_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        login_canvas.create_image(0,0,anchor = "nw", image = self.sprite_dict["UI"]["login background.png"])
        
        login_frame = Frame(login_canvas, bg= ACCENT_COLOUR)
        login_frame.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.7)
        
        
        
        Label(login_frame, text= "Login page", font= ("Arial", 28, "bold"), anchor=CENTER, bg= ACCENT_COLOUR, fg="#cabfcf").place(relx=0.2, rely=0.1, relheight=0.1, relwidth=0.6) 
        
        Label(login_frame, text= "Username:", font= ("Arial", 18, "bold"), anchor=CENTER, bg= ACCENT_COLOUR, fg="#cabfcf" ).place(relx=0.1, rely=0.3, relheight=0.1, relwidth=0.3) 
        username_var = StringVar()
        username_var.set(1)
        username_entry = Entry(login_frame, textvariable=username_var, font= ("Arial", 18), bg= LOGIN_UI_COLOUR, fg="#cabfcf" )
        username_entry.place(relx=0.55, rely=0.3, relheight=0.1, relwidth=0.4) 
        
        Label(login_frame, text= "Password:", font= ("Arial", 18, "bold"), anchor=CENTER, bg= ACCENT_COLOUR, fg="#cabfcf" ).place(relx=0.1, rely=0.5, relheight=0.1, relwidth=0.3) 
        password_var = StringVar()
        password_var.set(1)
        password_entry = Entry(login_frame, textvariable= password_var, font= ("Arial", 18), bg= LOGIN_UI_COLOUR, fg="#cabfcf" )
        password_entry.place(relx=0.55, rely=0.5, relheight=0.1, relwidth=0.4) 
        
        Button(login_frame, text ="New Account", command= lambda: self.login(username=username_var.get(), password= password_var.get(),new_user=True), bg= LOGIN_UI_COLOUR, fg="#cabfcf", font= ("Arial",14, "bold") ).place(relx=0.1, rely=0.8, relheight=0.1, relwidth=0.3) 
        Button(login_frame, text ="Login", command= lambda: self.login(username=username_var.get(), password= password_var.get(),new_user=False), bg= LOGIN_UI_COLOUR, fg="#cabfcf" , font= ("Arial",14, "bold")).place(relx=0.6, rely=0.8, relheight=0.1, relwidth=0.3) 

        self.login_text = StringVar()
        
        Label(login_frame, textvariable= self.login_text, font= ("Arial", 14), wraplength= 450, bg= ACCENT_COLOUR, fg="#cabfcf" ).place(relx=0.1, rely=0.65, relheight=0.1, relwidth=0.8) 


        self.mainloop()

    def login(self,username: str, password: str, new_user: bool): 
        """ 
        Deals with user login and new account creation.

        Args:
            username (str): Username which the user inputed.
            password (str): Password which the user inputed.
            new_user (bool): Tells function if user is logging in or making new account.
        """
        username = username.rstrip()
        password = password.rstrip()
        print(new_user, "new user")
        with open("player_data.json", "r") as f: 
            file = json.load(f)
        
        if password != "" and username != "":
            if " " in username or "'" in username or '"' in username:
                     self.login_text.set("Username cannot include spaces or speech marks")
                     return
                
            if " " in password or "'" in password or '"' in password:
                self.login_text.set("Password cannot include spaces or speech marks")
                return
            
            if  new_user == False:
                if username in file.keys():
                    if file[username]["password"] == password:
                        self.player_data = file[username]["data"]
                        
                        if file[username]["data"]["health"] > 0:
                            print("login successful")
                            self.load_game(new_user= False, username = username) 
                        else:
                            self.player_data = {"position": self.player_data["position"],
                            "health": 400,
                            "level": 1, 
                            "score": 0,
                            "high score": self.player_data["high score"] if self.player_data["score"]< self.player_data["high score"] else self.player_data["score"], 
                            "deaths": self.player_data["deaths"]+1,
                            "items": {"mini heal": 10, "wooden sword": 10}}
                            print('health lower than 0 so game reset')
                            self.load_game(new_user= True, username = username) 
                        
                    else: 
                        self.login_text.set("Wrong password to account!")
                else:
                    self.login_text.set("This username has not been saved, click 'New Account' button to login as new player!")
                    
            elif new_user == True:
                
                
                if username not in file.keys():
                    file[username] = {
                    "password" : str(password), 
                    "data": 
                        {
                            "position": [],
                            "health": 400,
                            "level": 1, 
                            "score": 0,
                            "high score" : 0,
                            "deaths": 0,
                            "items": {"mini heal": 10, "wooden sword": 10}
                        }, 
                    "save data": {}
                    }
                    with open("player_data.json", 'w') as outfile: json.dump(file, outfile, indent= 5)
                    self.load_game(new_user= True, username = username) 
                    print("new accoutn made")
                else: 
                    self.login_text.set("Account has already been saved, please login")
        else: 
            self.login_text.set("Please enter both username and password")
            

    
    def load_game(self, new_user: bool , username: str):
        """
        Loads the map exporation part of the game after user has finished logging in.

        Args:
            new_user (bool): New account or previous account logging in.
            username (str): Username of player.
        """
        
        for widgets in self.winfo_children():
            widgets.destroy()
        
        self.canvas = Canvas(self, width=WINDOW_SIZE_WIDTH, height=WINDOW_SIZE_HEIGHT, bg="green")
        self.canvas.pack(padx=10)
        self.menu_frame = Frame(self, bg= "purple")
        self.menu_frame.pack(expand=TRUE, fill=BOTH)
        
        self.player_username= username
        self.player_pos = [] 
        self.movement_allowed = True
       

        
        self.up_direction=False
        self.down_direction=False
        self.left_direction=False
        self.right_direction=False
        

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
        
        if not new_user:
            with open("player_data.json", "r") as file: data =  json.load(file)
            for monster_name in self.game_data["monster data"].keys():
           
                
                self.terrain_cord_dict[monster_name] = data[username]["save data"][monster_name]
            
    
  
        # binds arrow keys for movement        
        self.bind("<KeyPress>", lambda x : self.key_press(x))
        self.bind("<KeyRelease>", lambda x : self.key_release(x))

        self.auto_save(True)
        self.load_main_menu()
        self.game_loop()
        self.new_frame()
    
    
    def auto_save(self, loop:bool = True): 
        """
        Autosaves player data like health, items, score, etc every 5 seconds.

        Args:
            loop (bool, optional): Decides if autosave is on or not. Defaults to True.
        """
        
        with open("player_data.json", "r") as file: 
            data =  json.load(file)
        
        monster_dict = {}
        for monster_name in self.game_data["monster data"].keys():
            monster_dict[monster_name] =  self.terrain_cord_dict[monster_name]
     

        data[self.player_username]["save data"] = monster_dict
        data[self.player_username]["data"] = self.player_data
        

        with open("player_data.json", 'w') as outfile: 
            json.dump(data, outfile, indent= 5)

        
        if loop == True:
            print("auto-saved")
            self.after(5000, lambda: self.auto_save())
       
        
    def load_main_menu (self):         
        """
        Loads the main menu UI for the map exploration part of the game. Displays things like player info 
        (health, score, etc) and displays items player currently has in a listbox.
        Args: None 
        Returns: None
        """
        menu_canvas = Canvas(self.menu_frame)
        menu_canvas.place(relx=0, rely=0, relheight=1, relwidth=1)
        menu_canvas.create_image(0,0,anchor = "nw", image = self.sprite_dict["UI"]["main menu background.png"])
        
        self.main_menu_frame = Frame(menu_canvas, bg=ACCENT_COLOUR)
        self.main_menu_frame.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.8)
        
        
        character_info_frame = Frame(self.main_menu_frame, borderwidth=2, background= "purple")
        character_info_frame.place(relx=0.02, rely=0.2, relwidth=0.46, relheight=0.8)
        Label(self.main_menu_frame, text="Character Info", font =("Arial",18,"bold"), bg= ACCENT_COLOUR, fg="light blue").place(relx=0, rely=0, relwidth=0.5, relheight=0.2)
        text = f"Health: {self.player_data['health']}\nLevel: {self.player_data['level']}\nScore: {self.player_data['score']}\nHigh Score: {self.player_data['high score']}\nDeaths: {self.player_data['deaths']}"
        Label(character_info_frame, text=text, font =("Arial",12),wraplength=150, anchor= N, bg=ACCENT_COLOUR, fg="White").place(relx=0, rely=0, relwidth=1, relheight=1)
        
        item_frame = Frame(self.main_menu_frame, borderwidth=2, background= "purple")
        item_frame.place(relx=0.52, rely=0.2, relwidth=0.46, relheight=0.8)
        Label(self.main_menu_frame, text="Items", font =("Arial",18,"bold"),wraplength=150, bg= ACCENT_COLOUR, fg="light blue").place(relx=0.5, rely=0, relwidth=0.5, relheight=0.2)
        sb = Scrollbar(item_frame)
        sb.place(relx=0.92, rely=0, relwidth=0.08, relheight=1)
        listbox = Listbox(item_frame,justify= CENTER,font =("Arial",12), bg= ACCENT_COLOUR, borderwidth=0, highlightthickness=0, fg="white")
        listbox.place(relx=0, rely=0, relwidth=0.92, relheight=1)
        
        for key, value in self.player_data["items"].items(): 
            if value  != 0:
                listbox.insert("end", f"{key}: {value}" )
        sb.config(command=listbox.yview)
        listbox.config(state="disabled", disabledforeground="White", yscrollcommand=sb.set )
    
   
    
    def key_press (self, event):

        key = event.keysym
        if key == "Up": 
            self.up_direction = True
        if key == "Down": 
            self.down_direction = True
        if key == "Left": 
            self.left_direction = True
        if key == "Right": 
            self.right_direction = True
        

    def key_release (self, event):
        key = event.keysym
        if key == "Up": 
            self.up_direction = False
        if key == "Down": 
            self.down_direction = False
        if key == "Left": 
            self.left_direction = False
        if key == "Right": 
            self.right_direction = False
 
 

    def monster_movement (self): 
        for key, list in self.monster_movement_dict.items():  
            try:
                for monster in self.game_data["monster data"].keys():
                    for monster_cord in self.terrain_cord_dict[monster]:
                        if (monster_cord[0],monster_cord[1])  in list:
                            
                            new_monster_cord = {"D": [monster_cord[0],monster_cord[1]+2],
                                        "U": [monster_cord[0],monster_cord[1]-2],
                                        "L": [monster_cord[0]-2,monster_cord[1]],
                                        "R": [monster_cord[0]+2,monster_cord[1]]}.get(key)
                            
                            self.terrain_cord_dict[monster].remove(monster_cord)
                            self.terrain_cord_dict[monster].insert(0,new_monster_cord)
            except KeyError: 
                continue

        
    def game_loop(self):
        self.monster_movement()

        result = self.player_movement()
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
            
            self.new_frame()
            self.after(int(1000/FPS), lambda : self.game_loop())
                    

    def player_movement( self):
        keys = [self.up_direction,self.down_direction, self.left_direction, self.right_direction]
        pixel_dist = 5
        '''
        direction = (0,0) if event == "none" else{
            "Up": (0, -pixel_dist),
            "Down": (0, pixel_dist),
            "Left": (-pixel_dist, 0),
            "Right": (pixel_dist, 0)
        }.get(event.keysym) 
        '''
        
        # keys = [up, down, left, right]
        if keys == [True, False, False, False]:
            direction = (0, -pixel_dist)
        elif keys == [False, True, False, False]:
            direction = (0, pixel_dist)
        elif keys == [False, False, True, False]:
            direction = (-pixel_dist, 0)
        elif keys == [False, False, False, True]:
            direction = (pixel_dist, 0)
        elif keys == [True, False, True, False]:
            direction = (-pixel_dist, -pixel_dist)
        elif keys == [True, False, False, True]:
            direction = (pixel_dist, -pixel_dist)
        elif keys == [False, True, True, False]:
            direction = (-pixel_dist, pixel_dist)
        elif keys == [False, True, False, True]:
            direction = (pixel_dist, pixel_dist)
        else: 
            
            direction = None
            
            
        if direction == None: 
            return None
        else:
            new_x = self.player_data["position"][0] + direction[0]
            new_y = self.player_data["position"][1] + direction[1]
            collision = self.collision_check(new_x,new_y)
            return collision
       
            
        
    def collision_check (self, new_x:int, new_y:int)->tuple:
        
        for key, list in self.terrain_cord_dict.items():
            if key not in self.game_data["terrain states"]["non solids"]:
                for value in list: 
                    obj_x = value[0]
                    obj_y = value[1]
                    if new_x in range(obj_x-30, obj_x +35) and new_y in range(obj_y-30, obj_y +35) :
                        #and (abs(obj_y -new_y)!=GRID_SIZE ) and abs(obj_x -new_x)!=GRID_SIZE
                        if key in self.game_data["monster data"].keys() : 
                            print("monster")
                            return key, (obj_x, obj_y)
                        else: 
                            return key, None
                  
        return True, (new_x, new_y)



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
              
                if x_min <= value[0] < x_max and y_min <= value[1] < y_max  and key != "grdsfaass": # remember to change this !!!!   
                    self.canvas.create_image(
                        value[0] - top_left_x,
                        value[1] - top_left_y,
                        anchor='nw',
                        image=self.sprite_dict["Textures"][f"{key}.png"]
                    )
        
        self.canvas.create_image(10 * GRID_SIZE, 7 * GRID_SIZE, 
                                 anchor=NW, image=self.sprite_dict["Textures"]['character.png'])

                            
class Map():

    def __init__(self, parent:Tk, terrain_cord_dict:dict, player_data:dict, monster_movement_dict:dict):
        """_summary_

        Args:
            parent (Tk): _description_
            terrain_cord_dict (dict): _description_
            player_data (dict): _description_
            monster_movement_dict (dict): _description_
        """
        super().__init__()
        
        self.game_instance = parent
        
        self.player_data = player_data
        self.terrain_cord_dict = terrain_cord_dict
        self.monster_movement_dict = monster_movement_dict
        
        with open("monster_path_data.json", "r") as file: 
            self.monster_path_file = json.load(file)
            
        with open("game_data.json", "r") as file: 
            self.game_data =  json.load(file)
        with open("map_data.json", "r") as file: 
            self.map_storage =  json.load(file)
        


    def delete_monster_cord(self, monster_cord:list, name:str):
        """_summary_

        Args:
            monster_cord (list): _description_
            name (str): _description_
        """
        for cord in self.terrain_cord_dict[name]: 
            if list(monster_cord) == list(cord): 
                print(self.terrain_cord_dict[name])
                remove = list(monster_cord)
                self.terrain_cord_dict[name].remove(remove)
                print("deleted")
                return
    def monster_path_load(self):

        direction = { 
            "D" : [(0,1), (0, 40)],
            "U" : [(0,1), (-39, 1)],
            "L" : [(-39, 1), (0, 1)],
            "R" : [(0, 40), (0, 1)]
        }

        y_cord = 0
        for x_line in self.map_storage[str(self.player_data["level"])]["monster paths"]:
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
       
        terrain_codes =  self.game_data["terrain codes"]
        monster_codes =  self.game_data["monster codes"]
        y_cord = 0
        
        
        for x_line in self.map_storage[str(self.player_data["level"])]["terrain"] :
            x_cord = 0
            for obj in x_line:
                #if (x_cord*40,y_cord*40) != tuple(self.player_data["position"]):
                pos = [x_cord*GRID_SIZE,y_cord*GRID_SIZE]
                #self.terrain_cord_dict["grass"].append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                
                sprite_name = terrain_codes.get(obj)
                if sprite_name == "teleport":
                    self.terrain_cord_dict[sprite_name].append(pos)
                    self.terrain_cord_dict["grass"].append(pos)
                elif sprite_name == "spawn": 
                    self.player_data["position"] = [x_cord*GRID_SIZE,y_cord*GRID_SIZE]
                    self.terrain_cord_dict["grass"].append(pos)
                elif sprite_name == None:
                    self.terrain_cord_dict["grass"].append(pos)
                else:
                    self.terrain_cord_dict[sprite_name].append(pos)
                    
                x_cord+=1 
            y_cord+=1        
        y_cord = 0 
        
        
        
        for x_line in self.map_storage[str(self.player_data["level"])]["monster spawns"]:
            x_cord = 0 
            for obj in x_line: 
                pos = [x_cord*GRID_SIZE,y_cord*GRID_SIZE]
                monster_name = monster_codes.get(obj)
                
                if monster_name != None: 
                    self.terrain_cord_dict[monster_name].append(pos)
                x_cord+=1 
                
            y_cord+=1     
                
                
        
        print('terrain loaded in')
        

Game()
            
        