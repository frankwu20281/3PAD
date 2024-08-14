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
        self.character_sprite = PhotoImage(file="sprites\character.png")
        self.wall_sprite = PhotoImage(file="sprites\wall.png")
        self.grass_full_sprite = PhotoImage(file="sprites\grass_full.png")
        self.tilted_towers = PhotoImage(file="sprites\Tilted_Towers.png")
        self.monster_image = PhotoImage(file="sprites\o.png")
        self.plane_sprite = PhotoImage(file="sprites\plane.png")


        # loading in all the different file classes
        self.menu_handler = Menu(self)
        self.monster_handler = Monster(self)
        self.player_handler = Player(self)

        self.battle_handler = Battle(self)

        self.map_handler = Map(self)
        
        

        #self.load_terrain_map()
        # binds arrow keys for moVEMENT        
        self.bind("<KeyPress>", lambda x : self.key_press(x) )
        #self.bind("<KeyRelease>", lambda x : self.player_stop_movement(x))
          
        #self.bind('<Map>', lambda x: self.monster_loop())
     
        self.bind("<KeyRelease>", lambda x : self.key_release(x))#lambda x : self.player_movement(x,"KeyRelease")

        self.move_player()
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


    def move_player(self):

        
        if self.player_direction != "none":

            result = self.player_handler.key_press(self.player_direction)
            self.movement_allowed = True
            
            if type(result)== list:
                self.player_pos = result
                
            elif type(result) == tuple:
                print("battle time")
                self.menu_handler.load_battle_menu()
                self.battle_handler.battle_screen(result) 
                self.movement_allowed = False
                return
                
            elif result == "teleport": 
                self.map_handler.next_level()
                self.monster_handler.monster_path_load()
                self.new_frame()
                return
                
                 
            
            self.movement_allowed = True
            self.new_frame()
        if self.movement_allowed:
            self.after(10, lambda : self.move_player())




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
    
        self.canvas.create_image(10 * GRID_SIZE, 7 * GRID_SIZE, 
                                 anchor=NW, image=self.character_sprite)
        self.canvas.create_rectangle(10 * GRID_SIZE, 7 * GRID_SIZE, 11 * GRID_SIZE, 8 * GRID_SIZE, 
                                 fill="red")
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
                        #if key == "grass full":
                            #self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, 
                            #                        (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, 
                            #                        fill="green" , width=0)
                            
                        if key == "walls":
                            
                            self.canvas.create_rectangle(x*GRID_SIZE - remainder_x, y*GRID_SIZE -remainder_y, 
                                                    (x*GRID_SIZE + GRID_SIZE) - remainder_x, (y*GRID_SIZE + GRID_SIZE) - remainder_y, 
                                                    fill="grey" )
                            #self.canvas.create_image(x * GRID_SIZE, y * GRID_SIZE, 
                                # anchor='nw', image=self.wall_sprite)
                        
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
                        
                            


        
class Player(): 
    def __init__(self, x) -> None:
        global game_instance
        
        game_instance = x 
        self.hug_horz_wall = False
        self.hug_vert_wall = False
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

            collision = self.wall_collision_check(new_x,new_y, event.keysym)
            
            if collision == False:
               
                return [new_x, new_y]
            
            else: 
                return collision
        else:
            return False
 
    def wall_collision_check (self, new_x, new_y, direction):
        
        grid_cord_x = new_x // GRID_SIZE
        grid_cord_y = new_y //GRID_SIZE  
        
        screen_midpoint_x = 10*GRID_SIZE
        screen_midpoint_y = 7*GRID_SIZE
        
        player_point_top_left = (screen_midpoint_x, WINDOW_SIZE_WIDTH-screen_midpoint_y)
        player_point_bottom_right = ( (screen_midpoint_x+GRID_SIZE), WINDOW_SIZE_WIDTH -(screen_midpoint_y+GRID_SIZE))

        remainder_x = new_x % GRID_SIZE
       
        remainder_y = new_y % GRID_SIZE
        print("000000000000000000000000000")
        print('newx newy', new_x, new_y)
        print("player grid x y", grid_cord_x, grid_cord_y)
        print('remainder x and y', remainder_x, remainder_y)
        
    
        for key, list in game_instance.terrain_cords_dict.items():
            if key == "walls": #!= "teleport" and key != "grass full":
                for value in list: 
              
                    wall_grid_x_cord = value[0]
                    wall_grid_y_cord = value[1]
                    
                    
                    if wall_grid_x_cord in range(grid_cord_x,grid_cord_x +2) and wall_grid_y_cord in range(grid_cord_y, grid_cord_y+2):
                        print('____________________')
                        print('wall x and y grid', wall_grid_x_cord, wall_grid_y_cord)
                        print("grid cordx and gridcordy", grid_cord_x,grid_cord_y)
                        
                        wall_x_offset_pos =  wall_grid_x_cord - grid_cord_x
                        wall_y_offset_pos =  wall_grid_y_cord - grid_cord_y
                        print('xoffset yoffset', wall_x_offset_pos,wall_y_offset_pos)
                        
                        wall_x_pos = (screen_midpoint_x + wall_x_offset_pos*GRID_SIZE) -remainder_x
                        wall_y_pos = (screen_midpoint_y +wall_y_offset_pos*GRID_SIZE) -remainder_y
                        print('wall x and y pos', wall_x_pos, wall_y_pos)
                        print('player x and y ', screen_midpoint_x,screen_midpoint_y)
                        
                        
                        print('\nplayer top left', player_point_top_left)
                        print('player bottom right', player_point_bottom_right)
                        
                        wall_point_top_left = (wall_x_pos, WINDOW_SIZE_WIDTH-wall_y_pos)
                        wall_point_bottom_right = ((wall_x_pos+GRID_SIZE), (WINDOW_SIZE_WIDTH-wall_y_pos)+GRID_SIZE)
                        print('wall top9 left' , wall_point_top_left)
                        print('wall bottom right', wall_point_bottom_right)
                        
                        if player_point_top_left[0] > wall_point_bottom_right[0] or wall_point_top_left[0] > player_point_bottom_right[0]:
                            print('hit 1')
                            return True
                        if ((player_point_bottom_right[1] > wall_point_top_left[1] or wall_point_bottom_right[1]> player_point_top_left[1] ) and remainder_x != 0 ) :
                        

                            print('hit 2')
                            return True
                            
                        elif (grid_cord_x == wall_grid_x_cord) and player_point_bottom_right[1]< wall_point_top_left[1] :
                            print('hit 3')
                            return True
                        
            if key == "teleport":
                for value in list: 
                
                    wall_grid_x_cord = value[0]
                    wall_grid_y_cord = value[1]
                
                
                    if wall_grid_x_cord in range(grid_cord_x,grid_cord_x +2) and wall_grid_y_cord in range(grid_cord_y, grid_cord_y+2):                
                        print('____________________')
                        print('wall x and y grid', wall_grid_x_cord, wall_grid_y_cord)
                        print("grid cordx and gridcordy", grid_cord_x,grid_cord_y)
                        
                        wall_x_offset_pos =  wall_grid_x_cord - grid_cord_x
                        wall_y_offset_pos =  wall_grid_y_cord - grid_cord_y
                        print('xoffset yoffset', wall_x_offset_pos,wall_y_offset_pos)
                        
                        wall_x_pos = (screen_midpoint_x + wall_x_offset_pos*GRID_SIZE) -remainder_x
                        wall_y_pos = (screen_midpoint_y +wall_y_offset_pos*GRID_SIZE) -remainder_y
                        print('wall x and y pos', wall_x_pos, wall_y_pos)
                        print('player x and y ', screen_midpoint_x,screen_midpoint_y)
                        
                        
                        print('\nplayer top left', player_point_top_left)
                        print('player bottom right', player_point_bottom_right)
                        
                        wall_point_top_left = (wall_x_pos, WINDOW_SIZE_WIDTH-wall_y_pos)
                        wall_point_bottom_right = ((wall_x_pos+GRID_SIZE), (WINDOW_SIZE_WIDTH-wall_y_pos)+GRID_SIZE)
                        print('wall top9 left' , wall_point_top_left)
                        print('wall bottom right', wall_point_bottom_right)
                        
                        if player_point_top_left[0] > wall_point_bottom_right[0] or wall_point_top_left[0] > player_point_bottom_right[0]:
                            print('hit 1')
                            return 'teleport'
                        if ((player_point_bottom_right[1] > wall_point_top_left[1] or wall_point_bottom_right[1]> player_point_top_left[1] ) and remainder_x != 0 ) :
                        

                            print('hit 2')
                            return 'teleport'
                            
                        elif (grid_cord_x == wall_grid_x_cord) and player_point_bottom_right[1]< wall_point_top_left[1] :
                            print('hit 3')
                            return "teleport"
                        
                     
        return False
                
    def collision_check (self, new_x, new_y):

        grid_cord_x = new_x // GRID_SIZE
        grid_cord_y = new_y //GRID_SIZE  
        
        print(grid_cord_x,"grid cord x, gridcordy", grid_cord_y)
    
        for key, list in game_instance.terrain_cords_dict.items():
            
            if key == "teleport":
                
                
                for value in list: 
                   
                    x_cord = value[0]
                    y_cord = value[1]
                    
                    if x_cord in range(grid_cord_x,grid_cord_x +2) and y_cord in range(grid_cord_y, grid_cord_y+2):

                        print(value,"teleport")
                        game_instance.level_number = 2
                        return "teleport"
                    
                    
            elif key =="monster":
                for value in list: 
            
                    x_cord = value[0]
                    y_cord = value[1]
                    if x_cord in range(grid_cord_x-1,grid_cord_x +3) and y_cord in range(grid_cord_y -1, grid_cord_y+3):
                        return (x_cord,y_cord)
                    '''i =-1
                    while i < 2:
                        j = -1
                        while j < 2: 
                            if (new_x,new_y) == (x_cord+i,y_cord+j):
                                return (x_cord,y_cord)
                            j+=1
                        i+= 1'''
          
                    
            
            elif key == "walls": #!= "teleport" and key != "grass full":
                for value in list: 
              
                    x_cord = value[0]
                    y_cord = value[1]
                    
                    if x_cord in range(grid_cord_x,grid_cord_x +2) and y_cord in range(grid_cord_y, grid_cord_y+2):
                        
        
                        print(value,"hit somet")
         
                        return True
                    
        return False 

    
        
        
        
        

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
                for direction_cord in list:      
                    if direction_cord == monster_cord: 
                
                        
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
        (new_x, new_y) = new_monster_cord
        '''
        for key, list in game_instance.terrain_cords_dict.items():
            
            if key != "teleport" and key != "grass full":
        
        '''
        if new_monster_cord == tuple(game_instance.player_pos): 
            return True        
        
        i = -1
        while i < 2:
            j = -1
            print('first')
            while j < 2: 
                if (new_monster_cord[0] + i, new_monster_cord[1]+j) == tuple (game_instance.player_pos):
                #if (game_instance.player_pos[0] + i ,game_instance.player_pos[1]+j) == (new_x,new_y):
                    
                    print("battle time monster collision")
                    return True
                j+=1
            i+= 1

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
        game_instance.move_player()
        
    
    def reset_cord_storage (self):
        game_instance.monster = []
        game_instance.walls = []
        game_instance.map_border=[]
        game_instance.teleport = []
        game_instance.grass_full = []
        game_instance.terrain_cords_dict = {"walls":game_instance.walls, 
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
                        game_instance.walls.append((x_cord,y_cord))
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
            
        