
import time  
from tkinter import *

class Menu():
    def __init__(self,x ):    
        global game_instance 
        game_instance =x
        print('running menu')
        
        self.load_main_menu()
    
    def clear_frame(self):
        for widgets in game_instance.menu_frame.winfo_children():
            widgets.destroy()


    def load_main_menu (self):
        self.clear_frame()
        game_instance.unbind("<Enter>")
        Label(game_instance.menu_frame, text="Main Menu", font =("Arial",25)).pack(padx=50)


    def load_battle_menu (self):
        self.clear_frame()

        game_instance.math_question_text = "math question"
        game_instance.header = Label(game_instance.menu_frame, text="Battle Menu", font =("Arial",25))
        game_instance.header.pack()

        game_instance.math_question_label = Label(game_instance.menu_frame, text=game_instance.math_question_text, font =("Arial",15), fg= "green")
        game_instance.math_question_label.pack()

        Label(game_instance.menu_frame,text= "Entry").pack()
        
        game_instance.user_input_entry =  Entry(game_instance.menu_frame)
        game_instance.user_input_entry.pack()
        game_instance.user_input_entry.focus_set()

        game_instance.response_label = Label(game_instance.menu_frame, text="???", font =("Arial",15))
        game_instance.response_label.pack()

        Button(game_instance.menu_frame, command= lambda: game_instance.battle_handler.check_user_input(), text= 'submit answer').pack()
        game_instance.bind("<Return>",  lambda x: game_instance.battle_handler.check_user_input())

                 
        
