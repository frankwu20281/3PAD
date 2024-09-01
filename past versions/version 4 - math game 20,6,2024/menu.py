
import time  
from tkinter import *

class Menu():
    def __init__(self,x ):    
        global game_instance 
        game_instance =x
        print('running menu')
        self.frame = game_instance.menu_frame
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

        self.button1 = Button(self.upper_row, text= "1",command=lambda: game_instance.battle_handler.check_user_input())
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

        game_instance.response_label = Label(self.question_frame, text="???", font =("Arial",15))
        game_instance.response_label.pack()
        


        """

        game_instance.math_question_text = "math question"
        game_instance.header = Label(self.frame, text="Battle Menu", font =("Arial",25))
        game_instance.header.pack()

        game_instance.math_question_label = Label(self.frame, text=game_instance.math_question_text, font =("Arial",15), fg= "green")
        game_instance.math_question_label.pack()

        Label(self.frame,text= "Entry").pack()
        
        game_instance.user_input_entry =  Entry(self.frame)
        game_instance.user_input_entry.pack()
        game_instance.user_input_entry.focus_set()

        game_instance.response_label = Label(self.frame, text="???", font =("Arial",15))
        game_instance.response_label.pack()

        Button(self.frame, command= lambda: game_instance.battle_handler.check_user_input(), text= 'submit answer').pack()
        game_instance.bind("<Return>",  lambda x: game_instance.battle_handler.check_user_input())

        """
        