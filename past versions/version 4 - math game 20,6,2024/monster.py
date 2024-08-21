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
                
    
        