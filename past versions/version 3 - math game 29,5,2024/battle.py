MAP_SIZE = 40 
WINDOW_SIZE = 600  
GRID_SIZE = 40
VIEWPORT_SIZE = WINDOW_SIZE // GRID_SIZE
import time  

class Battle():
    def __init__(self, game_instance):    
        print('running battle')
        game_instance.canvas.delete("all")
        game_instance.canvas.configure(bg="red")
        game_instance.canvas.create_rectangle(0,0,1 *GRID_SIZE,1*GRID_SIZE ,fill="grey" )
       