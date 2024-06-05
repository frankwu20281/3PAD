MAP_SIZE = 40 
WINDOW_SIZE = 600  
GRID_SIZE = 40
VIEWPORT_SIZE = WINDOW_SIZE // GRID_SIZE   

class Map():
    def __init__(self, x):
        global game_instance
        game_instance = x
        
        game_instance.player_pos = []
        self.reset_cord_storage()
        self.spawn_location()
        self.terrain_load()
        game_instance.monster_handler.monster_path_load()
        game_instance.new_frame()

    
    def next_level (self): 
        game_instance.level_number= 2
        game_instance.player_pos = []
        self.reset_cord_storage()
        self.spawn_location()
        self.terrain_load()
        game_instance.monster_handler.monster_path_load()
        game_instance.new_frame()
    
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
                    game_instance.player_pos = [x_cord,y_cord]
                    game_instance.grass_full.append((x_cord,y_cord))
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