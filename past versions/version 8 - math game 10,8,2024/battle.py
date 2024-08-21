
from tkinter import *
import random  
import json 
import operator
from functools import reduce

MAP_SIZE = 40 
WINDOW_SIZE_HEIGHT = 600  
WINDOW_SIZE_WIDTH = 1200  
GRID_SIZE = 40
VIEWPORT_SIZE_HEIGHT = WINDOW_SIZE_HEIGHT // GRID_SIZE  
VIEWPORT_SIZE_WIDTH = WINDOW_SIZE_WIDTH // GRID_SIZE 

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

def mass_place_forget(*args):
    for widget in args: 
        widget.place_forget()

class Battle():

    def __init__(self, *args, **kwargs):   

        with open("game_data.json") as file: 
            self.game_data = json.load(file)
            self.monster_data =  self.game_data["monster data"]

        self.monster_name = kwargs ["monster_name"]
        self.player_data = kwargs["data"]
        self.game_instance = kwargs["parent"]
        self.monster_cord = kwargs["monster_cord"]
        self.battle_sprite_dict = kwargs["sprite_dict"]["Battle"]
        
        
        self.reset_stat_vars()

        self.monster_health = random.randint(400, 700)
        self.canvas = self.game_instance.canvas

        self.frame = self.game_instance.menu_frame
        clear_frame(self.frame)

        self.cutscreen()

        self.game_instance.after(1500, lambda: self.load_battle_canvas())
        self.game_instance.after(1500, lambda: self.load_battle_menu())
        self.game_instance.after(1500, lambda: self.canvas.move(self.player, 100, 100))
        
    def reset_stat_vars (self): 
        self.shield_health = 0 
        self.player_weapon_multiplyer = 1
        self.monster_debuff = 1 
        
        self.shield_active = False
        self.shield_active_name = None
        self.weapon_active = False
        self.weapon_active_name = None
        self.debuff_active = False
        self.debuff_active_name = None 

    def load_battle_menu (self):
        
        """
        Frame where u do all the math questions
        
        """

        self.battle_interaction_frame = Frame(self.frame, width= 100, height=100)
        self.battle_interaction_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)
        
        #self.question_frame = Frame(self.battle_interaction_frame, width= 100, height=100)
        #self.question_frame.place(relx=0, rely= 0, relwidth=0.5, relheight=1)
        
        #Label(self.question_frame, text="Question Menu", font =("Arial",30)).place(relx=0.2, rely= 0, relwidth=0.6, relheight=0.2)

        self.question_var = StringVar()
        Label(self.battle_interaction_frame,textvariable=self.question_var, font =("Arial",30)).place(relx=0.1, rely= 0.2, relwidth=0.3, relheight=0.2)
        self.text_var = StringVar()
        Label(self.battle_interaction_frame,textvariable=self.text_var, font =("Arial",20)).place(relx=0.1, rely= 0.6, relwidth=0.3, relheight=0.2)

        self.buttons_frame = Frame(self.battle_interaction_frame,width= 100, height=100)
        self.buttons_frame.place(relx=0.5, rely= 0, relwidth=0.5, relheight=1)
        
        self.answer_button1 = Button(self.buttons_frame, text='wrong' , font=("Arial", 20), bg="Red")
        self.answer_button1.place(relx=0, rely=0 ,relwidth=0.5, relheight=0.5)
        self.answer_button2 = Button(self.buttons_frame, text= "wrong", font=("Arial", 20), bg= "Blue")
        self.answer_button2.place(relx=0.5, rely=0,relwidth=0.5, relheight=0.5)
        self.answer_button3 = Button(self.buttons_frame, text= "wrong", font=("Arial", 20), bg ="Orange")
        self.answer_button3.place(relx=0, rely=0.5,relwidth=0.5, relheight=0.5)
        self.answer_button4 = Button(self.buttons_frame, text= "wrong", font=("Arial", 20), bg = "Purple")
        self.answer_button4.place(relx=0.5, rely=0.5,relwidth=0.5, relheight=0.5)     
        

        self.answer_button1.config(state= "normal")
        self.answer_button2.config(state= "normal")
        self.answer_button3.config(state= "normal")
        self.answer_button4.config(state= "normal")
        
        
        """
        
        Inventory Frame 
        
        """
        def open_item_frame(self): 
            

         
            self.item_frame = Frame(self.frame,width= 100, height=100)
            self.item_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)
            self.item_frame.lift()
            tab_frame = Frame(self.item_frame, background="purple")
            tab_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)
            
            
            Label(tab_frame, text= "Inventory", font= ('Arial', 10)).place(relx=0.1, rely=0, relwidth=0.3, relheight=0.2)
            Button(tab_frame,text="Back to Menu", command= lambda: self.menu_selection_frame.lift(), font= ('Arial', 8) ).place(relx=0.5, rely= 0, relwidth=0.4, relheight= 0.2)
            Button(tab_frame, text = "Heals Tab", command= lambda : self.update_item_buttons( tab="heals"), font= ('Arial', 10)).place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)
            Button(tab_frame, text = "Weapons Tab", command= lambda : self.update_item_buttons(tab="weapons"), font= ('Arial', 10)).place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.2)
            Button(tab_frame, text = "Shields Tab", command= lambda : self.update_item_buttons(tab="shields"), font= ('Arial', 10)).place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.2)
            Button(tab_frame, text = "Potions Tab", command= lambda : self.update_item_buttons( tab="potions"), font= ('Arial', 10)).place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.2)
            
            button_frame = Frame(self.item_frame, background= "purple")
            button_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
            
            self.item1_var = StringVar()
            self.item1_var.set("Select an Inventory Tab")
            self.item_button1 = Button(button_frame, textvariable=self.item1_var, wraplength=90, state= "disabled", font= ('Arial', 10))
            self.item_button1.place(relx=0.03, rely=0.1 ,relwidth= 0.19, relheight=0.8)
            self.item2_var = StringVar()
            self.item_button2 = Button(button_frame, textvariable= self.item2_var, wraplength=90, state= "disabled", font= ('Arial', 10))
            self.item_button2.place(relx=0.28, rely=0.1 ,relwidth= 0.19, relheight=0.8)
            self.item3_var = StringVar()
            self.item_button3 = Button(button_frame, textvariable= self.item3_var, wraplength=90, state= "disabled", font= ('Arial', 10))
            self.item_button3.place(relx=0.53, rely=0.1 ,relwidth= 0.19, relheight=0.8)
            self.item4_var = StringVar()
            self.item_button4 = Button(button_frame, textvariable=self.item4_var, wraplength=90, state= "disabled", font= ('Arial', 10))
            self.item_button4.place(relx=0.78, rely=0.1 ,relwidth= 0.19, relheight=0.8)

        
        
        """
        
        Select menu Frame 
        
        """
        def answer_question(self): 
            self.battle_interaction_frame.lift()
            self.update_battle_interaction_menu()
            self.game_instance.after(1000, lambda: self.timer())

            
        self.menu_selection_frame = Frame(self.frame,background="purple",width= 100, height=100)
        self.menu_selection_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)
        self.menu_selection_frame.lift()
        
        
        self.info_display_var= StringVar()
        self.info_display_var.set(f"Shield active: {self.shield_active}\nWeapon active: {self.weapon_active}\nEnemy debuff active: {self.debuff_active}")
        
        Label(self.menu_selection_frame, textvariable=self.info_display_var , background= "purple", font= ("Arial", "10", "bold")).place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.6)
        
        Button(self.menu_selection_frame, text= "Item Menu",command= lambda: open_item_frame(self), font= ("Arial", "16")).place(relx=0.05, rely=0.2, relwidth=0.3, relheight=0.6)
        Button(self.menu_selection_frame, text= "Answer Question",command= lambda: answer_question(self), font= ("Arial", "16")).place(relx=0.65, rely=0.2, relwidth=0.3, relheight=0.6)
        

        
        '''

        Action response frame
    
        '''
        
        self.action_response_frame = Frame(self.frame, bg="red")
        self.action_response_text = StringVar()
        
        Label(self.action_response_frame, textvariable=self.action_response_text, font =("Arial",18)).pack()#place(relx=0.4, rely= 0, relwidth=0.5, relheight=0.2)
        
        
    
    
    
    
    def item_button_function(self, text: str, tab: str):
        print(' button press, item name: ', text , "tab:", tab)
        name =text.split('\n', 1)[0]
        if tab == "heals":
            heal = self.game_data["items"]["heals"][name][0]
            self.player_data["health"] += heal
            self.player_health_var.set(self.player_data["health"])
            if int(self.player_health_var.get()) <=200: self.low_health(flashed= True)
            else:self.player_health_label.config(fg="black")

        elif tab == "weapons": 
            self.weapon_active = True 
            self.weapon_active_name = name
            self.player_weapon_multiplyer = self.game_data["items"]["weapons"][name][0]
            
        elif tab == "shields":
            self.shield_active= True
            self.shield_active_name = name
            self.shield_health =  self.game_data["items"]["shields"][name][0]
            self.player_shield_var.set(self.shield_health)
        elif tab == "potions": 
            self.debuff_active = True 
            self.debuff_active_name = name 
            self.monster_debuff =  self.game_data["items"]["potions"][name][0]
        
        print(f"weapon multi: {self.player_weapon_multiplyer}\n shield: {self.shield_health}\n monster debuff {self.monster_debuff}")
        
        self.player_data["items"][name] -= 1      
        self.info_display_var.set(f"Shield active: {self.shield_active}\nWeapon active: {self.weapon_active}\nEnemy debuff active: {self.debuff_active}")
        self.update_item_buttons(tab = tab)
        
      
        
                
    def update_item_buttons(self, tab:str):
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
                
            
            self.item_button1.config( command = lambda: self.item_button_function(self.item1_var.get(), tab = tab),state = button_state, bg= "Green" if self.item1_var.get().split('\n', 1)[0] == active.get(tab)[1] else "SystemButtonFace"  )         
            self.item_button2.config( command = lambda:  self.item_button_function(self.item2_var.get(), tab = tab), state = button_state, bg= "Green" if self.item2_var.get().split('\n', 1)[0] == active.get(tab)[1] else "SystemButtonFace")    
            self.item_button3.config( command = lambda: self.item_button_function( self.item3_var.get(), tab = tab), state =button_state, bg= "Green" if self.item3_var.get().split('\n', 1)[0] == active.get(tab)[1] else "SystemButtonFace")          
            self.item_button4.config(command = lambda: self.item_button_function(self.item4_var.get(), tab = tab), state =button_state, bg= "Green" if self.item4_var.get().split('\n', 1)[0] == active.get(tab)[1] else "SystemButtonFace")

        
            
            
            for counter in range(0, 4):
                var_list[counter].set("")
                
                if counter <= len(item_names)-1 and var_list[counter].get() != "none": # check if in item dict
                    amount = 0        
                    active_text = ""
                    if  item_names[counter] in self.player_data["items"]: #item in inv
                        amount = self.player_data["items"][item_names[counter]]
                        if amount == 0: 
                            buttons_list[counter].config(state="disabled")
                    
                    elif item_names[counter] not in self.player_data["items"]: #item not in inv
                        buttons_list[counter].config(state="disabled")

                    if  item_names[counter] == active.get(tab)[1]: 
                        buttons_list[counter].config(bg="#a7f37e", state="disabled")
                        active_text = f"\nITEM IN USE"
                        button_state = "disabled"   
                    else: 
                        buttons_list[counter].config(bg="SystemButtonFace")
                        
                        
                    description = self.game_data["items"][tab][item_names[counter]][1]
                    var_list[counter].set(f"{item_names[counter]}\n amount: {amount}\n description: {description}"+active_text)
                    
                else: # not in item dict (button will be empty)
                    
                    buttons_list[counter].config(state="disabled")
                    var_list[counter].set("none")


    

        
    def update_battle_interaction_menu(self): 
        

        hardness_range = (1, 12)
        self.text_var.set("Answer Question")

        answer_tuple = Math.generate_question(question_type= self.monster_data[self.monster_name], num_variables=self.player_data["level"]+1)
        #answer_tuple = Math.calcuate_answer( var_range = hardness_range, amount = self.player_data["level"]+1,function = self.monster_data[self.monster_name])      
        print(answer_tuple,"answer tuple")
        
        
        
        self.question_var.set(f"{answer_tuple[1]} = ?")
        buttons_randomized = [self.answer_button1, self.answer_button2, self.answer_button3, self.answer_button4]
        random.shuffle(buttons_randomized)
        wrong_answers = Math.create_wrong_answers(answer = answer_tuple[0])

        print(answer_tuple[0], "ANSWER")

        buttons_randomized[0].config(text= answer_tuple[0],  command=lambda: self.player_attack("correct"), state="normal")
        buttons_randomized[1].config(text= wrong_answers[0], command=lambda: self.player_attack("wrong"), state="normal")
        buttons_randomized[2].config(text= wrong_answers[1], command=lambda: self.player_attack("wrong"), state="normal")
        buttons_randomized[3].config(text= wrong_answers[2], command=lambda: self.player_attack("wrong"), state="normal")
    
    def timer(self): 
        pass
    

    def cutscreen(self): 
        
        self.canvas.create_polygon(0,0, 0, 600, 400, 600, fill= "black", width= 0)
        self.game_instance.after(250, lambda: self.canvas.create_polygon(0,600, 840, 600, 0, 300, fill= "black", width= 0))
        self.game_instance.after(500, lambda: self.canvas.create_polygon(400,600, 840, 0, 840, 600, fill= "black", width= 0))  
        self.game_instance.after(750, lambda: self.canvas.create_polygon(100,0, 840, 0, 840, 200, fill= "black", width= 0))     
        self.game_instance.after(1000, lambda: self.canvas.create_polygon(0,0, 300, 0, 0, 600, fill= "black", width= 0))
        self.game_instance.after(1250, lambda: self.canvas.create_rectangle(0, 0, 840, 600, fill="black", width= 0))

    
                
    def load_battle_canvas(self):        
        self.canvas.delete("all")
        self.canvas.configure(bg="green") 

        #player labels
        self.player_labelframe = LabelFrame(self.canvas)
        self.player_labelframe.place(relx=0.5, rely= 0.8, relwidth=0.5, relheight=0.2)

        
        self.player_health_var = StringVar()
        self.player_health_var.set(self.player_data["health"])

        Label(self.player_labelframe, text= "Player", font =("Arial",20, "bold")).place(relx=0.2, rely=0 , relwidth= 0.6, relheight=0.4)
        Label(self.player_labelframe, text="Health:", font =("Arial",18)).place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.2)
        self.player_health_label = Label(self.player_labelframe, textvariable=self.player_health_var, font =("Arial",18))
        self.player_health_label.place(relx= 0.5, rely=0.4, relwidth= 0.2, relheight=0.2)
        
        if int(self.player_health_var.get()) <=200: self.low_health(flashed= True)
        else:self.player_health_label.config(fg="black")
            
        
        
        self.player_shield_var = StringVar()
        self.player_shield_var.set(self.shield_health)        
        
        Label(self.player_labelframe, text="Shields:", font =("Arial",18)).place(relx=0.3, rely=0.7, relwidth=0.2, relheight=0.2)
        Label(self.player_labelframe, textvariable=self.player_shield_var, font =("Arial",18), fg= "blue").place(relx= 0.5, rely=0.7, relwidth= 0.2, relheight=0.2)
        
        
    
        #monster labels
        
        self.monster_labelframe = LabelFrame(self.canvas)
        self.monster_labelframe.place(relx=0, rely= 0, relwidth=0.5, relheight=0.2)

        self.monster_name_var = StringVar()
        self.monster_name_var.set(self.monster_name.title())

        self.monster_health_var = StringVar()
        self.monster_health_var.set(self.monster_health)
        

        Label(self.monster_labelframe, textvariable= self.monster_name_var ,font =("Arial",20, "bold")).place(relx=0.2, rely=0 , relwidth= 0.6, relheight=0.4)
        Label(self.monster_labelframe, text="Health:", font =("Arial",18)).place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.2)
        
        Label(self.monster_labelframe,textvariable= self.monster_health_var, font =("Arial",18)).place(relx= 0.5, rely=0.4, relwidth= 0.2, relheight=0.2)

        #images 
        self.bg = self.canvas.create_image(-260,0, anchor ='nw',image=self.battle_sprite_dict["battle bg.png"])
        self.player = self.canvas.create_image(60,200, anchor ='nw',image=self.battle_sprite_dict["character.png"])

        
        
        if f"{self.monster_name}.png" in self.battle_sprite_dict.keys(): 
            name = f"{self.monster_name}.png"
        else: 
                name = "placeholder.png"
      
            
        self.monster = self.canvas.create_image(480,0, anchor ='nw',image=self.battle_sprite_dict[name])
        
    def low_health(self, flashed = False ):
      
            if int(self.player_health_var.get()) <=200:
                
                
                self.player_health_label.config(fg="red" if flashed == False else "Black")
                
                
                new_flashed = True if flashed == False else False
                
                self.game_instance.after(500, lambda: self.low_health(flashed = new_flashed))
                
            else: 
                self.player_health_label.config(fg="black")
        
                
    def animate_change_exponential(self, var , current, target, duration): 
        if var is None:
            raise ValueError("string_var must be provided")

        diff = target - current
        steps = 100  # Number of steps in the animation
        decay_factor = 0.95  # Exponential decay factor
        delay = int(duration * 1000 / steps)  # Calculate delay in milliseconds based on total duration

        def update_value(step):
            nonlocal current
            if step < steps:
                current += diff * (decay_factor**step - decay_factor**(step + 1))
                if int(current) != last_displayed[0]:
                    last_displayed[0] = int(current)
                    var.set(last_displayed[0])
                self.game_instance.after(delay, update_value, step + 1)
            else:
                var.set(target)  # Ensure the final value is displayed correctly

        last_displayed = [current]
        update_value(0)
    

    def player_attack (self, mode:str):
        
        self.answer_button1.config(state= "disabled")
        self.answer_button2.config(state= "disabled")
        self.answer_button3.config(state= "disabled")
        self.answer_button4.config(state= "disabled")
        
        damage = random.randint(100, 130) 
        damage = int(damage *self.player_weapon_multiplyer)
        print(self.player_weapon_multiplyer)
        if mode == "correct":
            self.text_var.set("RIGHT!")
            self.monster_health -= damage
            
            
                
        elif mode == "wrong": 
            self.text_var.set("WRONG")
            damage = 0  
            
        def re(self): 
            self.animate_change_exponential(var = self.monster_health_var,current= int(self.monster_health_var.get()), target =  int(self.monster_health_var.get()) - damage, duration = 1.5)
            #self.monster_health_var.set(int(self.monster_health_var.get()) - damage)      
            self.action_response_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)
            self.action_response_frame.lift()
        
            self.action_response_text.set(f"player hit monster for {damage} damage")    
            
        

        
        self.player_attack_animation()
        self.game_instance.after(2000,lambda: re(self))
      
        self.game_instance.after(5000, lambda: self.monster_attack()    )
        self.game_instance.after(5000, lambda: self.monster_attack_animation())
        
    
    
    def monster_attack(self): 
        self.action_response_frame.lift()
        
        if self.monster_health <1:  #check if monster is dead yet 
            self.exit_menu()
            return
        
        damage_multiplyer = self.player_data["level"] *1.05
        
        base_damage = random.randint(90, 110)
        
        max_damage = base_damage * damage_multiplyer *self.monster_debuff
        
        damage = random.randint(base_damage, int(max_damage))
        
        if int(self.player_shield_var.get()) == 0:
            print('no shield')
            self.player_data["health"] -= damage
            self.animate_change_exponential(var = self.player_health_var,current= int(self.player_health_var.get()), target =  self.player_data["health"], duration = 1.5)
            #self.player_health_var.set(self.player_data["health"])
        else:
            self.shield_health -= damage
            if self.shield_health < 0: 
                self.shield_health = 0
                
            self.animate_change_exponential(var = self.player_shield_var,current= int(self.player_shield_var.get()), target =  self.shield_health, duration = 1.5)
        
        if int(self.player_health_var.get()) <=200: self.low_health(flashed= True)
        else:self.player_health_label.config(fg="black")
        
        self.reset_stat_vars()
        self.action_response_text.set(f"monster attack hit player for {damage} damage")
        
        #self.game_instance.after(3000, lambda: self.action_response_text.set(f"monster attack hit player for {damage} damage") )

        self.game_instance.after(4000, lambda:self.player_death() if self.player_data["health"] <1 else self.menu_selection_frame.lift())
                 
        


    
    def player_attack_animation(self): 
        
        pass 
    
    def monster_attack_animation(self):
        
        pass
    def exit_menu(self):
        clear_frame(self.frame)
        items = self.item_drops() 
        text =""
        for key, value in items.items():
            text += f"{key}: {value}\n"
        
        
        Button(self.frame, text = "exit", command= lambda:self.monster_death() ).pack()
        Label(self.frame, text = f"items dropped: {text}", font= ("Arial", 18)).pack()
        
        
    def item_drops(self):
        loot_table=self.game_data["loot table"]
        
        items = {"mini heal" : 2}
        tab_randomised = ["heals", "weapons", "shields", "potions"]
        random.shuffle(tab_randomised)
        rand_amount = random.randint(2,5)
        
        for index in range(0,rand_amount):
            current = 0
            tab = tab_randomised[random.randint(0,3)] 
            rand = random.randint(1,100)
            item_pool = loot_table.get(tab)
            for key, value in item_pool.items():
                if rand <= value: 
                    current = value
            
            if current in items.keys(): 
                items[key] +=1
            else:
                items[key] = 1
     
        
        
        for key, value in items.items(): 
            if key in self.player_data["items"].keys():
                self.player_data["items"][key] += value
            else: 
                self.player_data["items"][key] = value
             
        return items

        
    def monster_death (self):
        clear_frame(self.game_instance.menu_frame)
        self.player_labelframe.destroy()
        self.monster_labelframe.destroy()
        self.cutscreen()
        self.game_instance.after(1500, lambda: self.exit_battle())
        return
        
    def player_death (self): 
        
        clear_frame(self.game_instance)
        Label(self.game_instance, text="GAME OVER", font =("Arial",100)).place(rely=0, relwidth=1)
        #self.game_instance.after(4000, lambda: self.game_instance.destroy())
    
    
    def exit_battle(self): 
        self.player_data["score"] += 100
        self.game_instance.map_handler.delete_monster_cord(self.monster_cord, self.monster_name)
        self.game_instance.movement_allowed = True
        self.game_instance.load_main_menu()
        self.game_instance.auto_save(loop=False)
        self.game_instance.game_loop()


    def create_question (self): 
        pass
        

