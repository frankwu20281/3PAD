"""
Main file which needs to be run to start program. 
Code created by Frank Wu.
"""

# Import modules that the game needs to be able to work.
from  tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from battle import *        
import  json, os
PROGRAM_PATH = os.getcwd() # Store the program's path to access essential folders.
SPRITE_FOLDER_PATH=PROGRAM_PATH+"/Sprites" # Store path to sprites folder.
TEXTURE_FOLDER_PATH=PROGRAM_PATH+"/Sprites/Textures" # Store path to texture folder.
BATTLE_FOLDER_PATH=PROGRAM_PATH+"/Sprites/Battle" # Store path to monster battling textures folder.
UI_FOLDER_PATH=PROGRAM_PATH+"/Sprites/UI" # Store path to UI textures folder
DATA_FOLDER_PATH=PROGRAM_PATH+"/Data" # Store path to data folder. 
# Adjustable variables for the core functionality of the game.
FPS = 40    # Frames per second. 
WINDOW_SIZE_HEIGHT = 600    # Number of pixels for the height of the main screen.
WINDOW_SIZE_WIDTH = 840     # Number of pixels for the width of the main screen.
GRID_SIZE = 40  # The number of pixles for each texture tile.
# Styling variables used in the game. 
BG_COLOUR = "#2b7d9b"
ACCENT_COLOUR = "#191919"
LOGIN_UI_COLOUR = "#323645"
TEXT_COLOUR = "#cabfcf"
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
        # Attempt to find the path of the image with the args passed through the function. 
        path = path+f"/{name}"
        image = PhotoImage(file=path)
    except : 
        # If image is not found, then throw up error and load no image. 
        pass
    # If image is found then return the PotoImage
    return image


