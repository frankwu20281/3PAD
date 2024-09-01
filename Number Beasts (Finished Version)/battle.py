"""
The battle.py file runs the monster battling part of the game. 
Code created by Frank Wu.
"""
# Importing modules to make game work. 
from tkinter import *   # Import Tkinter 
import random           # Import random used in math question generation
import json             # Import json to be able to read json files 
import operator         # Used to impliment the math functions to calculate the answer from the questions generated
from functools import reduce    # Used to calculate the answers by apply the function to the question to calculate the answer. 
# Constants that are used in the monster battling. 
TEXT_COLOUR = "#cabfcf" # Hex code value used for the backgrounds.
ACCENT_COLOUR = "#191919"   # Hex code value for the text. 
def clear_frame(frame):
    """
    This function deletes all the childen inside the frame that you pass into the function. 
    Args:
        frame : Frame that will have its childen elements removed. 
    """
    for widgets in frame.winfo_children():  # Loop through all the childen in the frame. 
      widgets.destroy() # Delete the childen from the frame. 

class Battle():
    """
    This class is is used to create the monster battling. 
    """

    def __init__(self, **kwargs):   
        """
        This function creates all the variables which will be needed to create the monster battling. It also 
        creates the cutscreen to indicate that the player has started the monster battle. This function
        automatically runs when the battle class is called.
        Args: 
            **kwargs : All the variables and data needed to be passed through the battle class to create the monster battling
                       part of the game. 
        """
        with open("game_data.json") as file:    # Open the game_data json. 
            self.game_data = json.load(file)    # Load the json data into the self.game_data variable. 
            self.monster_data =  self.game_data["monster data"] # Put the monster data into a variable. 
        self.monster_name = kwargs ["monster_name"]             # Put monster name into variable. 
        self.player_data = kwargs["data"]                       # Put player data into variable.    
        self.game_instance = kwargs["parent"]                   # Put game tkinter varaible into variable. 
        self.monster_cord = kwargs["monster_cord"]              # Put monster cordinates into variable. 
        self.battle_sprite_dict = kwargs["sprite_dict"]["Battle"]   # Put battle sprites into dict variable. 
        self.sprite_dict = kwargs["sprite_dict"]                    # Put all sprites into dict variable. 
        self.username = kwargs["username"]  # Put username into variable. 
        self.frame = self.game_instance.menu_frame      # Set the menu frame of the game as a variable which can be accessed in the battle class. 
        self.canvas = self.game_instance.canvas         # Set the main canvas of the game as a variable which can be accessed in the battle class. 
        self.monster_health = random.randint(300, 450)  # Set monster health as a random number bewteen 400 and 700.
        self.shield_health = 0 
        self.reset_stat_vars()  # Run function which resets the stats variables to the default states. 
        clear_frame(self.frame) # Clear the main menu to prepare to create the battle menus. 
        self.cutscreen()        # Play cutscreen to tell user that battle is starting. 
        self.game_instance.after(1500, lambda: self.load_battle_canvas())   # After cutscreen finishes load the battle canvas. 
        self.game_instance.after(1500, lambda: self.load_battle_menu())     # After cutscreen finishes load in battling menus. 
        
    def reset_stat_vars (self): 
        """
        This function resets all the variables use in monster battling to their default states.
        Args: None 
        Returns: None
        """
        self.player_weapon_multiplyer = 1   # Resets player damage multiplyer on monster back to 1.
        self.monster_debuff = 1             # Resets monster attack damage debuff to 1.
        self.shield_active = False          # No shields active. 
        self.shield_active_name = None      
        self.weapon_active = False          # No weapons being used by player.
        self.weapon_active_name = None
        self.debuff_active = False          # No debuffs on monster. 
        self.debuff_active_name = None 

    def load_battle_menu (self):
        """
        This function loads all four menus which will be using in the monster battling part of the game. 
        First menu is the battle interaction menu where the player answers the math questions. The second menu 
        is the inventory where player can see all the items they currently have and choose to activate/use them. 
        The thrid menu is the menu is the menu selection menu where the user chooses if they want to go answer the 
        math question or check out their inventory. The fourth menu is the action response frame where the game tells 
        the user what is going on damage wise to their own character and the monster after the math question is answered. 
        Args: None 
        Returns: None 
        """
        self.battle_interaction_frame = Frame(self.frame, width= 100, height=100)       # Frame where the battle interaction UI goes. 
        self.battle_interaction_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)   # Placing frame onto screen. 
        self.question_var = StringVar()     # Question variable. 
        Label(self.battle_interaction_frame, image= self.sprite_dict["UI"]["question background.png"]).place(relx=0, rely=0, relwidth=0.5,relheight=1)  # Use Label to place background of menu. 
        Label(self.battle_interaction_frame,textvariable=self.question_var, font =("Arial",30), bg= ACCENT_COLOUR, fg=TEXT_COLOUR).place(relx=0.1, rely= 0.2, relwidth=0.3, relheight=0.2)  # Place label which has the question. 
        self.text_var = StringVar() # Text variable which tells user if they got question correct or wrong. 
        Label(self.battle_interaction_frame,textvariable=self.text_var, font =("Arial",20), bg= ACCENT_COLOUR, fg=TEXT_COLOUR).place(relx=0.1, rely= 0.6, relwidth=0.3, relheight=0.2)        
        self.buttons_frame = Frame(self.battle_interaction_frame,width= 100, height=100)    # Frame to put all the answer buttons. 
        self.buttons_frame.place(relx=0.5, rely= 0, relwidth=0.5, relheight=1)              # Place frame onto screen. 
        # Create and place all four answer buttons into the answer button frame. 
        self.answer_button1 = Button(self.buttons_frame, text='wrong' , font=("Arial", 20), bg="Red")   # Answer button 1.
        self.answer_button1.place(relx=0, rely=0 ,relwidth=0.5, relheight=0.5)
        self.answer_button2 = Button(self.buttons_frame, text= "wrong", font=("Arial", 20), bg= "Blue") # Answer button 2.
        self.answer_button2.place(relx=0.5, rely=0,relwidth=0.5, relheight=0.5)
        self.answer_button3 = Button(self.buttons_frame, text= "wrong", font=("Arial", 20), bg ="Orange")   # Answer button 3.
        self.answer_button3.place(relx=0, rely=0.5,relwidth=0.5, relheight=0.5)
        self.answer_button4 = Button(self.buttons_frame, text= "wrong", font=("Arial", 20), bg = "Purple")  # Answer button 4.
        self.answer_button4.place(relx=0.5, rely=0.5,relwidth=0.5, relheight=0.5)     
        # Config all the states of the buttons to allow them to be pressed and activated. 
        self.answer_button1.config(state= "normal")
        self.answer_button2.config(state= "normal")
        self.answer_button3.config(state= "normal")
        self.answer_button4.config(state= "normal")
        
        def open_inventory_frame(self): 
            """
            This function is used to open the Inventory menu.
            Args: None 
            Returns: None
            """
            self.inventory_frame = Frame(self.frame,width= 100, height=100)         # Create inventory frame.
            self.inventory_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)    # Place inventory frame onto screen.
            self.inventory_frame.lift()
            tab_frame = Frame(self.inventory_frame, background="purple")    # Create tab frame. 
            tab_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)      # Place tab frame. 
            Label(tab_frame, image=self.sprite_dict["UI"]["gradient background.png"]).place(relx=0, rely=0, relwidth=1, relheight=1)    # Place background image for menu. 
            # Create and place all the UI elements of the inventory menu.         
            Label(tab_frame, text= "Inventory", font= ('Arial', 10)).place(relx=0.1, rely=0, relwidth=0.3, relheight=0.2)
            Button(tab_frame,text="Back to Menu", command= lambda: self.menu_selection_frame.lift(), font= ('Arial', 8) ).place(relx=0.5, rely= 0, relwidth=0.4, relheight= 0.2)
            Button(tab_frame, text = "Heals Tab", command= lambda : self.update_item_buttons( tab="heals"), font= ('Arial', 10)).place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)
            Button(tab_frame, text = "Weapons Tab", command= lambda : self.update_item_buttons(tab="weapons"), font= ('Arial', 10)).place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.2)
            Button(tab_frame, text = "Shields Tab", command= lambda : self.update_item_buttons(tab="shields"), font= ('Arial', 10)).place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.2)
            Button(tab_frame, text = "Potions Tab", command= lambda : self.update_item_buttons( tab="potions"), font= ('Arial', 10)).place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.2)
            button_frame = Frame(self.inventory_frame, background= "purple")    # Create frame to put all the item buttons. 
            button_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)     # Place frame onto screen. 
            Label(button_frame, image=self.sprite_dict["UI"]["gradient background.png"]).place(relx=0, rely=0, relwidth=1, relheight=1)
            self.item1_var = StringVar()    # Item 1 button text variable. 
            self.item1_var.set("Select an Inventory Tab")
            self.item_button1 = Button(button_frame, textvariable=self.item1_var, wraplength=90, state= "disabled", font= ('Arial', 10))
            self.item_button1.place(relx=0.03, rely=0.1 ,relwidth= 0.19, relheight=0.8)
            self.item2_var = StringVar()    # Item 2 button text variable. 
            self.item_button2 = Button(button_frame, textvariable= self.item2_var, wraplength=90, state= "disabled", font= ('Arial', 10))
            self.item_button2.place(relx=0.28, rely=0.1 ,relwidth= 0.19, relheight=0.8)
            self.item3_var = StringVar()    # Item 3 button text variable. 
            self.item_button3 = Button(button_frame, textvariable= self.item3_var, wraplength=90, state= "disabled", font= ('Arial', 10))
            self.item_button3.place(relx=0.53, rely=0.1 ,relwidth= 0.19, relheight=0.8)
            self.item4_var = StringVar()    # Item 4 button text variable. 
            self.item_button4 = Button(button_frame, textvariable=self.item4_var, wraplength=90, state= "disabled", font= ('Arial', 10))
            self.item_button4.place(relx=0.78, rely=0.1 ,relwidth= 0.19, relheight=0.8)
        
        def answer_question(self): 
            """
            The function opens the menu where the user answers the question. 
            Args: None
            Returns: None
            """
            self.battle_interaction_frame.lift()    # Places the battle interaction menu to the top of all the menus. 
            self.update_battle_interaction_menu()   # Update battle interaction menu. 
            
        self.menu_selection_frame = Frame(self.frame,background="purple",width= 100, height=100)    # Create menu selection frame. 
        self.menu_selection_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)                   # Place menu selection frame onto screen. 
        self.menu_selection_frame.lift()
        
        Label(self.menu_selection_frame, image=self.sprite_dict["UI"]["gradient background.png"]).place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.info_display_var= StringVar()  # Text variable for info display. 
        self.info_display_var.set(f"Shield active: {self.shield_active}\nWeapon active: {self.weapon_active}\nEnemy debuff active: {self.debuff_active}")    
        Label(self.menu_selection_frame, textvariable=self.info_display_var , font= ("Arial", "11", "bold"), bg= ACCENT_COLOUR, fg=TEXT_COLOUR).place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.6)  # Display info using label. 
        # Buttons for user to choose what menu to open. 
        Button(self.menu_selection_frame, text= "Inventory Menu",command= lambda: open_inventory_frame(self), font= ("Arial", "16")).place(relx=0.05, rely=0.2, relwidth=0.3, relheight=0.6)
        Button(self.menu_selection_frame, text= "Answer Question",command= lambda: answer_question(self), font= ("Arial", "16")).place(relx=0.65, rely=0.2, relwidth=0.3, relheight=0.6)   
        self.action_response_frame = Frame(self.frame, bg="red")    # Create frame for action response frame.
        self.action_response_text = StringVar()     # Text variable to tell user what happened.                
        Label(self.action_response_frame, image=self.sprite_dict["UI"]["gradient background.png"]).place(relx=0, rely=0, relwidth=1, relheight=1)   # Create label to show user response. 
        Label(self.action_response_frame, textvariable=self.action_response_text, font =("Arial",22), bg= ACCENT_COLOUR, fg=TEXT_COLOUR).place(relx=0.2, rely=0.4, relheight=0.2, relwidth=0.6)
        
    def item_button_function(self, text: str, tab: str):
        """
        This funciton updates the inventory menu buttons depending on what tab is currently active.
        Args:
            text (str): Name of button that was pressed. 
            tab (str): Current inventory tab. 
        Returns: None 
        """
        name =text.split('\n', 1)[0].lower()
        if tab == "heals":  # If inventory tab is heals then the item that was used is a heal. 
            heal = self.game_data["items"]["heals"][name][0]    # Amount that will be healed.
            if (int(self.player_data["health"]) + heal) >= 600: self.player_data["health"] = 600    # Check if palyer is healed to full heal, if healed more than full health then cap the health to max health amount (600). 
            else:self.player_data["health"] += heal # If under max health then add heal amount to health. 
            self.player_health_var.set(self.player_data["health"])  # Display health value. 
            if int(self.player_health_var.get()) <=200: self.low_health(flashed= True)  # If under 200 health run low health function which flashes the health number. 
            else:self.player_health_label.config(fg="black")
        elif tab == "weapons":  # If inventory tab is weapons then the item that was used is a weapon. 
            self.weapon_active = True   # Weapon is being used by player. 
            self.weapon_active_name = name  # Name of weapon being used.
            self.player_weapon_multiplyer = self.game_data["items"]["weapons"][name][0] # Add weapon multi to player damage output. 
        elif tab == "shields":  # If inventory tab is shields then the item that was used is a shield. 
            self.shield_active= True    # Shield is being used by character.
            self.shield_active_name = name  # Name of shield being used. 
            self.shield_health =  self.game_data["items"]["shields"][name][0]   # Update shield health.
            self.player_shield_var.set(self.shield_health)      # Display shield health. 
        elif tab == "potions":  # If inventory tab is potions then the item that was used is a potion. 
            self.debuff_active = True   # Potion is being used by character.
            self.debuff_active_name = name  # Name of potion being used. 
            self.monster_debuff =  self.game_data["items"]["potions"][name][0]  # Add debuff to monster damage output. 
        self.player_data["items"][name] -= 1    # Item used so minus one from the inv data. 
        self.info_display_var.set(f"Shield active: {self.shield_active}\nWeapon active: {self.weapon_active}\nEnemy debuff active: {self.debuff_active}")   # Update data text. 
        self.update_item_buttons(tab = tab) # Update item buttons.
         
    def update_item_buttons(self, tab:str):
        """
        This function updates the item buttons.  
        Args:
            tab (str): Inventory tab which is currently active. 
        Returns: None
        """
        item_names = list(self.game_data["items"][tab].keys())
        var_list = [self.item1_var, self.item2_var, self.item3_var, self.item4_var]
        buttons_list = [self.item_button1, self.item_button2, self.item_button3, self.item_button4]
    
        active = {"weapons": [self.weapon_active, self.weapon_active_name], 
                    "shields": [self.shield_active, self.shield_active_name], 
                    "potions": [self.debuff_active, self.debuff_active_name], 
                    "heals": [False, None]}
        if active.get(tab)[0] ==False:
            button_state = "active"
        else:button_state = "disabled"
        # Config all the buttons to have new functions if tab has changed. 
        self.item_button1.config( command = lambda: self.item_button_function(self.item1_var.get(), tab = tab),state = button_state) # , bg= "Green" if self.item1_var.get().split('\n', 1)[0] == active.get(tab)[1] else "SystemButtonFace"           
        self.item_button2.config( command = lambda:  self.item_button_function(self.item2_var.get(), tab = tab), state = button_state)    
        self.item_button3.config( command = lambda: self.item_button_function( self.item3_var.get(), tab = tab), state =button_state)          
        self.item_button4.config(command = lambda: self.item_button_function(self.item4_var.get(), tab = tab), state =button_state)
        
        
        for counter in range(0, 4): # Loop through all buttons. 
            var_list[counter].set("") # Clear the text of each buttonn
            if counter <= len(item_names)-1 and var_list[counter].get() != "none": # Check if item button has an item linked to it. 
                amount = 0  # Create amount var of item. 
                active_text = ""    # Create text var. 
                if item_names[counter] in self.player_data["items"]: # If player has item. 
                    amount = self.player_data["items"][item_names[counter]]
                    if amount == 0:     # If player has none of that item then disable item button. 
                        buttons_list[counter].config(state="disabled")
                elif item_names[counter] not in self.player_data["items"]: # If player doesn't have item.
                    buttons_list[counter].config(state="disabled")  # Disable button so user can't use the item. 
                if  item_names[counter] == active.get(tab)[1]:  # If player is currently using the item. 
                    buttons_list[counter].config(bg="#a7f37e", state="disabled")    # Highlight it green and disable it so user can't use more items. 
                    active_text = f"\nITEM IN USE"        
                else: # If player isn't currently using it. 
                    buttons_list[counter].config(bg="SystemButtonFace")  # Normal colour.         
                if tab == "heals" and self.player_data["health"] >=600: # If item is a heal and player already at max health.
                    active_text = f"\nFULL HEALTH ALREADY"
                    buttons_list[counter].config( state="disabled") # Don't let user use a heal item since they are at max health. 
                description = self.game_data["items"][tab][item_names[counter]][1]
                var_list[counter].set(f"{item_names[counter].title()}\n Amount: {amount}\n Description: {description}"+active_text)               
            else: # Not in item dict (button will be empty).               
                buttons_list[counter].config(state="disabled")
                var_list[counter].set("none")
        
    def update_battle_interaction_menu(self): 
        """
        This function updates the battle interaction menu where the user does the math question to attack the monster.
        Args: None
        Returns: None
        """ 
        self.text_var.set("Answer Question")    # Text to tell user to answer question. 
        answer_tuple = Math.generate_question(question_type= self.monster_data[self.monster_name], num_variables=self.player_data["level"]+1)   # Create math question and answer for user to do. 
        self.question_var.set(f"{answer_tuple[1]} = ?") # Display maths question to user. 
        buttons_randomized = [self.answer_button1, self.answer_button2, self.answer_button3, self.answer_button4]   
        random.shuffle(buttons_randomized)  # Randomise the answer buttons. 
        wrong_answers = Math.create_wrong_answers(answer = answer_tuple[0]) # Randomly generate the wrong answers for the other three answer buttons. 
        # Config all the answer buttons to place the number answers in them and make it so the button with the correct answer is the one that makes player attack monster.
        buttons_randomized[0].config(text= answer_tuple[0],  command=lambda: self.player_attack("correct", number= answer_tuple[0], answer=answer_tuple[0]), state="normal")
        buttons_randomized[1].config(text= wrong_answers[0], command=lambda: self.player_attack("wrong", number= wrong_answers[0], answer=answer_tuple[0]), state="normal")
        buttons_randomized[2].config(text= wrong_answers[1], command=lambda: self.player_attack("wrong", number= wrong_answers[1], answer=answer_tuple[0]), state="normal")
        buttons_randomized[3].config(text= wrong_answers[2], command=lambda: self.player_attack("wrong", number= wrong_answers[2], answer=answer_tuple[0]), state="normal")

    def cutscreen(self): 
        """
        This function creates the cutscreen. 
        Args: None
        Returns: None
        """
        # Create the black triangles which are displayed during the cutscreen. 
        self.canvas.create_polygon(0,0, 0, 600, 400, 600, fill= "black", width= 0)
        self.game_instance.after(250, lambda: self.canvas.create_polygon(0,600, 840, 600, 0, 300, fill= "black", width= 0))
        self.game_instance.after(500, lambda: self.canvas.create_polygon(400,600, 840, 0, 840, 600, fill= "black", width= 0))  
        self.game_instance.after(750, lambda: self.canvas.create_polygon(100,0, 840, 0, 840, 200, fill= "black", width= 0))     
        self.game_instance.after(1000, lambda: self.canvas.create_polygon(0,0, 300, 0, 0, 600, fill= "black", width= 0))
        self.game_instance.after(1250, lambda: self.canvas.create_rectangle(0, 0, 840, 600, fill="black", width= 0))
       
    def load_battle_canvas(self):        
        """
        This function loads all the images and things onto the battle canvas. 
        Args: None
        Return: None
        """
        self.canvas.delete("all")   # Clear the canvas to prepare to create the monster battling scene.
        self.player_labelframe = LabelFrame(self.canvas, background="White") # Create the labelframe for the player card which displays player info. 
        self.player_labelframe.place(relx=0.5, rely= 0.8, relwidth=0.5, relheight=0.2)
        Label(self.player_labelframe, image=self.sprite_dict["UI"]["display box.png"]).place(relx=0, rely=0, relwidth=1, relheight=1)   # Background for player card. 
        self.player_health_var = StringVar()    # Variable for player health. 
        self.player_health_var.set(self.player_data["health"])  # Display player health. 
        # Labels to tell user info. 
        Label(self.player_labelframe, text= "Player", font =("Arial",20, "bold"), background="White").place(relx=0.2, rely=0.05 , relwidth= 0.6, relheight=0.4) 
        Label(self.player_labelframe, text="Health:", font =("Arial",18), background="White").place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.2)
        self.player_health_label = Label(self.player_labelframe, textvariable=self.player_health_var, font =("Arial",18), background="White")   # Place player health. 
        self.player_health_label.place(relx= 0.5, rely=0.4, relwidth= 0.2, relheight=0.2)
        if int(self.player_health_var.get()) <=200: self.low_health(flashed= True)  # If player health is under 200 then start flashing health. 
        else:self.player_health_label.config(fg="black")
        self.player_shield_var = StringVar()    # Player shield health variable. 
        self.player_shield_var.set(self.shield_health)        
        Label(self.player_labelframe, text="Shields:", font =("Arial",18), background="White").place(relx=0.3, rely=0.7, relwidth=0.2, relheight=0.2)   # Label to tell player what the shield number is. 
        Label(self.player_labelframe, textvariable=self.player_shield_var, font =("Arial",18), fg= "blue", background="White").place(relx= 0.5, rely=0.7, relwidth= 0.2, relheight=0.2) # Display shield number onto screen. 
        self.monster_labelframe = LabelFrame(self.canvas, background="White")   # Create the labelframe for the player card which displays monster info.  
        self.monster_labelframe.place(relx=0, rely= 0, relwidth=0.5, relheight=0.2)   
        Label(self.monster_labelframe, image=self.sprite_dict["UI"]["display box.png"]).place(relx=0, rely=0, relwidth=1, relheight=1)   # Background for monster card. 
        self.monster_name_var = StringVar() # Monster name variable. 
        self.monster_name_var.set(self.monster_name.title())
        self.monster_health_var = StringVar()
        self.monster_health_var.set(self.monster_health)
        Label(self.monster_labelframe, textvariable= self.monster_name_var ,font =("Arial",20, "bold"), background="White").place(relx=0.2, rely=0.05 , relwidth= 0.6, relheight=0.4) # Place monster name. 
        Label(self.monster_labelframe, text="Health:", font =("Arial",18), background="White").place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.2)   # Label to tell user what the monster health number is. 
        Label(self.monster_labelframe,textvariable= self.monster_health_var, font =("Arial",18), background="White").place(relx= 0.5, rely=0.4, relwidth= 0.2, relheight=0.2)   # Place monster health onto screen. 
        self.bg = self.canvas.create_image(-260,0, anchor ='nw',image=self.battle_sprite_dict["battle bg.png"]) # Monster battle background. 
        self.player = self.canvas.create_image(60,200, anchor ='nw',image=self.battle_sprite_dict["character.png"]) # display character sprite on canvas. 
        if f"{self.monster_name}.png" in self.sprite_dict["Battle"].keys(): name = f"{self.monster_name}.png"   # If the sprite of the monster the user if currently fighting exists then display it otherwise display placeholder sprite.
        else: name = "placeholder.png"            
        self.monster = self.canvas.create_image(480,0, anchor ='nw',image=self.sprite_dict["Battle"][name]) # Display monster sprite on canvas.
        
    def low_health(self, flashed:bool = False):
        """
        This function makes the player health number flash if its below 200 health to tell user that they should think about healing.
        Args:
            flashed (bool, optional): If it on the red flashed cycle or not. Defaults to False.
        Returns: None
        """
        if int(self.player_health_var.get()) <=200: # If player health is under 200.
            if self.player_health_label.winfo_exists(): # Check if player health var exists or not. 
                self.player_health_label.config(fg="red" if flashed == False else "Black")  # Changes the colour of the health number depending on the flash cycle it is currently on. 
            else: # If var doesn't exist then don't don anything. 
                return 
            new_flashed = True if flashed == False else False # Update flash cycle so now it flashes to the other colour the next time this function is run.
            
            self.game_instance.after(200, lambda: self.low_health(flashed = new_flashed))  # After 200 miliseconds run this function again to cause the number to keep flashing until stopped.
            
        else:   # If player health over 200 then stop flashing. 
            self.player_health_label.config(fg="black")
        
    def animate_change_exponential(self, var, current:int, target:int, duration:int): 
        """
        This function make it so that when damage is taken the health number decrease is animated that it decreases exponentally. 

        Args:
            var : Variable which is being animated.
            current (int): Current value. 
            target (int): Value that is going to be reached. 
            duration (int): Time to animate this whole change. 

        Raises:
            ValueError: If player doesn't pass through a variable to animate then raise an error. 
        """
        if var is None: # Raise error if no var is passed through. 
            raise ValueError("string_var must be provided")
        diff = target - current     # The difference between the target and current number. 
        steps = 100  # Number of steps in the animation.
        decay_factor = 0.95  # Exponential decay factor.
        delay = int(duration * 1000 / steps)  # Calculate delay in milliseconds based on total duration.

        def update_value(step:int):
            """
            This function updates the value by a certain incriment to animate the damage decrease.

            Args:
                step (int): Current step it is on. 
            """
            nonlocal current
            if step < steps:    # If variable still needs to be updated, target not reached.
                current += diff * (decay_factor**step - decay_factor**(step + 1))   # Calculate number to decrease by exponentially. 
                if int(current) != last_displayed[0]:   
                    last_displayed[0] = int(current)
                    var.set(last_displayed[0])  # Update number variable. 
                self.game_instance.after(delay, update_value, step + 1)
            else:
                var.set(target)  # Ensure the final value is displayed correctly.
        last_displayed = [current]  
        update_value(0) # Start to animate the decrease in the number variable. 
        
    def player_attack (self, mode:str, number:int, answer:int):
        """
        This function is run when user has answered the question and depending if they got it correct or not deal deal a certain amount of damage to the monster.
        Args:
            mode (str): If user got the question correct or not. 
            number (int): The number of the answer they chose.
            answer (int): The actual answer of the question. 
        """
        # Disable all of the answer buttons so that user can't press them again. 
        self.answer_button1.config(state= "disabled")
        self.answer_button2.config(state= "disabled")
        self.answer_button3.config(state= "disabled")
        self.answer_button4.config(state= "disabled")
        damage = random.randint(100, 130)   # Calculate the amount of damage the player could deal to the monster. 
        damage = int(damage *self.player_weapon_multiplyer) # Apply damage multi to player damage. 
        if mode == "correct":   # If user got question correct.    
            self.text_var.set("RIGHT!") # Display text telling user that they got it correct. 
            self.monster_health -= damage   # Deal the calculated damge to the monster. 
        elif mode == "wrong":   # If user got question wrong. 
            self.text_var.set(f"WRONG! Answer: {answer}")   # Display text telling user that they got it wrong and display the correct answer.
            damage = 0  # Deal zero damage to monster since user got question wrong.
        self.question_var.set(f"{self.question_var.get()[:-1]}{number}")  # Update question to show the answer number user chose.
            
        def attack(self): 
            """
            This function updates the monster health and animates the damage taken using the animate_change_exponential function. Also shows text to user that tells them how much 
            damage was dealt to monster. 
            """
            self.animate_change_exponential(var = self.monster_health_var,current= int(self.monster_health_var.get()), target =  int(self.monster_health_var.get()) - damage, duration = 1.5)   # Animate damage decrease of monster health value.   
            self.action_response_frame.place(relx=0, rely=0, relwidth = 1, relheight = 1)
            self.action_response_frame.lift() # Show action response menu.
            self.action_response_text.set(f"Player dealt {damage} damage to monster") # Tell user how much damage was dealt to monster.
        self.game_instance.after(2000,lambda: attack(self)) # Run attack function after 2 seconds. 
        self.game_instance.after(5000, lambda: self.monster_attack()) # After 5 seconds then it is monster's time to attack player, so run monster_attack function.
    
    def monster_attack(self): 
        """
        This function is run when its time for for the monster to attack the player. 
        Args: None 
        Returns: None
        """
        if self.monster_health <1:  # Check if monster is dead yet. 
            self.exit_menu()        # If monster is dead then end monster battle interaction. 
            return
        damage_multiplyer = 1 + self.player_data["level"] *0.05 # Damage multi which will be applyed depending on the level the player is currently on 
        base_damage = random.randint(90, 110)   # Calculate the damage that the monster will deal. 
        damage = int(base_damage * damage_multiplyer *self.monster_debuff)  # Add all damage multis and debuffs to the base damage output to get the actual damage the monster will deal.    
        if int(self.player_shield_var.get()) == 0:  # If player doesn't have shield active then deal damage to player health.
            self.player_data["health"] -= damage
            self.animate_change_exponential(var = self.player_health_var,current= int(self.player_health_var.get()), target =  self.player_data["health"], duration = 1.5)  # Animate the change in player health number.  
        else:   # If player has shield active then deal damage to shield.
            self.shield_health -= damage   
            if self.shield_health < 0:  # If damage dealt to the shield makes it so shield heal is less than 0.
                self.shield_health = 0  # Reset the shield health so it is at zero indicating there is no more shield active to protect player.    
            self.animate_change_exponential(var = self.player_shield_var,current= int(self.player_shield_var.get()), target =  self.shield_health, duration = 1.5)  # Animate the change in player health number.  
        self.game_instance.after(1600, lambda:self.low_health(flashed= True) if int(self.player_health_var.get()) <=200 else self.player_health_label.config(fg="black"))   # If player health is under 200 then start flashing. 
        self.reset_stat_vars()  # Reset all battling variables to prepare for the next battle interaction. 
        self.info_display_var.set(f"Shield active: {self.shield_active}\nWeapon active: {self.weapon_active}\nEnemy debuff active: {self.debuff_active}")    
        self.action_response_text.set(f"Monster dealt {damage} damage to player")    # Text to tell user how much damage was dealt.
        self.game_instance.after(4000, lambda:self.player_death() if self.player_data["health"] <1 else self.menu_selection_frame.lift())   # If player health under 0 then end game, else go to next battle interaction.


    def exit_menu(self):
        """
        This function is run when the player defeats the monster and the function displays a menu telling player what items the monster dropped. 
        Args: None 
        Returns: None
        """
        clear_frame(self.frame) # Clear menu frame to prepare for new menu. 
        items = self.item_drops()   # Run item_drops function to get the items which the monster dropped. 
        text =""    
        for key, value in items.items():
            text += f"\n{key}: {value}" # Update text to show what items were dropped. 
        Label(self.frame, image= self.sprite_dict["UI"]["gradient background.png"]).place(relx=0, rely=0, relheight=1, relwidth=1)  # Background for menu.
        Label(self.frame, text = f"Items Dropped{text}", font= ("Arial", 12), fg=TEXT_COLOUR, bg= ACCENT_COLOUR).place(relx=0.35, rely=0.05, relheight=0.6,relwidth=0.3)    # Label to display the items that were dropped to player. 
        Button(self.frame, text = "Exit", command= lambda:self.monster_death()).place(relx=0.4, rely=0.75, relheight=0.2 ,relwidth=0.2)    # Exit button for user to go back to map exploration part of the game. 
        
    def item_drops(self):
        """
        This function creates the items that will be given to the player after they defeat the monster. 
        Args: None
        Returns:
            item (dict): This dictionary holds the items that will be given to player and the amounts of those items. 
        """
        loot_table=self.game_data["loot table"] # Get the loot table drop rates.
        items = {"mini heal" : 3}   # Always give player 2 mini heals. 
        tab_randomised = ["heals", "weapons", "shields", "potions"]
        random.shuffle(tab_randomised) # Randomise the item groups that will be dropped to the player. 
        rand_amount = random.randint(2,5)   # Randomise the amount of the items the player will get. 
        for index in range(0,rand_amount):  # Loop through the item drop amount. 
            current = 0
            tab = tab_randomised[random.randint(0,3)]   # Randomise the item type.
            rand = random.randint(1,100)    # Random number to comapare to loot table to see what rareity of loot player gets.
            item_pool = loot_table.get(tab) # Get the items that can be given to player in the item type group.
            for key, value in item_pool.items():    # Loop through the drop rates to calculate what item to give player. 
                if rand <= value: 
                    current = value
            if current in items.keys(): # If player has item in inv then add 1 to inv amount.
                items[key] +=1
            else:   # If player doesn't have item then add it to inv. 
                items[key] = 1   
        for key, value in items.items():    # Update player data with the items that were dropped. 
            if key in self.player_data["items"].keys(): self.player_data["items"][key] += value
            else:  self.player_data["items"][key] = value  
        return items    # Return the dict of the items dropped and their amount.
        
    def monster_death (self):
        """
        This function clears the screen and plays the cutscreen to indicate to user that they have defeated the user and are going back to the 
        map exploration part of the game. 
        Args: None
        Returns: None
        """
        clear_frame(self.game_instance.menu_frame)  # Clear the menu frame. 
        self.player_labelframe.destroy()    # Delete player info card. 
        self.monster_labelframe.destroy()   # Delete monster info card.
        self.cutscreen()    # Play cutscreen animation.
        self.game_instance.after(1500, lambda: self.exit_battle())  # After cutscrren finishes exit monster battling part of game. 
        return
        
    def player_death (self): 
        """
        If player gets defeated by monster then end game and tell user that game has ended. Display some infomation about their playthrough of the game like
        high score, etc. 
        Args: None
        Returns: None
        """
        clear_frame(self.game_instance) # Delete everything on screen. 
        
        Label(self.game_instance, text=f"GAME OVER", font =("Arial",100)).place(rely=0.2,relx=0.1, relheight=0.3, relwidth=0.8) # Label to tell player that ga  me is over and they have died.
        high_score = self.player_data["high score"] if self.player_data["score"]< self.player_data["high score"] else self.player_data["score"] # Update high score if they got more score this playthrough than previous high score. 
        score = self.player_data["score"]   # Current score this playthrough. 
        deaths = int(self.player_data["deaths"] ) +1    # Update death amount since they just died. 
        Label(self.game_instance, text=f"Username:{self.username}\nScore:{score}\nHigh Score:{high_score}\nDeaths:{deaths}", font =("Arial",30)).place(rely=0.5,relx=0.1, relwidth=0.8) # Display the player info like score, high score and death count.
        Button(self.game_instance, command= lambda:self.game_instance.destroy() , text= "Close Game").place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.1)    # Close game button for user to exit the game. 
       
    def exit_battle(self): 
        """
        This function is used to update the score and prepares the game to go back to map exploration. 
        Args: None
        Returns: None
        """
        self.player_data["score"] += 100    # Update score.
        self.game_instance.map_handler.delete_monster_cord(self.monster_cord, self.monster_name)    # Delete the monster which was just defeated from the monster storage.
        self.game_instance.movement_allowed = True  # Allow movement since going back to map exploration. 
        self.game_instance.load_main_menu() # Load main menu.
        self.game_instance.auto_save(loop=False)    # Turn auto-save back on.
        self.game_instance.game_loop()  # Start game loop again.
        