class Math: 

        
    def calcuate_answer( var_range : tuple, amount: int , function :str) -> tuple:
        
        yes={
            "-":operator.sub,
            "+":operator.add,
            "x":operator.mul,
            "/":operator.truediv
        }
        operators={
            "addition":"+",
            "subtraction":"-",
            "times":"x",
            "divide":"/"
        }
        answer = 0
        string = ""
        var_list = []
        ops=list(operators.keys())
        
        for x in range(amount): 
            print(x)
            var_list.append(random.randint(var_range[0], var_range[1])) 


        for x in range(amount): 
            if function == "algebra": 
                get = random.choice(["addition", "subtraction", "times"])
            elif function == "addition and subtraction":
                get = random.choice(["addition", "subtraction"])
            else:
                get = function
            
            
            op = operators.get(get) 

            string += f"{random.randint(var_range[0], var_range[1])} {op} "


        string = string[:-3]
        answer = eval((string.replace("x","*")).replace(" ",""))

        
        return (answer, string)
            
        
        
    def create_wrong_answers(answer: int) -> list:
        
        list = []
        counter = 3
        start = answer - 25
        end = answer +25
        while counter != 0:
            wrong_answer = random.randint(start,end)
            if wrong_answer != answer and wrong_answer not in list: 
                list.append(wrong_answer)
                counter -= 1
  
        return list
    
    def generate_question(question_type, num_variables=2):
        def generate_addition_question(num_variables):
            operands = [random.randint(1, 10) for _ in range(num_variables)]
            question = ' + '.join(map(str, operands))
            answer = sum(operands)
            return answer, question

        def generate_subtraction_question(num_variables):
            operands = [random.randint(1, 10) for _ in range(num_variables)]
            question = ' - '.join(map(str, operands))
            answer = reduce(operator.sub, operands)
            return answer, question

        def generate_multiplication_question(num_variables):
            operands = [random.randint(1, 10) for _ in range(num_variables)]
            question = ' * '.join(map(str, operands))
            answer = reduce(operator.mul, operands)
            return answer, question
        
            
        def generate_division_question(num_variables):
            operands = [random.randint(1, 10) for _ in range(num_variables)]
        
            div_num = reduce(operator.mul, operands)
            operands.reverse()
            
            operands.insert(0,div_num)
                
            question = ' / '.join(map(str, operands))
            
            question = question[:-4]
            answer = operands[-1]
            return answer, question
        def generate_mixed_algebra_question(num_variables):
            operators = {
                '+': operator.add,
                '-': operator.sub,
                '*': operator.mul,
                '/': operator.floordiv
            }

            operands = [random.randint(1, 10) for _ in range(num_variables)]
            op_symbols = [random.choice(list(operators.keys())) for _ in range(num_variables - 1)]

            question_parts = []
            for i in range(num_variables - 1):
                question_parts.append(str(operands[i]))
                question_parts.append(op_symbols[i])
            question_parts.append(str(operands[-1]))

            question = ' '.join(question_parts)

            answer = operands[0]
            for i in range(1, num_variables):
                op = operators[op_symbols[i - 1]]
                if op_symbols[i - 1] == '/' and answer % operands[i] != 0:
                    while answer % operands[i] != 0:
                        operands[i] = random.randint(1, 10)
                answer = op(answer, operands[i])

            return answer, question

        if question_type == 'addition':
            return generate_addition_question(num_variables)
        elif question_type == 'subtraction':
            return generate_subtraction_question(num_variables)
        elif question_type == 'multiplication':
            return generate_multiplication_question(num_variables)
        elif question_type == 'division':
        
            return generate_division_question(num_variables)
        elif question_type == 'algebra':
            return generate_mixed_algebra_question(num_variables)
        else:
            raise ValueError("Invalid question type. Choose from 'addition', 'subtraction', 'multiplication', 'division', 'algebra'.")

        
  

        