class Main(Tk):
    """
    The main class for the game, login screen, most of the backend components and map exporation code 
    is found in this class.

    Args:
        Tk : Lets the class use functions from the Tkinter and Tkinter.ttk modules 
    """
    
    def __init__(self):
        """
        Runs when game is started up. Loads all necessary Json files and creates login page for user to login to game.
        Args: None 
        Returns: None
        
        """
        super().__init__()
        # Setup Tkinter page (window size, colour, etc). 
        self.geometry(f"1000x800") # Set size of window. 
        self.configure(background= "Black") # Set window background colour.
        self.resizable(False, False) # Dont let user resize window. 
        self.title("Number Beasts") # Name the tile of the window as "Number Beasts" which is the name of the game.
        # Opening JSON file and making the data in that json into a variable which can be accessed by the program. 
        with open("game_data.json") as file: 
            self.game_data =  json.load(file) # Load all game data (terrain states, item descriptions and what they do, etc) into variable named self.game_data. 
        # Setup player data. 
        self.player_data = {"position": [],
                            "health": 600,
                            "level": 1, 
                            "score": 0,
                            "high score": 0,
                            "deaths": 0,
                            "items": {"mini heal": 10, "wooden sword": 5}}
        self.sprite_dict = {"Textures":{}, "UI":{}, "Battle": {}} # Setup sprite dictionary where all the image assets used in the game will be stored. 
        folder_names =os.listdir(SPRITE_FOLDER_PATH) # Get the names of the folders storing the sprite images.
        # Load all the images stored in the folders as PhotoImages into the sprite dictionary, ready for the program to use.
        for folder in folder_names: # Loop through all the folder names.
            path = {"Textures": TEXTURE_FOLDER_PATH, 
                    "UI": UI_FOLDER_PATH, 
                    "Battle": BATTLE_FOLDER_PATH}.get(folder) # Get the path to that folder. 
            for file in os.listdir(path): # Loop through every image name stored under the file and make them into a PhotoImage variable and store them in dictionary. 
                self.sprite_dict[folder][file] = create_sprites(path = path , name = file)
        Label(self,image=self.sprite_dict["UI"]["login background.png"]).place(relx=0, rely=0, relwidth=1, relheight=1) # Label to put the login background image in. 
        login_frame = Frame(self, bg= ACCENT_COLOUR) # Frame to put all of the login UI elements in. 
        login_frame.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.7) # Place login frame onto screen. 
        # Labels to tell user what the entry boxes do. 
        Label(login_frame, text= "Login page", font= ("Arial", 28, "bold"), anchor=CENTER, bg= ACCENT_COLOUR, fg=TEXT_COLOUR).place(relx=0.2, rely=0.1, relheight=0.1, relwidth=0.6) 
        Label(login_frame, text= "Username:", font= ("Arial", 18, "bold"), anchor=CENTER, bg= ACCENT_COLOUR, fg=TEXT_COLOUR ).place(relx=0.1, rely=0.3, relheight=0.1, relwidth=0.3) 
        username_var = StringVar() # Setup username variable. 
        username_entry = Entry(login_frame, textvariable=username_var, font= ("Arial", 18), bg= LOGIN_UI_COLOUR, fg=TEXT_COLOUR )   # Entrybox for username entry.
        username_entry.place(relx=0.55, rely=0.3, relheight=0.1, relwidth=0.4) # Place username entrybox onto screen. 
        Label(login_frame, text= "Password:", font= ("Arial", 18, "bold"), anchor=CENTER, bg= ACCENT_COLOUR, fg=TEXT_COLOUR ).place(relx=0.1, rely=0.5, relheight=0.1, relwidth=0.3) # Label to tell user what the password entrybox does.
        password_var = StringVar()  # Setup password variable. 
        password_entry = Entry(login_frame, textvariable= password_var,show="*", font= ("Arial", 18), bg= LOGIN_UI_COLOUR, fg=TEXT_COLOUR ) # Entrybox for password entry. 
        password_entry.place(relx=0.55, rely=0.5, relheight=0.1, relwidth=0.4) # password entrybox onto screen. 
        # Buttons for logging in and making a new account. 
        Button(login_frame, text ="New Account", command= lambda: self.login(username=username_var.get(), password= password_var.get(),new_user=True), bg= LOGIN_UI_COLOUR, fg=TEXT_COLOUR, font= ("Arial",14, "bold") ).place(relx=0.1, rely=0.8, relheight=0.1, relwidth=0.3) 
        Button(login_frame, text ="Login", command= lambda: self.login(username=username_var.get(), password= password_var.get(),new_user=False), bg= LOGIN_UI_COLOUR, fg=TEXT_COLOUR , font= ("Arial",14, "bold")).place(relx=0.6, rely=0.8, relheight=0.1, relwidth=0.3) 
        self.login_text = StringVar()  # If any errors occur when user is logging in, this variable connected to a label will tell the user what the issue is. 
        Label(login_frame, textvariable= self.login_text, font= ("Arial", 14), wraplength= 450, bg= ACCENT_COLOUR, fg=TEXT_COLOUR ).place(relx=0.1, rely=0.65, relheight=0.1, relwidth=0.8) # Place error displaying label onto screen. 
        self.mainloop() # Initiate Tkinter loop, which creates the Tkinter window. 
        
    def login(self,username: str, password: str, new_user: bool): 
        """ 
        Deals with user login and new account creation.

        Args:
            username (str): Username which the user inputed.
            password (str): Password which the user inputed.
            new_user (bool): Tells function if user is logging in or making new account.
        Returns: None
        """
        # Strip username and password text of any spaces at the end of the strings. 
        username = username.rstrip()
        password = password.rstrip()
        # Opens json file where all player data is stored and puts the data into a variable.
        with open("player_data.json", "r") as infile: 
            user_data_file = json.load(infile) 
        # Checks if username and password are empty or not.
        if password != "" and username != "":
            symbols = "'!@#$%^&*()-+?=,<>/ '"  # Symbols that are not allowed in the password of username. 
            # Error if username has any symbols that are not allowed.
            if any(c in symbols for c in username) or not username.isalnum():
                self.login_text.set("Username cannot include spaces, symbols or ASCII")
                return
            # If there are any spaces or symbols that are not wanted in password then error is shown to user.
            if " " in password or "'" in password or '"' in password:
                self.login_text.set("Password cannot include spaces,speech marks or ASCII")
                return
            # If user is logging in and not making a new account. 
            if  new_user == False:
                # Get strings of all usernames which are stored in the json and checks if the username entered is there.
                if username in user_data_file.keys():
                    # If password matches the password saved for that certain username. 
                    if user_data_file[username]["password"] == password:
                        # Make data stored in the json file the player_data which the game uses.
                        self.player_data = user_data_file[username]["data"]
                        # Checks if the user just died during the last time they played or if their character still has enough health to keep playing.
                        messagebox.showinfo(title = "Login", message= "Login successful!")
                        if user_data_file[username]["data"]["health"] > 0:
                            # Load game with the current data stored in the json from the last time they played.
                            self.load_game(new_user= False, username = username) 
                        else:
                            # Since user's character died last time they played, reset all the player data and make them start as a new character in the frist level. 
                            self.player_data = {"position": self.player_data["position"],
                            "health": 600,
                            "level": 1, 
                            "score": 0,
                            "high score": self.player_data["high score"] if self.player_data["score"]< self.player_data["high score"] else self.player_data["score"], # Update players high score value. 
                            "deaths": self.player_data["deaths"]+1, # Update player death score. 
                            "items": {"mini heal": 10, "wooden sword": 5}}
                            self.load_game(new_user= True, username = username) 
                        
                    else: 
                        # Tell user that the password entered doesn't match the password stored for this account. 
                        self.login_text.set("Wrong password to account!")
                else:
                    # Tell user what to do if they try to login with an account that hasn't been saved in the json. 
                    self.login_text.set("This username has not been saved, click 'New Account' button to login as new player!")
            # If player is making a new account. 
            elif new_user == True:
                # Check if the username user has entered has already been taken.
                if username not in user_data_file.keys():
                    if password != "" and username != "":
                        symbols = "'!@#$%^&*()-+?=,<>/ '"  # Symbols that are not allowed in the password of username. 
                        # Error if username has any symbols that are not allowed.
                        if any(c in symbols for c in username) and username.isalnum():
                            self.login_text.set("Username cannot include spaces,symbols or ASCII")
                            return
                        # If there are any spaces or symbols that are not wanted in password then error is shown to user.
                        if " " in password or "'" in password or '"' in password:
                            self.login_text.set("Password cannot include spaces or speech marks")
                            return
                        messagebox.showinfo(title = "New account", message= "New account has been created!")
                        # If it has not been taken load new player data under this username.
                        user_data_file[username] = {
                        "password" : str(password), 
                        "data": self.player_data, 
                        "save data": {}
                        }
                        # Save the data to the json.
                        with open("player_data.json", 'w') as outfile: json.dump(user_data_file, outfile, indent= 5)
                        self.load_game(new_user= True, username = username) 
                        
                else: 
                    # Show error if username has already been used.
                    self.login_text.set("Account has already been saved, please login")
        else: 
            # Show error if user hasn't entered anything for username and/or password. 
            self.login_text.set("Please enter both username and password (No spaces)")
            
    def load_game(self, new_user: bool , username: str):
        """
        Loads the map exporation part of the game after user has finished logging in.

        Args:
            new_user (bool): New account or previous account logging in.
            username (str): Username of player.
        Returns: None
        """
        # Clear screen. 
        for widgets in self.winfo_children():
            widgets.destroy()
        # Setup canvas where the game will be displayed on. 
        self.canvas = Canvas(self, width=WINDOW_SIZE_WIDTH, height=WINDOW_SIZE_HEIGHT, bg="green")  # Set the canvas size with the variables which were set in the beginning of the program. 
        self.canvas.pack(padx=10)   # Place the canvas onto the window. 
        self.menu_frame = Frame(self, bg= "purple") # Setup the menu frame where all the menus will be places in. 
        self.menu_frame.pack(expand=TRUE, fill=BOTH)# Place the menu fram onto the window. 
        self.player_username= username  # Let username be accessed in whatever function. 
        self.player_pos = []            # Characters current position coordinates on the map. 
        self.movement_allowed = True    # Allow movement of character around the map using arrow keys. 
        # Setup movement key variables. 
        self.up_direction=False 
        self.down_direction=False
        self.left_direction=False
        self.right_direction=False
        # Setup dictionaries to store game data. 
        self.terrain_cord_dict = {} 
        self.monster_movement_dict = {"U" :[], 
                                      "D" :[], 
                                      "L": [],
                                      "R": []} # Dictionary where all the cords of the monster movement tiles are stored so that the program know where to move a monster if they are on the cords of one of these tiles. 
        # Load map data.
        self.map_handler = Map(parent=self, terrain_cord_dict= self.terrain_cord_dict, player_data= self.player_data, monster_movement_dict = self.monster_movement_dict)
        self.map_handler.reset_cord_storage()   # Wipe terrain coord storage dict clean.
        self.map_handler.terrain_load()         # Load new terrain coords into storage dict. 
        self.map_handler.monster_path_load()    # Load the monster paths for the moving monsters.
        
        # If user has just made a new account load all the monster coords to the json file so that when the log back in the they can start from where
        # they got off from. 
        if not new_user:
            with open("player_data.json", "r") as file: data =  json.load(file)
            for monster_name in self.game_data["monster data"].keys():self.terrain_cord_dict[monster_name] = data[username]["save data"][monster_name]
            self.player_data["position"] = data[username]["data"]["position"]   # Puts player at the last position that was saved. 
        # Bind all the keys on the keyboard to activate respective functions when pressed and released.    
        self.bind("<KeyPress>", lambda x : self.key_press(x))
        self.bind("<KeyRelease>", lambda x : self.key_release(x))
        self.auto_save(True)    # Turn on auto-save. 
        self.load_main_menu()   # Load main menu of the game.
        self.game_loop()        # Start game loop so things will start running.
        self.new_frame()        # Display frist frame of the game. 
        
    def auto_save(self, loop:bool = True): 
        """
        Autosaves player data like health, items, score, etc every 5 seconds.
        Args:
            loop (bool, optional): Decides if autosave is on or not. Defaults to True.
        """
        # Opens json file and put data in json into "data" variable.
        with open("player_data.json", "r") as file: 
            data =  json.load(file)
        # Get the current coords of monsters in game.
        monster_dict = {}
        for monster_name in self.game_data["monster data"].keys():
            monster_dict[monster_name] =  self.terrain_cord_dict[monster_name]
        # Load auto-save data into the data variable.
        data[self.player_username]["save data"] = monster_dict
        data[self.player_username]["data"] = self.player_data
        # Save the updated data back into the json. 
        with open("player_data.json", 'w') as outfile: 
            json.dump(data, outfile, indent= 5)
        # If auto-save is turned on then run the auto-save function again in 5 seconds. 
        if loop == True:
            self.after(5000, lambda: self.auto_save())
       
    def load_main_menu (self):         
        """
        Loads the main menu UI for the map exploration part of the game. Displays things like player info 
        (health, score, etc) and displays items player currently has in a listbox.
        Args: None 
        Returns: None
        """
        # Label which is used to display the background image of the main menu. 
        Label(self.menu_frame, image = self.sprite_dict["UI"]["main menu background.png"] ).place(relx=0, rely=0, relheight=1, relwidth=1) 
        self.main_menu_frame = Frame(self.menu_frame, bg=ACCENT_COLOUR) # Frame to place all the menu UI elements. 
        self.main_menu_frame.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.8) # Place all the frame on to the screen. 
        character_info_frame = Frame(self.main_menu_frame, borderwidth=2, background= "purple") # Frame to place the player infomation like health and score etc.
        character_info_frame.place(relx=0.02, rely=0.2, relwidth=0.46, relheight=0.8)   # Place this frame onto the window. 
        Label(self.main_menu_frame, text="Character Info", font =("Arial",18,"bold"), bg= ACCENT_COLOUR, fg="light blue").place(relx=0, rely=0, relwidth=0.5, relheight=0.2)    # Label used to create a title to tell user the info below is player info. 
        text = f"Health: {self.player_data['health']}\nLevel: {self.player_data['level']}\nScore: {self.player_data['score']}\nHigh Score: {self.player_data['high score']}\nDeaths: {self.player_data['deaths']}"  # Text of player info. 
        Label(character_info_frame, text=text, font =("Arial",12),wraplength=150, anchor= N, bg=ACCENT_COLOUR, fg="White").place(relx=0, rely=0, relwidth=1, relheight=1)   # Display player info text using a label onto them menu. 
        item_frame = Frame(self.main_menu_frame, borderwidth=2, background= "purple")   # Frame to display all the items the player currently has. 
        item_frame.place(relx=0.52, rely=0.2, relwidth=0.46, relheight=0.8)             # Place this frame onto the window. 
        Label(self.main_menu_frame, text="Items", font =("Arial",18,"bold"),wraplength=150, bg= ACCENT_COLOUR, fg="light blue").place(relx=0.5, rely=0, relwidth=0.5, relheight=0.2)    # Use label to create a "Items" title. 
        sb = Scrollbar(item_frame)  # Create scrollbar which lets user scroll through the items stored in the listbox. 
        sb.place(relx=0.92, rely=0, relwidth=0.08, relheight=1) # Place scrollbar onto menu. 
        listbox = Listbox(item_frame,justify= CENTER,font =("Arial",12), bg= ACCENT_COLOUR, borderwidth=0, highlightthickness=0, fg="white")    # Create listbox to display all the items. 
        listbox.place(relx=0, rely=0, relwidth=0.92, relheight=1)   # Place listbox onto menu. 
        for key, value in self.player_data["items"].items():    # Loop through all the items the player currently has to display them in listbox.
            if value  != 0: listbox.insert("end", f"{key}: {value}" )   # If there is a an item then place it into the listbox. 
        sb.config(command=listbox.yview)    # Bind the scrollbar functionality to allow user to scroll listbox. 
        listbox.config(state="disabled", disabledforeground="White", yscrollcommand=sb.set )    # Don't let user to be able to click on items. 
        
    def key_press (self, event):
        """
        This function detects if any of the movement keys is being pressed.
        Args:
            event : Data about what key is being pressed.
        Returns: None
        """
        key = event.keysym # From key data get the name of the key being pressed.
        
        # If direction key is being pressed then tell program that it is currently active.
        if key == "Up": 
            self.up_direction = True
        if key == "Down": 
            self.down_direction = True
        if key == "Left": 
            self.left_direction = True
        if key == "Right": 
            self.right_direction = True
        

    def key_release (self, event):
        """This function detects if any of the direction keys are being released.

        Args:
            event : Data about what key is being released.
            
        Returns: None
        """
        key = event.keysym  # From the key data get the name of the key being released. 
        
        
        # If direction key is being released tell program that that key is currently not active.
        if key == "Up": 
            self.up_direction = False
        if key == "Down": 
            self.down_direction = False
        if key == "Left": 
            self.left_direction = False
        if key == "Right": 
            self.right_direction = False
 
    def monster_movement (self): 
        """
        This function automatically moves the monsters around the map. 
        Args: None
        Returns: None
        """
        # Loop to check if there are any monsters on movement tiles, and if so then move that monster's cords depending on what direction the tile says to go to.
        for key, list in self.monster_movement_dict.items():  
            try:    # Try block to catch any key errors that might occur so that the program won't crash when there is a key error. 
                for monster in self.game_data["monster data"].keys():   # Loops through all the lists of each monsters cords. 
                    for monster_cord in self.terrain_cord_dict[monster]:    # Loops through all the cords of the monsters on map.
                        if (monster_cord[0],monster_cord[1])  in list:  # If monster cord matches a movement tile cord then prepare to move the monster.
                            # Direction the monster should move depending on movement tile.
                            new_monster_cord = {"D": [monster_cord[0],monster_cord[1]+2],
                                        "U": [monster_cord[0],monster_cord[1]-2],
                                        "L": [monster_cord[0]-2,monster_cord[1]],
                                        "R": [monster_cord[0]+2,monster_cord[1]]}.get(key)
                            # Update coords of the monster depending on the movement tile they are on currently 
                            self.terrain_cord_dict[monster].remove(monster_cord)
                            self.terrain_cord_dict[monster].insert(0,new_monster_cord)
            except KeyError: 
                continue
        
    def game_loop(self):
        """
        This function is the main game loop for the game, meaning all automatic functions like frame generation, auto monster movement and collision detection
        are run in this function as they are things that need to be constantly run. The loop repeats itself depending on the FPS value stated in the beginning 
        of the code, currently it is at 40FPS so this function should run every 25 miliseconds.
        Args: None
        Returns: None
        """
        self.monster_movement() # Run the monster_movement function to update moving monster cords. 
        result = self.player_movement() # Update player cords depending on movement buttons currently pressed.
        if result[0] in self.game_data["monster data"].keys():   # If new updated player cords hits a monster then run the monster battling part of the game.
            self.movement_allowed = False   # Don't let player move around the map anymore. 
            # Start displaying cutscreen to indicate to player that they are entering the monster battling part of the game since they collided with a monster. 
            self.canvas.create_image(10 * GRID_SIZE, 6 * GRID_SIZE, 
                                 anchor=NW, image=self.sprite_dict["Textures"]['exclamation mark.png'])
            # Start the monster battling by running the Battle class.
            Battle(parent = self,monster_cord= result[1], sprite_dict=self.sprite_dict, monster_name= result[0], data = self.player_data, username= self.player_username)
            return 
        elif result[0] == "teleport": # Puts player in next level when player enters portal. 
            self.map_handler.next_level() # Update sprite cords for the next level
            self.game_loop()    # Start game loop again to display new level. 
            self.new_frame()    # Display first frame of the next level. 
            return
        elif result[0] == True: # Move player to new cords if no collisions or interactions (monster battling or portal) occur. 
            self.player_data["position"] = result[1]
        if self.movement_allowed:   # Checks if new frame should keep being generated or not.
            # If yes, then display new frame and run the game_loop again after the designated timeframe set by FPS variable. 
            self.new_frame()
            self.after(int(1000/FPS), lambda : self.game_loop())
    def player_movement(self):
        """
        This function calculates where the player has moved depending on the movement keys currently active. 
        Args: None. 
        Returns:
            If there is a player collision or not. 
        """
        keys = [self.up_direction,self.down_direction, self.left_direction, self.right_direction] # Get all the variables that are linked to the movement keys.
        pixel_dist = 5 # How many pixels the player should move. 
        # If statments to calculate what direction the player should move depending on what direction keys are active. 
        if keys == [True, False, False, False]:     # Move up. 
            direction = (0, -pixel_dist)
        elif keys == [False, True, False, False]:   # Move down. 
            direction = (0, pixel_dist)
        elif keys == [False, False, True, False]:   # Move left.
            direction = (-pixel_dist, 0)
        elif keys == [False, False, False, True]:   # Move right.
            direction = (pixel_dist, 0)
        elif keys == [True, False, True, False]:    # Move diagonally up-left. 
            direction = (-pixel_dist, -pixel_dist)  
        elif keys == [True, False, False, True]:    # Move diagonally up-right.
            direction = (pixel_dist, -pixel_dist)
        elif keys == [False, True, True, False]:    # Move diagonally down-left.
            direction = (-pixel_dist, pixel_dist)
        elif keys == [False, True, False, True]:    # Move diagonally down-right. 
            direction = (pixel_dist, pixel_dist)
        else: 
            direction = (0,0)                       # If no movement keys are active then dont move player coords  
        # Calculate the new player coords depending on what direction player has moved which was calculated in the previous if statment block.    
        new_x = self.player_data["position"][0] + direction[0]
        new_y = self.player_data["position"][1] + direction[1]
        collision = self.collision_check(new_x,new_y)   # Check if the player collides with anything when moving to the new coords. 
        return collision    # Return the collision value. 
         
    def collision_check (self, new_x:int, new_y:int)->tuple:
        """
        This function checks if the new player cords collide with any solid terrain object or monsters currently on the map, and if so returns values that flag this collision. 
        If no collision occurs then flag that no collisions have occured. 
        Args:
            new_x (int): x-coord value of the new coord of the player. 
            new_y (int): y-coord value of the new coord of the player. 

        Returns:
            tuple: Info on if there was a collision or not, if there was a collision what type collision occured (monter interaction or hit solid terrain object). 
        """
        for key, list in self.terrain_cord_dict.items():
            if key not in self.game_data["terrain states"]["non solids"]: # Get all terrain objects that are solid.                
                for value in list: # Extract the cords of each solid terrain object in the list which is in the terrain dictionary. 
                    obj_x = value[0]
                    obj_y = value[1]
                    if new_x in range(obj_x-30, obj_x +35) and new_y in range(obj_y-30, obj_y +35): # Sees if new player coords has hit any solid terrain objects or monsters.   
                        if key in self.game_data["monster data"].keys() :   # If players new cords collide with a monster. 
                            return key, (obj_x, obj_y) # Returns collision info (name of monster, cord of monster). 
                        else: 
                            return key, None # Returns collision info (hit a solid terrain object, no need for cords).                   
        return True, (new_x, new_y) # Returns collision info (True for nothing collided, new player cords). 

    def new_frame(self):
        """
        This function displays all the sprites that can currently be seen on the canvas using the terrain cords of all objects on the players current level. 
        Args: None 
        Returns: None
        """       
        self.canvas.delete("all")   # Delete all previous sprites displayed on canvas to prepare to display new sprites.       
        top_left_x = self.player_data["position"][0] - 10*GRID_SIZE # Calculate the cords of the top left corner of the canvas to see what the display cords are so as to calculate what to sprites to display. 
        top_left_y = self.player_data["position"][1] - 7*GRID_SIZE  # Calculate the cords of the top right corner of the canvas to see what the display cords are so as to calculate what to sprites to display.      
        x_min = top_left_x - GRID_SIZE              # Calculate the minimium x-cord of sprites that are displayed. 
        x_max = top_left_x + WINDOW_SIZE_WIDTH + 1  # Calculate the maximum x-cord of sprites that are displayed. 
        y_min = top_left_y - GRID_SIZE              # Calculate the minimium y-cord of sprites that are displayed. 
        y_max = top_left_y + WINDOW_SIZE_HEIGHT + 1 # Calculate the maximum y-cord of sprites that are displayed. 
        sprite_coords = [] # List of all the coords of sprites that are stored for this current level. 
        for key, value_list in self.terrain_cord_dict.items(): # This for loop is to re-adjust the display order so all non-solid terrain sprites (grass, dirt paths etc) are displayed first. 
            if key in self.game_data["terrain states"]["non solids"]: # If current coord list is non-solid put it in the front of the sprite_coords list 
                sprite_coords.insert(0,(key, value_list))
            else:
                sprite_coords.append((key, value_list))   # If not non-solid then put it in the back of the sprite_coords list.
        for key, value_list in sprite_coords:   # Loop through all sprite lists in sprite_coords.
            for value in value_list:  # Loop through all coord-values of the stored sprites in each value_list.             
                if x_min <= value[0] < x_max and y_min <= value[1] < y_max : # If the coord of the sprite is between the min and max x-coord and y-coord value then display that sprite on the canvas.
                    # Display the sprite on its designated coord value on the canvas. 
                    self.canvas.create_image( value[0] - top_left_x, value[1] - top_left_y, anchor='nw', image=self.sprite_dict["Textures"][f"{key}.png"])
        # After finishing displaying all the visible sprites on the canvas place the character sprite in the middle of the canvas as this sprite does not move around and is always in the middle of the canvas. 
        self.canvas.create_image(10 * GRID_SIZE, 7 * GRID_SIZE, anchor=NW, image=self.sprite_dict["Textures"]['character.png'])
               
