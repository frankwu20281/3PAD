



        
class Player(): 
    def __init__(self, x) -> None:
        global game_instance
        
        game_instance = x 
        
        pass
        
    def key_press( self, event):
        
        direction = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }.get(event.keysym)

        if direction: 
            new_x = game_instance.player_pos[0] + direction[0]
            new_y = game_instance.player_pos[1] + direction[1]
            
            col = self.collision_check(new_x,new_y)
            if col == True:
                return [new_x, new_y]
           
            else: 
                return col
        else:
            return False
            
            
                
                

    def collision_check (self, new_x, new_y):
        for key, list in game_instance.terrain_cords_dict.items():
            if key == "teleport":
                if (new_x,new_y) in list: 
                    game_instance.level_number = 2
                    return "teleport"
            elif key =="monster":
                if (new_x,new_y) in list:
                    
                    
                    return "battle time"
            elif key != "teleport" and key != "grass full":
                if (new_x,new_y) in list: 
                    return False
        return True
        
    