MAP_SIZE = 40 
WINDOW_SIZE = 600  
GRID_SIZE = 40
VIEWPORT_SIZE = WINDOW_SIZE // GRID_SIZE   

class Map():
    def __init__(self, game_instance):
        
        game_instance.reset_cord_storage()
        
        game_instance.player_pos = []

        self.spawn_location(game_instance)
        self.terrain_load(game_instance)
        


    def spawn_location (self, game_instance):
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


    def terrain_load(self,game_instance):
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
        
        game_instance.monster_handler.monster_path_load()
        game_instance.new_frame()
        print('terrain loaded in')