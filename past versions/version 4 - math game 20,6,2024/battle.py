
from tkinter import *
import random  
MAP_SIZE = 40 
WINDOW_SIZE_HEIGHT = 600  
WINDOW_SIZE_WIDTH = 1200  
GRID_SIZE = 40
VIEWPORT_SIZE_HEIGHT = WINDOW_SIZE_HEIGHT // GRID_SIZE  
VIEWPORT_SIZE_WIDTH = WINDOW_SIZE_WIDTH // GRID_SIZE 

class Battle():
    def __init__(self, x):    
        global game_instance 
        game_instance =x
        

      

        self.math_instance = Math(game_instance)

    def battle_screen(self, a): 
        global monster_cord
        monster_cord = a 
        game_instance.movement_allowed = False
        
        print('running battle')
        game_instance.canvas.delete("all")
        game_instance.canvas.configure(bg="red")
        game_instance.unbind("<KeyPress>")
        game_instance.unbind("<Map>")

        
        
       # game_instance.canvas.create_image(100, 100, anchor ='nw',
            #                 image=game_instance.plane_sprite)
        
       # game_instance.canvas.create_image(500, 100, anchor ='nw',
                    #         image=game_instance.tilted_towers)
        

        self.var1 , self.var2 = self.math_instance.create_question()
        
        
        #game_instance.canvas.create_image(0, 0,anchor='nw', image=monster_image)

    def check_user_input (self): 

        game_instance.response_label.config(text="right",fg="green")

        game_instance.after(1000 , lambda: self.exit_battle())
        


    def exit_battle(self): 
        game_instance.monster_handler.delete_monster_cord(monster_cord)
        game_instance.bind("<KeyPress>", lambda x : game_instance.key_press(x) )
        game_instance.movement_allowed = True
        game_instance.menu_handler.load_main_menu()
        
        
        #game_instance.bind('<Map>', lambda x : game_instance.monster_loop())
        game_instance.movement_loop()

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



        

    