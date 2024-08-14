
from tkinter import *
import random  
MAP_SIZE = 40 
WINDOW_SIZE_HEIGHT = 600  
WINDOW_SIZE_WIDTH = 1200  
GRID_SIZE = 40
VIEWPORT_SIZE_HEIGHT = WINDOW_SIZE_HEIGHT // GRID_SIZE  
VIEWPORT_SIZE_WIDTH = WINDOW_SIZE_WIDTH // GRID_SIZE 

class Battle():
    def __init__(self, parent, monster_cord, sprite_dict):  
        
        self.game_instance = parent
        self.monster_cord = monster_cord
        self.canvas = parent.canvas

        self.battle_sprite_dict = sprite_dict["Battle"]


        
        self.cutscreen()

        self.game_instance.after(1500, lambda: self.load())
        
        
        self.monster_health = 3
    def load(self): 
        self.load_battle_canvas()
        test = 'eeee'
        self.canvas.create_text(100, 100, text="Question Menu", font =("Arial",30))

        test = 'kkkk'
        

        self.load_battle_menu()
    def cutscreen(self): 
        
        
        self.canvas.create_polygon(0,0, 0, 600, 400, 600, fill= "black", width= 0)
        self.game_instance.after(250, lambda: self.canvas.create_polygon(0,600, 840, 600, 0, 300, fill= "black", width= 0))
        self.game_instance.after(500, lambda: self.canvas.create_polygon(400,600, 840, 0, 840, 600, fill= "black", width= 0))  
        self.game_instance.after(750, lambda: self.canvas.create_polygon(100,0, 840, 0, 840, 200, fill= "black", width= 0))     
        self.game_instance.after(1000, lambda: self.canvas.create_polygon(0,0, 300, 0, 0, 600, fill= "black", width= 0))
        self.game_instance.after(1250, lambda: self.canvas.create_rectangle(0, 0, 840, 600, fill="black", width= 0))

        return

    def load_battle_canvas(self):
        self.canvas.delete("all")
        self.canvas.configure(bg="green") 
        self.canvas.create_image(0,300, anchor ='nw',image=self.battle_sprite_dict["tilted towers.png"])
        self.canvas.create_rectangle(10 * GRID_SIZE, 7 * GRID_SIZE, 10 * GRID_SIZE +80, 7 * GRID_SIZE+80,  fill="blue" , width=0)  

    def correct_answer (self): 
        self.button1.config(state= "disabled")
        self.button2.config(state= "disabled")
        self.button3.config(state= "disabled")
        self.button4.config(state= "disabled")
        self.question_label.config(text="right")

        self.monster_health -= 1 
        if self.monster_health != 0:
            self.game_instance.after(1000 , lambda: self.load_battle_menu())
        else:  
            self.cutscreen()
            self.game_instance.after(1500, lambda: self.exit_battle())
        


    def exit_battle(self): 
        self.game_instance.map_handler.delete_monster_cord(self.monster_cord)
        self.game_instance.movement_allowed = True
        self.clear_frame(self.game_instance.menu_frame)
        self.game_instance.load_main_menu()
        
        
        self.game_instance.game_loop()

    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def load_battle_menu (self):
        
        frame = self.game_instance.menu_frame
        self.clear_frame(frame)

        self.question_frame = Frame(frame, background="red", width= 100, height=100)
        self.question_frame.place(relx=0, rely= 0, relwidth=0.5, relheight=1)
        self.buttons_frame = Frame(frame,background="orange",width= 100, height=100)
        self.buttons_frame.place(relx=0.5, rely= 0, relwidth=0.5, relheight=1)


        Label(self.question_frame, text="Question Menu", font =("Arial",30)).place(relx=0.2, rely= 0, relwidth=0.6, relheight=0.2)

        

        self.button1 = Button(self.buttons_frame, text='wrong')
        self.button1.place(relx=0, rely=0 ,relwidth=0.5, relheight=0.5)

        self.button2 = Button(self.buttons_frame, text= "wrong")
        self.button2.place(relx=0.5, rely=0,relwidth=0.5, relheight=0.5)


        self.button3 = Button(self.buttons_frame, text= "wrong")
        self.button3.place(relx=0, rely=0.5,relwidth=0.5, relheight=0.5)


        self.button4 = Button(self.buttons_frame, text= "wrong")
        self.button4.place(relx=0.5, rely=0.5,relwidth=0.5, relheight=0.5)

        self.var1 , self.var2 = None, None
        self.question_label = Label(self.question_frame, text=f"{self.var1} + {self.var2} = ?", font =("Arial",15))
        self.question_label.place(relx=0.2, rely= 0.5, relwidth=0.6, relheight=0.2)


        self.button1.config(state= "normal")
        self.button2.config(state= "normal")
        self.button3.config(state= "normal")
        self.button4.config(state= "normal")

        self.update_menu()
        
       


        
    def create_addtion_question (self): 

        self.var1 = random.randint(1,10)
        self.var2 = random.randint(1,10)

        self.question_label.config(text=f"{self.var1} + {self.var2} = ?")
    
    def update_menu(self): 
        
        self.create_addtion_question()
        buttons_randomized = random.choice([self.button1, self.button2, self.button3, self.button4],)
        buttons_randomized.config(text= self.var1 + self.var2, command=lambda: self.correct_answer() )





        

    