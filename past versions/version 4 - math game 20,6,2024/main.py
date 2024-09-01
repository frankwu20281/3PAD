from  tkinter import *
from tkinter.ttk import *
import threading, time, json

#from player import *  
from battle import *        
#from map import *       
#from monster import *   
from menu import *   
import os 

#os.system('xset r off')

startTime = time.time()

MAP_SIZE = 40 
WINDOW_SIZE_HEIGHT = 600  
WINDOW_SIZE_WIDTH = 840  
GRID_SIZE = 40
VIEWPORT_SIZE_HEIGHT = WINDOW_SIZE_HEIGHT // GRID_SIZE  # 15
VIEWPORT_SIZE_WIDTH = WINDOW_SIZE_WIDTH // GRID_SIZE # 21

        
    


class Game(Tk):
    def __init__(self):
        
        super().__init__()
       
        
        with open("map_data.json") as file: 
            self.map_storage =  json.load(file)
        with open("monster_path_data.json") as file: 
            self.monster_path_storage = json.load(file)

        

        self.level_number = 1
        self.player_pos = [] 
        self.movement_allowed = True
        self.key_change = False
        self.player_direction = "none"
        
        self.terrain_map= self.map_storage[str(self.level_number)]
        self.monster_path_map= self.monster_path_storage[str(self.level_number)]

        
       
        #setting up game screen, canvas
        self.geometry(f"1000x800")
        self.resizable(False, False)      
        self.canvas = Canvas(self, width=WINDOW_SIZE_WIDTH, height=WINDOW_SIZE_HEIGHT, bg="orange")
        self.canvas.pack()
        self.menu_frame = Frame(self, bg= "blue")
        self.menu_frame.pack(expand=TRUE, fill=BOTH)


        # load sprites
        self.character_sprite = PhotoImage(file="sprites\Textures\character.png")
        self.wall_sprite = PhotoImage(file="sprites\Textures\wall.png")
        self.grass_full_sprite = PhotoImage(file="sprites\Textures\grass.png")
        '''
        self.tilted_towers = PhotoImage(file="sprites\Textures\Tilted_Towers.png")
        self.monster_image = PhotoImage(file="sprites\Textures\o.png")
        self.plane_sprite = PhotoImage(file="sprites\Textures\plane.png")
        '''

        # loading in all the different file classes
        self.menu_handler = Menu(self)
        self.monster_handler = Monster(self)
        self.player_handler = Player(self)

        self.battle_handler = Battle(self)

        self.map_handler = Map(self)
        
        


        # binds arrow keys for moVEMENT        
        self.bind("<KeyPress>", lambda x : self.key_press(x) )
        #self.bind("<KeyRelease>", lambda x : self.player_stop_movement(x))
          
        self.bind('<Map>', lambda x: self.monster_loop())
     
        self.bind("<KeyRelease>", lambda x : self.key_release(x))#lambda x : self.player_movement(x,"KeyRelease")

        self.movement_loop()
        self.new_frame()
        self.mainloop()

        #self.fake_ass_menu=Menu(self) opens new window 
        #terrain_handler.terrain_load("level 1",self)

    def key_press (self, event): 
       
        self.player_direction = event
        
    


    def key_release (self,event):
        print("keyrealease")
        self.key_change = False
        self.player_direction = "none"


    def movement_loop(self):
        
        
        if self.player_direction != "none":

            result = self.player_handler.key_press(self.player_direction)
            self.movement_allowed = True
            
            if result[0] == True:
                self.player_pos = result[1]
                
            elif result[0] == "monster":
                print("battle time")
                self.menu_handler.load_battle_menu()
                self.battle_handler.battle_screen(result[1]) 
                self.movement_allowed = False
                pass
                print('passed pass')
                
            elif result[0] == "teleport": 
                self.map_handler.next_level()
                self.monster_handler.monster_path_load()
                self.new_frame()
                return
            elif result[0] == "collision":
                pass 
            #hit wall so no movement 
            
            self.movement_allowed = True
            
            
        if self.movement_allowed:
            print('updated frame')
            self.new_frame()
            self.after(10, lambda : self.movement_loop())
       



    def monster_loop(self):
        
        if self.movement_allowed == True:
            result= self.monster_handler.move_monster_cords()
            if type(result) == tuple:
                print("battle time")
                self.menu_handler.load_battle_menu()
                self.battle_handler.battle_screen(result) 
            
                self.movement_allowed = False
                
            else:

                self.new_frame()
                self.after(1000, lambda: self.monster_loop())
       
        self.unbind('<Map>')

    def new_frame(self):
        
        self.canvas.delete("all")
        self.canvas.configure(bg="green")
        
        
        #update player pos
    
        
        #update all terrain pos
        top_left_x = self.player_pos[0] - 10*GRID_SIZE # pos -10
        
        top_left_y = self.player_pos[1] - 7*GRID_SIZE  #pos - 7

        remainder_x = top_left_x % GRID_SIZE
       
        remainder_y = top_left_y % GRID_SIZE
        for key, list in self.terrain_cords_dict.items():
            for x in range(VIEWPORT_SIZE_WIDTH):
                for y in range(VIEWPORT_SIZE_HEIGHT):
                    map_x = top_left_x + x*GRID_SIZE
                    map_y = top_left_y + y*GRID_SIZE
                    if (map_x//GRID_SIZE, map_y//GRID_SIZE) in list:
                        if key == "grass full":
                            self.canvas.create_rectangle(x*GRID_SIZE - remainder_x, y*GRID_SIZE -remainder_y, 
                                                    (x*GRID_SIZE + GRID_SIZE) - remainder_x, (y*GRID_SIZE + GRID_SIZE) - remainder_y, 
                                                    fill="yellow" , width=0)
                            
                        if key == "wall":
                            """
                            self.canvas.create_rectangle(x*GRID_SIZE - remainder_x, y*GRID_SIZE -remainder_y, 
                                                    (x*GRID_SIZE + GRID_SIZE) - remainder_x, (y*GRID_SIZE + GRID_SIZE) - remainder_y, 
                                                    fill="grey" )
                                                """
                            self.canvas.create_image(x*GRID_SIZE - remainder_x, y*GRID_SIZE -remainder_y, 
                                anchor='nw', image=self.wall_sprite)
                        
                        if key == "border": 
                            self.canvas.create_rectangle(x*GRID_SIZE - remainder_x, y*GRID_SIZE -remainder_y, 
                                                    (x*GRID_SIZE + GRID_SIZE) - remainder_x, (y*GRID_SIZE + GRID_SIZE) - remainder_y, 
                                                    fill="black" )
                        if key == "teleport": 
                            self.canvas.create_rectangle(x*GRID_SIZE - remainder_x, y*GRID_SIZE -remainder_y, 
                                                    (x*GRID_SIZE + GRID_SIZE) - remainder_x, (y*GRID_SIZE + GRID_SIZE) - remainder_y, 
                                                    fill="blue" )
                        if key == "monster":  
                            self.canvas.create_rectangle(x*GRID_SIZE - remainder_x, y*GRID_SIZE -remainder_y, 
                                                    (x*GRID_SIZE + GRID_SIZE) - remainder_x, (y*GRID_SIZE + GRID_SIZE) - remainder_y, 
                                                    fill="red" ) 
                            self.canvas.create_image(x*GRID_SIZE - remainder_x, y*GRID_SIZE -remainder_y,  
                                 anchor='nw', image=self.character_sprite)
                        
        self.canvas.create_image(10 * GRID_SIZE, 7 * GRID_SIZE, 
                                 anchor=NW, image=self.character_sprite)
        


        
class Player(): 
    def __init__(self, x) -> None:
        global game_instance
        
        game_instance = x 
       
        pass
        
    def key_press( self, event):
        pixel_dist = 4
        direction = {
            "Up": (0, -pixel_dist),
            "Down": (0, pixel_dist),
            "Left": (-pixel_dist, 0),
            "Right": (pixel_dist, 0)
        }.get(event.keysym)    
                
        if direction: 
           
            new_x = game_instance.player_pos[0] + direction[0]
            new_y = game_instance.player_pos[1] + direction[1]

            collision = self.wall_collision_check(new_x,new_y)
            
            return collision
       
 
    def wall_collision_check (self, new_x, new_y):
        
        player_grid_cord_x = new_x // GRID_SIZE
        player_grid_cord_y = new_y //GRID_SIZE  
        
        screen_midpoint_x = 10*GRID_SIZE
        screen_midpoint_y = 7*GRID_SIZE
        
        player_point_top_left = (screen_midpoint_x , WINDOW_SIZE_WIDTH-screen_midpoint_y)
        player_point_bottom_right = ( (screen_midpoint_x+GRID_SIZE), WINDOW_SIZE_WIDTH -(screen_midpoint_y+GRID_SIZE))

        remainder_x = new_x % GRID_SIZE
        remainder_y = new_y % GRID_SIZE
       
        
    
        for key, list in game_instance.terrain_cords_dict.items():
            for value in list: 
            
                obj_grid_x_cord = value[0]
                obj_grid_y_cord = value[1]
                
                if obj_grid_x_cord in range(player_grid_cord_x - (0 if key !="monster" else 1),player_grid_cord_x +(2 if key != "monster" else 3)) and obj_grid_y_cord in range(player_grid_cord_y -(0 if key!= "monster"else 1), player_grid_cord_y+(2 if key!= "monster"else 3)):
                    
                    
                    obj_x_offset_pos =  obj_grid_x_cord - player_grid_cord_x
                    obj_y_offset_pos =  obj_grid_y_cord - player_grid_cord_y
                    
                    
                    obj_x_pos = (screen_midpoint_x + obj_x_offset_pos*GRID_SIZE) -remainder_x
                    obj_y_pos = (screen_midpoint_y +obj_y_offset_pos*GRID_SIZE) -remainder_y
                    
                    
                    
                    obj_point_top_left = (obj_x_pos, WINDOW_SIZE_WIDTH-obj_y_pos)
                    obj_point_bottom_right = ((obj_x_pos+GRID_SIZE), (WINDOW_SIZE_WIDTH-obj_y_pos)+GRID_SIZE)
                
                    if ((player_point_bottom_right[1] > obj_point_top_left[1] or obj_point_bottom_right[1]> player_point_top_left[1] ) and remainder_x != 0 ) or ((player_grid_cord_x == obj_grid_x_cord) and player_point_bottom_right[1]< obj_point_top_left[1]) :
                        if key == "wall" or key == "border":return ("collision" , )
                        elif key == "teleport": return ("teleport", )
                        elif key == "monster": return "monster", (obj_grid_x_cord, obj_grid_y_cord)      

        return (True, (new_x, new_y))
                
    
        

class Monster(): 
    
    def __init__(self, x) :
        
        global game_instance
        
        game_instance = x
        
        pass
         
        
    def monster_path_load(self):
        y_cord = 0
        for x_line in game_instance.monster_path_storage[str(game_instance.level_number)]:
            x_cord = 0 
            for obj in x_line: 
                if obj == "D": 
                    game_instance.monster_movement_cords_dict["down"].append((x_cord,y_cord))
                elif obj == "U": 
                    game_instance.monster_movement_cords_dict["up"].append((x_cord,y_cord))
                elif obj == "L": 
                    game_instance.monster_movement_cords_dict["left"].append((x_cord,y_cord))
                elif obj == "R": 
                    game_instance.monster_movement_cords_dict["right"].append((x_cord,y_cord))
                x_cord += 1
            y_cord += 1
        
        print(game_instance.monster_movement_cords_dict)
        print("new monster path loaded in ")

    def delete_monster_cord(self, monster_cord):
        for cord in game_instance.monster: 
            if monster_cord == cord: 
                game_instance.monster.remove(monster_cord)
                return


    def move_monster_cords(self): 

        for monster_cord in game_instance.monster:
           
            direction = {"down": (monster_cord[0],monster_cord[1]+1),
                         "up": (monster_cord[0],monster_cord[1]-1),
                         "left": (monster_cord[0]-1,monster_cord[1]),
                         "right": (monster_cord[0]+1,monster_cord[1])}
            
            for key, list in game_instance.monster_movement_cords_dict.items():   
                
                if monster_cord in list:
                
                        
                    new_monster_cord = direction[key]
                    colision_check = self.collison_check(new_monster_cord)
                    if colision_check == True: 
                        print('start battle')
                        return tuple(monster_cord)
                    elif colision_check == False:
                        print('monster moved')
                        game_instance.monster.remove(monster_cord)
                        game_instance.monster.insert(0,new_monster_cord)
                        
     
    
    def collison_check(self, new_monster_cord): 
 
        player_grid_cord_x = game_instance.player_pos[0] // GRID_SIZE
        player_grid_cord_y = game_instance.player_pos[1] //GRID_SIZE  
        print(player_grid_cord_x,player_grid_cord_y)
        print(new_monster_cord)
        player_grid_pos = (player_grid_cord_x,player_grid_cord_y)
        if new_monster_cord == player_grid_pos: 
            print('2222')
            return True        
        
        print("range x and y ", range(new_monster_cord[0]-1, new_monster_cord[0] +3),range(new_monster_cord[1]-1, new_monster_cord[1]-3))
                
        if player_grid_cord_x in range(new_monster_cord[0]-1, new_monster_cord[0] +3) and player_grid_cord_y in range(new_monster_cord[1]-1, new_monster_cord[1]+3):
        #if (new_monster_cord[0] + i, new_monster_cord[1]+j) == (player_grid_cord_x,player_grid_cord_x):
        #if (game_instance.player_pos[0] + i ,game_instance.player_pos[1]+j) == (new_x,new_y):
            
            print("battle time monster collision")
            return True
     
        return False
    
        '''if (new_x,new_y) in list: 

                    print('hit something ')
                    return "error"'''
                
    
                            
class Map():
    def __init__(self, x):
        global game_instance
        game_instance = x
        
        game_instance.player_pos = []
        self.reset_cord_storage()
        self.spawn_location()
        self.terrain_load()
        game_instance.monster_handler.monster_path_load()

    
    def next_level (self): 
        game_instance.level_number= 2
        game_instance.player_pos = []
        self.reset_cord_storage()
        self.spawn_location()
        self.terrain_load()
        game_instance.movement_loop()
        
    
    def reset_cord_storage (self):
        game_instance.monster = []
        game_instance.wall = []
        game_instance.map_border=[]
        game_instance.teleport = []
        game_instance.grass_full = []
        game_instance.terrain_cords_dict = {"wall":game_instance.wall, 
                                   "border":game_instance.map_border,
                                   "teleport":game_instance.teleport,
                                   "grass full":game_instance.grass_full, 
                                   "monster": game_instance.monster}
        
        
        game_instance.monster_down= []
        game_instance.monster_up= []
        game_instance.monster_left= []
        game_instance.monster_right= []
        game_instance.monster_movement_cords_dict = {"down": game_instance.monster_down, 
                                            "up":game_instance.monster_up,
                                            "left": game_instance.monster_left, 
                                            "right":game_instance.monster_right}


    def spawn_location (self):
        game_instance.terrain_map= game_instance.map_storage[str(game_instance.level_number)]
        y_cord = 0
        for x_line in game_instance.terrain_map:
            x_cord = 0
            for obj in x_line:
                if obj == "x": 
                    game_instance.player_pos = [x_cord*GRID_SIZE,y_cord*GRID_SIZE]
                    game_instance.grass_full.append((x_cord*GRID_SIZE,y_cord*GRID_SIZE))
                    print("spawn pos found")
                    
                    return
                x_cord+=1
            y_cord+=1
        if not game_instance.player_pos:
            game_instance.player_pos = [MAP_SIZE // 2, MAP_SIZE // 2]
            print('error loadinng in spawn pos')


    def terrain_load(self):
        y_cord = 0
    
        for x_line in game_instance.map_storage[str(game_instance.level_number)]:
           
            x_cord = 0
            for obj in x_line:
                if (x_cord,y_cord) != tuple(game_instance.player_pos):
                    
                    if obj == "." or obj == "M":
                        game_instance.grass_full.append((x_cord,y_cord))
                        
                    if obj == "w": 
                        game_instance.wall.append((x_cord,y_cord))
                    if obj == "=":
                        game_instance.map_border.append((x_cord,y_cord))
                    if obj == "T": 
                        game_instance.teleport.append((x_cord,y_cord))
                    if obj == "M":
                        print('mosnter added')
                        game_instance.monster.append((x_cord,y_cord))
                    
                x_cord+=1
                
            y_cord+=1
        
        
        print('terrain loaded in')




class Cutscreens ():
    def __init__(self) -> None:
        pass



class fake_ass_menu(Tk):
    def __init__(self, game_instance):
        super().__init__()
        

        self.geometry('200x200')
        self.configure(background = "blue")

Game()
            
        