class Math:         
    def create_wrong_answers(answer: int) -> list:
        """
        This function is used to randomly generate wrong answers by getting the real answer and choosing random numbers close to it.
        
        Args:
            answer (int): The answer number to the question.

        Returns:
            list: List of all the generated wrong answers. 
        """
        list = []   # List to store all the wrong answers. 
        counter = 3 # How many wrong answers to generate. 
        start = answer - 7  # Start range.
        end = answer +7     # End range.
        while counter != 0:
            wrong_answer = random.randint(start,end)    # Choose a random number between the ranges. 
            if wrong_answer != answer and wrong_answer not in list:     # If number chosen is not the answer or has previously been chosen.
                list.append(wrong_answer)   # Add that number to the wrong numbers list. 
                counter -= 1
        return list # Return the wrong numbers list. 
    
    def generate_question(question_type:str, num_variables:int=2) -> tuple:
        """
        This function generates 5 types of math questions (+,-,/,x and algebraic), and also calcuates the correct answer to the question. 

        Args:
            question_type (str): What type of question to generate
            num_variables (int, optional): How many number constants in the question. Defaults to 2.

        Returns:
            tuple: Tuple which has the answer and the math question as a string. 
        """
        def generate_addition_question(num_variables:int) -> tuple:
            """
            This question creates a addition question and its answer. 

            Args:
                num_variables (int): How many number constants in question.

            Returns:
                tuple : Tuple which has the answer and the math question as a string. 
            """
            operands = [random.randint(1, 10) for _ in range(num_variables)]
            question = ' + '.join(map(str, operands))   # Create math question string. 
            answer = sum(operands)  # Calculate answer from string.
            return answer, question # Return answer and question string in tuple.

        def generate_subtraction_question(num_variables:int) -> tuple:
            """
            This function creates a subtraction question and its answer.

            Args:
                num_variables (int): How many number constants in question.

            Returns:
                tuple: Tuple which has the answer and the math question as a string. 
            """
            operands = [random.randint(1, 10) for _ in range(num_variables)]
            question = ' - '.join(map(str, operands))   # Create math question string. 
            answer = reduce(operator.sub, operands)     # Calculate answer from string.
            return answer, question # Return answer and question string in tuple.

        def generate_multiplication_question(num_variables:int) -> tuple:
            """
            This function creates a multiplication question and its answer. 

            Args:
                num_variables (int): How many number constants in question.

            Returns:
                tuple: Tuple which has the answer and the math question as a string. 
            """
            operands = [random.randint(1, 10) for _ in range(num_variables)]
            question = ' * '.join(map(str, operands))   # Create math question string. 
            answer = reduce(operator.mul, operands)     # Calculate answer from string.
            return answer, question.replace("*", "x")   # Return answer and question string in tuple.

        def generate_division_question(num_variables):
            """
            This function creates a division question and its answer.  

            Args:
                num_variables (int): How many number constants in question.

            Returns:
                tuple: Tuple which has the answer and the math question as a string. 
            """
            operands = [random.randint(1, 10) for _ in range(num_variables)]
            div_num = reduce(operator.mul, operands)    # Calculate the answer first and then divide the the answer number.
            operands.reverse()     
            operands.insert(0,div_num)
            question = ' / '.join(map(str, operands))    # Create math question string. 
            question = question[:-4]
            answer = operands[-1]
            return answer, question # Return answer and question string in tuple.
        
        def generate_mixed_algebra_question(num_variables:int) -> tuple:
            """
            This function creates algebraic question and its answer. 

            Args:
                num_variables (int): How many number constants in question.

            Returns:
                tuple: Tuple which has the answer and the math question as a string. 
            """
            while True: # Loop to keep generating questions until one is found which doesn't give a decimal answer. 
                operators = ['+', '-', '*', '/']    # All the operators that can be used in the question.
                operands = [random.randint(1, 10)]  # The range of number constants that can be used.
                op_symbols = []
                for _ in range(num_variables - 1):   # Loop to generate the question.
                    operator = random.choice(operators)
                    
                    if operator == '/': # If operator is division then use a special method to create next constant number so that no decimal answers are created. 
                        prev_operand = operands.pop()           # Remove the previous number (last operand).
                        next_operand = random.randint(1, 10)    # Generate a new operand and multiply with the previous one.
                        numerator = prev_operand * next_operand # Append the numerator (product) back to operands.
                        operands.append(numerator)              # Append the divisor.
                        operands.append(next_operand)
                    else:   # If not division operator continue as normal to create the question.
                        next_operand = random.randint(1, 10)    # Generate random number constants.
                        operands.append(next_operand)
                    op_symbols.append(operator)

                question_parts = [] # Construct the question
                for i in range(num_variables - 1):  # Loop through the question and add the number constants and the next operator. 
                    question_parts.append(str(operands[i]))
                    question_parts.append(op_symbols[i])
                question_parts.append(str(operands[-1]))
                question = ' '.join(question_parts) # Finish creating question by removing white spaces.
                answer = eval(question) # Evaluate the question using eval to get number answer.
                
                if float(answer).is_integer() == True:  # If answer is not a decimal.
                    return int(answer), question.replace("*", "x")  # Return answer and question string in tuple.
                else: 
                    continue    # Restart and make a new question. 
        # If statment block to see what type of question needs to be made.
        if question_type == 'addition': # If question type if addition then make addition question and answer. 
            return generate_addition_question(num_variables)    
        elif question_type == 'subtraction':    # If question type is subtraction then make subtraction question and answer.
            return generate_subtraction_question(num_variables)
        elif question_type == 'multiplication': # If question type is multiplication then make multiplication question and answer.
            return generate_multiplication_question(num_variables)
        elif question_type == 'division':       # If question type is division then make division question and answer.
            return generate_division_question(num_variables)
        elif question_type == 'algebra':        # If question type is algebra then make algebra question and answer.
            return generate_mixed_algebra_question(num_variables)
        else:   # Raise error if program doesn't specify question type when calling this function. 
            raise ValueError("Invalid question type. Choose from 'addition', 'subtraction', 'multiplication', 'division', 'algebra'.")

        
