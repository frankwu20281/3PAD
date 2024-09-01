
from tkinter import *
import random  
import json 
import operator
MAP_SIZE = 40 
WINDOW_SIZE_HEIGHT = 600  
WINDOW_SIZE_WIDTH = 1200  
GRID_SIZE = 40
VIEWPORT_SIZE_HEIGHT = WINDOW_SIZE_HEIGHT // GRID_SIZE  
VIEWPORT_SIZE_WIDTH = WINDOW_SIZE_WIDTH // GRID_SIZE 

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()
      
      
def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

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

        self.monster_health = 400
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
        def heal_player_health(self):
            self.player_data["health"] += 100
            self.player_health_var.set(self.player_data["health"])
            print('healed')
        
        self.battle_interaction_frame = Frame(self.frame, width= 100, height=100)
        self.battle_interaction_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)
        
        self.question_frame = Frame(self.battle_interaction_frame, background="red", width= 100, height=100)
        self.question_frame.place(relx=0, rely= 0, relwidth=0.5, relheight=1)
        
        Label(self.question_frame, text="Question Menu", font =("Arial",30)).place(relx=0.2, rely= 0, relwidth=0.6, relheight=0.2)

        self.question_var = StringVar()
        Label(self.question_frame,textvariable=self.question_var, font =("Arial",15)).place(relx=0.2, rely= 0.2, relwidth=0.6, relheight=0.2)
        self.text_var = StringVar()
        Label(self.question_frame,textvariable=self.text_var).place(relx=0.2, rely= 0.5, relwidth=0.6, relheight=0.2)
        
        self.change_menu_button = Button(self.question_frame, text= "Heal" , command= lambda: heal_player_health(self))
        self.change_menu_button.place(relx=0.2, rely= 0.8, relwidth=0.6, relheight=0.2)


        self.buttons_frame = Frame(self.battle_interaction_frame,background="orange",width= 100, height=100)
        self.buttons_frame.place(relx=0.5, rely= 0, relwidth=0.5, relheight=1)
        
        self.answer_button1 = Button(self.buttons_frame, text='wrong' )
        self.answer_button1.place(relx=0, rely=0 ,relwidth=0.5, relheight=0.5)
        self.answer_button2 = Button(self.buttons_frame, text= "wrong")
        self.answer_button2.place(relx=0.5, rely=0,relwidth=0.5, relheight=0.5)
        self.answer_button3 = Button(self.buttons_frame, text= "wrong")
        self.answer_button3.place(relx=0, rely=0.5,relwidth=0.5, relheight=0.5)
        self.answer_button4 = Button(self.buttons_frame, text= "wrong")
        self.answer_button4.place(relx=0.5, rely=0.5,relwidth=0.5, relheight=0.5)     
        

        self.answer_button1.config(state= "normal")
        self.answer_button2.config(state= "normal")
        self.answer_button3.config(state= "normal")
        self.answer_button4.config(state= "normal")
        
        
        """
        
        Inventory Frame 
        
        """
        def open_item_frame(self): 
            

         
            self.item_frame = Frame(self.frame,background="red",width= 100, height=100)
            self.item_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)
            self.item_frame.lift()
            tab_frame = Frame(self.item_frame)
            tab_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)
            
            
            Label(tab_frame, text= "Inventory").place(relx=0.1, rely=0, relwidth=0.4, relheight=0.2)
            Button(tab_frame,text="Back to Menu", command= lambda: self.menu_selection_frame.lift() ).place(relx=0.5, rely= 0, relwidth=0.4, relheight= 0.2)
            Button(tab_frame, text = "heals", command= lambda : self.update_item_buttons( tab="heals")).place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)
            Button(tab_frame, text = "weapons", command= lambda : self.update_item_buttons(tab="weapons")).place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.2)
            Button(tab_frame, text = "shields", command= lambda : self.update_item_buttons(tab="shields")).place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.2)
            Button(tab_frame, text = "potions", command= lambda : self.update_item_buttons( tab="potions")).place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.2)
            
            button_frame = Frame(self.item_frame,width= 100, height=100)
            button_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
            
            self.item1_var = StringVar()
            self.item1_var.set("Select an Inventory Tab")
            self.item_button1 = Button(button_frame, textvariable=self.item1_var, wraplength=80, state= "disabled")
            self.item_button1.place(relx=0.03, rely=0.1 ,relwidth= 0.19, relheight=0.8)
            self.item2_var = StringVar()
            self.item_button2 = Button(button_frame, textvariable= self.item2_var, wraplength=80, state= "disabled")
            self.item_button2.place(relx=0.28, rely=0.1 ,relwidth= 0.19, relheight=0.8)
            self.item3_var = StringVar()
            self.item_button3 = Button(button_frame, textvariable= self.item3_var, wraplength=80, state= "disabled")
            self.item_button3.place(relx=0.53, rely=0.1 ,relwidth= 0.19, relheight=0.8)
            self.item4_var = StringVar()
            self.item_button4 = Button(button_frame, textvariable=self.item4_var, wraplength=80, state= "disabled")
            self.item_button4.place(relx=0.78, rely=0.1 ,relwidth= 0.19, relheight=0.8)

        
        
        """
        
        Select menu Frame 
        
        """
        def answer_question(self): 
            self.battle_interaction_frame.lift()
            self.update_battle_interaction_menu()
            self.game_instance.after(1000, lambda: self.timer())
            
        def item_menu(self):
            self.menu_selection_frame.place_forget()
            self.item_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)
            self.item_frame.lift()
            
        self.menu_selection_frame = Frame(self.frame,background="purple",width= 100, height=100)
        self.menu_selection_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)
        self.menu_selection_frame.lift()
        
            
        Button(self.menu_selection_frame, text= "answer question",command= lambda: answer_question(self)).pack()
        Button(self.menu_selection_frame, text= "item menu",command= lambda: open_item_frame(self)).pack()

        
        '''

        Action response frame
    
        '''
        
        self.action_response_frame = Frame(self.frame, bg="red")
        self.action_response_text = StringVar()
        
        Label(self.action_response_frame, textvariable=self.action_response_text, font =("Arial",18)).pack()#place(relx=0.4, rely= 0, relwidth=0.5, relheight=0.2)
        
        #Button(self.action_response_frame, text= "Next", font =("Arial",12), command= lambda :open_menu_selection_frame(self)).pack()#place(relx=0, rely=1, relwidth=0.5, relheight=0.2)
        
    
    
    
    
    def item_button_function(self, text: str, tab: str):
        print(' button press, item name: ', text , "tab:", tab)
        name =text.split('\n', 1)[0]
        if tab == "heals":
            heal = self.game_data["items"]["heals"][name][0]
            self.player_data["health"] += heal
            self.player_health_var.set(self.player_data["health"])

        elif tab == "weapons": 
            self.weapon_active = True 
            self.weapon_active_name = name
            self.player_weapon_multiplyer = self.game_data["items"]["weapons"][name][0]
            
        elif tab == "shields":
            self.shield_active= True
            self.shield_active_name = name
            self.shield_health =  self.game_data["items"]["shields"][name][0]
        elif tab == "potions": 
            self.debuff_active = True 
            self.debuff_active_name = name 
            self.monster_debuff =  self.game_data["items"]["potions"][name][0]
        
        print(f"weapon multi: {self.player_weapon_multiplyer}\n shield: {self.shield_health}\n monster debuff {self.monster_debuff}")
        
        self.player_data["items"][name] -= 1      
        self.update_item_buttons(tab = tab)
        
      
        
                
    def update_item_buttons(self, tab:str):
            print('----------------------')
            item_names = list(self.game_data["items"][tab].keys())
            button_state = "active"
            var_list = [self.item1_var, self.item2_var, self.item3_var, self.item4_var]
            buttons_list = [self.item_button1, self.item_button2, self.item_button3, self.item_button4]
        
            active = {"weapons": [self.weapon_active, self.weapon_active_name], 
                      "shields": [self.shield_active, self.shield_active_name], 
                      "potions": [self.debuff_active, self.debuff_active_name], 
                      "heals": [None, None]}

            
            if  active.get(tab)[0] == True:
                pass
                
            
            self.item_button1.config( command = lambda: self.item_button_function(self.item1_var.get(), tab = tab),state = button_state, bg= "Green" if self.item1_var.get().split('\n', 1)[0] == active.get(tab)[1]  else "SystemButtonFace"  )         
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
    

    
    def timer(self): 
        pass 
        
    def update_battle_interaction_menu(self): 
        self.question_frame.place(relx=0, rely= 0, relwidth=0.5, relheight=1)
        self.buttons_frame.place(relx=0.5, rely= 0, relwidth=0.5, relheight=1)

        
       
        hardness_range = (1, 10)
        self.text_var.set("answer question")

        answer_tuple = Math.calcuate_answer( var_range = hardness_range, amount = 3 ,function = self.monster_data[self.monster_name])      
        print(answer_tuple,"answer tuple")
        
        
        
        self.question_var.set(f"{answer_tuple[1]} = ?")
        buttons_randomized = [self.answer_button1, self.answer_button2, self.answer_button3, self.answer_button4]
        random.shuffle(buttons_randomized)
        wrong_answers = Math.create_wrong_answers(answer = answer_tuple[0])
  

        buttons_randomized[0].config(text= answer_tuple[0],bg="green", command=lambda: self.player_attack("correct"), state="normal")
        buttons_randomized[1].config(text=wrong_answers[0], bg ="SystemButtonFace", command=lambda: self.player_attack("wrong"), state="normal")
        buttons_randomized[2].config(text= wrong_answers[1],bg ="SystemButtonFace",  command=lambda: self.player_attack("wrong"), state="normal")
        buttons_randomized[3].config(text= wrong_answers[2], bg ="SystemButtonFace", command=lambda: self.player_attack("wrong"), state="normal")
    
    
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
        

        Label(self.player_labelframe, text= "<- player", font =("Arial",30)).pack()
        Label(self.player_labelframe, textvariable=self.player_health_var, font =("Arial",30)).pack()
    
        #monster labels
        
        self.monster_labelframe = LabelFrame(self.canvas)
        self.monster_labelframe.place(relx=0, rely= 0, relwidth=0.5, relheight=0.2)

        self.monster_name_var = StringVar()
        self.monster_name_var.set(self.monster_name)

        self.monster_health_var = StringVar()
        self.monster_health_var.set(self.monster_health)
        

        Label(self.monster_labelframe, textvariable= self.monster_name_var ,font =("Arial",30) ).pack()
        Label(self.monster_labelframe,textvariable= self.monster_health_var, font =("Arial",30)).pack()

        #images 
        self.bg = self.canvas.create_image(-260,0, anchor ='nw',image=self.battle_sprite_dict["battle bg.png"])
        self.player = self.canvas.create_image(60,200, anchor ='nw',image=self.battle_sprite_dict["character.png"])
        self.monster = self.canvas.create_image(480,0, anchor ='nw',image=self.battle_sprite_dict["character.png"])
        
    
    

    def player_attack (self, mode:str):
        
        self.answer_button1.config(state= "disabled")
        self.answer_button2.config(state= "disabled")
        self.answer_button3.config(state= "disabled")
        self.answer_button4.config(state= "disabled")
        
        damage = 100 
        damage = int(damage *self.player_weapon_multiplyer)
        print(self.player_weapon_multiplyer)
        if mode == "correct":
            self.text_var.set("right")
            self.monster_health -= damage
            
            
            self.monster_health_var.set(int(self.monster_health_var.get()) - damage)            
            
                
        elif mode == "wrong": 
            self.text_var.set("wrong")
            
        self.action_response_frame.place(relx=0, rely= 0, relwidth=1, relheight=1)
        self.action_response_frame.lift()
        
        self.action_response_text.set(f"player hit monster for {damage} damage")    
        
        

        
        self.player_attack_animation()
        self.game_instance.after(2000, lambda: self.monster_attack()    )
        self.game_instance.after(2000, lambda: self.monster_attack_animation())
        
    
    
    def monster_attack(self): 
        
        self.question_frame.place_forget()
        self.buttons_frame.place_forget()
        
        if self.monster_health <1:  #check if monster is dead yet 
            self.monster_death()
            return
        
        
        damage_multiplyer = self.player_data["level"] *1.1
        
        base_damage = 100
        
        max_damage = base_damage * damage_multiplyer
        
        damage = random.randint(base_damage, int(max_damage))
        
  
        self.player_data["health"] -= damage
        self.player_health_var.set(self.player_data["health"])
        
        
        self.reset_stat_vars()
        self.action_response_text.set(f"monster attack hit player for {damage} damage")
        
        self.game_instance.after(1500, lambda: self.action_response_text.set(f"monster attack hit player for {damage} damage") )

        self.game_instance.after(3000, lambda:self.player_death() if self.player_data["health"] <1 else self.menu_selection_frame.lift())
                 
        


    
    def player_attack_animation(self): 
        
        pass 
    
    def monster_attack_animation(self):
        
        pass
    
    def monster_death (self):
        clear_frame(self.game_instance.menu_frame)
        self.player_labelframe.destroy()
        self.monster_labelframe.destroy()
        self.cutscreen()
        self.game_instance.after(1500, lambda: self.exit_battle())
        return
        
    def player_death (self): 
        
        clear_frame(self.game_instance)
        Label(self.game_instance, text="GAME OVER", font =("Arial",100)).place(rely=0.5)
        self.game_instance.after(4000, lambda: self.game_instance.destroy())
    
    
    def exit_battle(self): 
        self.game_instance.map_handler.delete_monster_cord(self.monster_cord, self.monster_name)
        self.game_instance.movement_allowed = True
        self.game_instance.load_main_menu()
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
            
            op = operators.get(function if function != "algebra" else random.choice(["addition", "subtraction", "times"])) 

            string += f"{random.randint(var_range[0], var_range[1])} {op} "


        string = string[:-3]
        answer = eval((string.replace("x","*")).replace(" ",""))
        
        
        
        return (answer, string)
            
        
        
    def create_wrong_answers(answer: int) -> list:
        print("createing wrong answers")
        list = []
        counter = 3
        start = answer - 50
        end = answer +50
        while counter != 0:
            wrong_answer = random.randint(start,end)
            print('in loop')
            if wrong_answer != answer and wrong_answer not in list: 
                list.append(wrong_answer)
                counter -= 1
                print('added to list')
        print("done")
        return list
     
   

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


        
    """CreateToolTip(self.answer_button2, text = 'Hello World\n'
                 'This is how tip looks like.'
                 'Best part is, it\'s not a menu.\n'
                 'Purely tipbox.')
    """
    