class Map():
    def __init__(self, parent:Tk, terrain_cord_dict:dict, player_data:dict, monster_movement_dict:dict):
        """
        This function automatically runs when the Map class is called. It creates all the variables for the arguments that are passed into the class, allowing the rest of the functions
        in this class to access them. It also loads the nessasary json file data into variables ready for the functions in this class to use. 
        Args:
            parent (Tk): The Tkinter variable from the Game class which allows the whole program to function.
            terrain_cord_dict (dict): Dictionary with all the coord values of all terrain items stored in it. 
            player_data (dict): Data of the user currently playing the game. 
            monster_movement_dict (dict): The coords of all monsters on the level. 
        Returns: None
        """
        super().__init__()
        self.game_instance = parent # Make the self.game_instance variable be the Tkinter variable of the main class which runs the whole program. 
        self.player_data = player_data  # Place player_data into self.player_data variable.
        self.terrain_cord_dict = terrain_cord_dict  # Place terrain_cord_dict into self.terrain_cord_dict variable. 
        self.monster_movement_dict = monster_movement_dict  # Place monster_movement_dict into self.monster_movement_dict variable. 
        # Store all data in the game_data json into the self.game_data variable. 
        with open("game_data.json", "r") as file: 
            self.game_data =  json.load(file)
        # Store all data in the map_data json into the self.map_storage variable. 
        with open("map_data.json", "r") as file: 
            self.map_storage =  json.load(file)

    def delete_monster_cord(self, monster_cord:list, name:str):
        """
        This function remove the cords of any monster that has been defeated by the player from storage. 
        Args:
            monster_cord (list): The cords of the monster. 
            name (str): The name of the monster that was defeated. 
        Returns: None
        """
        # Delete the cord value of the monster that was defeated from its cord list which is stored in the terrain_cord_dict. 
        self.terrain_cord_dict[name].remove(list(monster_cord))
        
    def monster_path_load(self):
        """
        This funciton loads the monster paths for each level which are set out in the map data json file. 
        Args: None 
        Returns: None
        
        """
        # Dictonary which stores all the sizes of the monster movement tiles. 
        direction = { 
            "D" : [(0,1), (0, 40)],
            "U" : [(0,1), (-39, 1)],
            "L" : [(-39, 1), (0, 1)],
            "R" : [(0, 40), (0, 1)]
        }
        y_cord = 0  # Variable used to loop through the monster path map. 
        for x_line in self.map_storage[str(self.player_data["level"])]["monster paths"]:    # Loop through the monster path map to find the paths of the monsters.
            x_cord = 0 
            for obj in x_line: # Loop through each letter tile of each line of the monster path map. 
                if obj == "D" or obj == "U" or obj ==  "L"  or obj == "R":  # If the current tile is a monster movement tile.
                    # Get the size and postition of the monster movement tiles.
                    x_start, x_end = direction.get(obj)[0][0],direction.get(obj)[0][1]
                    y_start, y_end = direction.get(obj)[1][0],direction.get(obj)[1][1]
                    tuple_range = [(x_cord+x, y_cord+y) for x in range(x_start, x_end) for y in range(y_start, y_end)]  # Create a list of all the pixel cords of the movement tiles.
                    self.monster_movement_dict[obj].extend(tuple_range) # Store all the cords of the movement tiles in a dictionary variable. 
                x_cord += GRID_SIZE
            y_cord += GRID_SIZE

    def next_level (self): 
        self.player_data["level"]+= 1
        self.player_data["position"] = []
        self.reset_cord_storage()
        self.terrain_load()
        self.monster_path_load()

    
    def reset_cord_storage (self):
        """
        This function clears all the cord values stored in the terrain dictionary to prepare for a new level.
        Args: None
        Returns: None
        """
        file_list = os.listdir(TEXTURE_FOLDER_PATH) # Get all the file names. 
        for file_name in file_list:  # Loop through all the file names. 
            self.terrain_cord_dict[file_name.replace(".png", "")] = []  # Clear the list value stored under the file name key in the terrain cord dictionary. 
        for key in self.monster_movement_dict:  # Loop through all the monster names. 
            self.monster_movement_dict[key] = []   # Clear all of the monster movement values stored under the monster name keys in the dictionary. 

    def terrain_load(self):
        """
        This function loads all the terrain cords using the data stored in the map data json. 
        Args: None 
        Returns: None
        """
        terrain_codes =  self.game_data["terrain codes"]    # Get all the terrain letter codes.
        monster_codes =  self.game_data["monster codes"]    # Get all the monster letter codes. 
        monster_codes["x"] = "spawn"
        y_cord = 0
        for x_line in self.map_storage[str(self.player_data["level"])]["terrain"] : # Loop through all lines in the map level.
            x_cord = 0
            for obj in x_line: # Loop through each letter tile in each line of the map level. 
                pos = [x_cord*GRID_SIZE,y_cord*GRID_SIZE]   # Calculate the cords of the letter tile depending on where it is on the level.         
                sprite_name = terrain_codes.get(obj)    # Get the sprite assigned to the letter tile. 
                if sprite_name == "teleport":           # If sprite is teleport then place it in their respective key dictionary spot.
                    self.terrain_cord_dict[sprite_name].append(pos)
                    self.terrain_cord_dict["grass"].append(pos)
                elif sprite_name == None:               # If sprite name doesn't exist then put grass sprite in its place.
                    self.terrain_cord_dict["grass"].append(pos)
                else:       # If sprite is stored then place it in their respective key dictionary spot.
                    self.terrain_cord_dict[sprite_name].append(pos)
                x_cord+=1 
            y_cord+=1        
        y_cord = 0 
        for x_line in self.map_storage[str(self.player_data["level"])]["monster spawns"]:   # Loop through all the lines in the monster map. 
            x_cord = 0 
            for obj in x_line:  # Loop through each letter tile in each line of the map level. 
                pos = [x_cord*GRID_SIZE,y_cord*GRID_SIZE]   # Calculate cord poistion of the letter tile. 
                monster_name = monster_codes.get(obj)       # Get the monster name assigned to the letter tile. 
                if monster_name != None:    # If monster name is known then store postion into the dictionary. 
                    if monster_name == "spawn":            # If sprite is spawn then grass sprite in that place and set spawn position of player there.
                        self.player_data["position"] = [x_cord*GRID_SIZE,y_cord*GRID_SIZE]
                    else:
                        self.terrain_cord_dict[monster_name].append(pos)
                x_cord+=1 
            y_cord+=1     
    
Main()  # Starts the game by calling Main class when main file is run. 
            
        