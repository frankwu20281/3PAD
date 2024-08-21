
import time  
from tkinter import *
import random   

class Menu():
    def __init__(self,x ):    
        global game_instance 
        game_instance =x
        print('running menu')
        self.frame = game_instance.menu_frame
        self.math_instance = Math(game_instance)
        self.load_main_menu()
    
    def clear_frame(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()


    def load_main_menu (self):
        self.clear_frame()
        game_instance.unbind("<Enter>")
        Label(self.frame, text="Main Menu", font =("Arial",25)).pack(padx=50)


    def load_battle_menu (self):
        self.clear_frame()

        

        
        self.question_frame = Frame(self.frame)
        self.question_frame.pack(side=LEFT, fill="both")

        self.buttons_frame = Frame(self.frame,background="blue")
        self.buttons_frame.pack(fill="both",expand=True) 
        self.upper_row = Frame(self.buttons_frame)
        self.upper_row.pack(side=TOP, expand=True, fill="both")
        
        self.lower_row = Frame(self.buttons_frame)
        self.lower_row.pack(side=BOTTOM, expand=True, fill="both")


        
        Label(self.question_frame, text="Main Menu", font =("Arial",40)).pack(padx=50)

        self.button1 = Button(self.upper_row, text='1')
        self.button1.pack(side=LEFT, expand=True, fill="both")

        self.button2 = Button(self.upper_row, text= "2")
        self.button2.pack(side=LEFT, expand=True, fill="both")


        self.button3 = Button(self.lower_row, text= "3")
        self.button3.pack(side=LEFT, expand=True, fill="both")


        self.button4 = Button(self.lower_row, text= "4")
        self.button4.pack(side=LEFT, expand=True, fill="both")
        game_instance.math_question_label = Label(self.question_frame, text="", font =("Arial",15), fg= "green")
        game_instance.math_question_label.pack()

        Label(self.question_frame,text= "Entry").pack()
        self.var1 , self.var2 = self.math_instance.create_question()
        game_instance.response_label = Label(self.question_frame, text="???", font =("Arial",15))
        game_instance.response_label.pack()
        self.configure_buttons()

        
    def configure_buttons(self): 
        

        buttons_randomized = random.choices([self.button1, self.button2, self.button3, self.button4], k=4)
        buttons_randomized[0].config(text= self.var1 + self.var2, command=lambda: game_instance.battle_handler.correct_answer() )

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



        

    



