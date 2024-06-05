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
        print("new")


    def move_monster_cords(self): 

        for monster_cord in game_instance.monster: 
            print("old monster cord" + str(monster_cord))
            direction = {"down": (monster_cord[0],monster_cord[1]+1),
                         "up": (monster_cord[0],monster_cord[1]-1),
                         "left": (monster_cord[0]-1,monster_cord[1]),
                         "right": (monster_cord[0]+1,monster_cord[1])}
            
            for key, list in game_instance.monster_movement_cords_dict.items():
                for direction_cord in list: 
                    if tuple(direction_cord) == monster_cord: 
                        print("found " , key)
                        
                        new_monster_cord = direction[key]
                        try:
                            if not self.collison_check(new_monster_cord):
                        
                                print("new monster cords", new_monster_cord)
                                print("monster list" ,game_instance.monster)
                                game_instance.monster.remove(monster_cord)
                                game_instance.monster.append(new_monster_cord)
                        except (ValueError):
                            print("error")
                            
                        
                        
                        print("monster list after" ,game_instance.monster)
                        #if not self.collison_check(new_monster_cord, game_instance): 
        
        
        
                        
            
    
    def collison_check(self, new_monster_cord): 
        new_x, new_y = new_monster_cord[0], new_monster_cord[1]

        for key, list in game_instance.terrain_cords_dict.items():
            
            if key != "teleport" and key != "grass full":
                
                if (new_x,new_y) == tuple(game_instance.player_pos):
                    game_instance.battle_handler
                    print("battle time monster collision")
                    return "battle time"
                elif (new_x,new_y) in list: 

                    print('hit something ')
                    return True
    
        return False