#OUR IMPORTS    
from queue import PriorityQueue
from operator import itemgetter
from tabnanny import check
from tkinter.tix import Tree
import numpy as np
import random

class player:

    def __init__(self , grid , Gameboard , agent_id , unit_id , hp):
        
        self.row = 0
        self.col = 0

        self.id = self.col + self.row * 15
        
        self.grid = grid
        self.gameBoard = Gameboard

        self.agent_id = agent_id 
        self.unit_id = unit_id

        self.bombs = None
        self.hp = hp 
        self.blast_diameter = None
        self.invulnerability = 0
        self.stunned = 0
        
        
        self.next_node_pos = None

        self.target_ammo = None

        self.goto = [7 , 94]


    def next_node(self , action ,  unit=None):
        
        if action == 'left':
            self.next_node_pos = self.id - 1
        
        elif action == 'right':
            self.next_node_pos = self.id + 1 
        
        elif action == 'up':
            self.next_node_pos = self.id - 15

        elif action == 'down':
            self.next_node_pos = self.id + 15
        
        elif action == 'bomb':
            
            self.can_i_place_bomb_here(unit)
            self.next_node_pos = self.id

        elif action == None:

            self.next_node_pos = self.id
        
        # elif action == 'bomb':
            # self.next_node_pos = self.id

    def can_i_place_bomb_here(self , unit):
        
        straight = True


    def move_on(self , start , to_node=None , told_by=None , single_Step=False):
        
        if not single_Step:

            print(" FUCNTION CALLED " , self.unit_id)
            self.grid[self.id].add_neibour(self.grid)
            
            neibour = self.grid[self.id].neibours

            neibour.remove(start)
            neibour.remove(to_node)

            least_Weight = float("inf")
            for i in neibour:
                if i.weight < least_Weight:
                    least_Weight = i.weight
                    to_ = i
            
            print(" CHOOSING TYPE : ", to_.obj_type , " LOC : " , to_.id)
            # to_ = random.choice(neibour)

            print("UNIT NAME : " , self.unit_id)
            return self.gameBoard.path_finding(unit=self.unit_id , end_point=to_.id , check=True)

        else:

            self.grid[self.id].add_neibour(self.grid)
            neibour = self.grid[self.id].neibours
            neibour.remove(start)

            least_Weight = float("inf")
            for i in neibour:
                if i.weight < least_Weight:
                    least_Weight = i.weight
                    to_ = i
            
            print(" CHOOSING TYPE : ", to_.obj_type , " LOC : " , to_.id)
            # to_ = random.choice(neibour)

            print("UNIT NAME : " , self.unit_id)
            return self.gameBoard.path_finding(unit=self.unit_id , end_point=to_.id , check=True)


    #HELP TEAM MATES TO OPEN A PATH OR SOMETHING
    # def help_me(self , unit , pos):
        
    #     print("BEFORE INSIDE HELP ME FUNCTION : " , unit)
    #     action , unit = self.gameBoard.path_finding(unit=unit , end_point=pos , bomb=10 ,help=True)
    #     print("AFTER INSIDE HELP ME FUNCTION : " , action , unit)
    #     return action , unit


class node:
    
    def __init__(self , row , col):

        self.row = row
        self.col = col
        self.id = self.col + self.row * 15

        self.neibours = []

    def board_reset(self , weight):
        
        self.obj_type = '.' #Type of This node i.e ENTITY type (Refer line : 53)

        self.bg = '.'

        self.player = None

        self.weight = weight
        self.is_visited = False
        
        self.bombs = None
        self.hp = None
        self.expires = None
        self.blast_diameter = None
        self.invulnerability = 0
    
        self.h_score = 0
        self.g_score = float("inf")
        self.f_score = float("inf")

    def add_neibour(self , grid):

        if self.row > 0 and grid[self.id - 15].weight !=  float("inf"): #UP
            self.neibours.append(grid[self.id - 15])

        if self.row < 14 and grid[self.id + 15].weight !=  float("inf"): #DOWN
            self.neibours.append(grid[self.id + 15])

        if self.col > 0 and grid[self.id -1].weight !=  float("inf"): #LEFT
            self.neibours.append(grid[self.id - 1])
        
        if self.col < 14 and grid[self.id + 1].weight !=  float("inf"): #RIGHT
            self.neibours.append(grid[self.id + 1])        

class Gameboard:

    def __init__(self): 

        g = []
        for i in range(15):
            for j in range(15):
                g.append(node(i , j))
        
        self.grid = np.array(g)

        self.p = {
                'c' : player(grid=self.grid , Gameboard=self , agent_id='a' , unit_id='c' , hp=3),
                'd' : player(grid=self.grid , Gameboard=self , agent_id='b' , unit_id='d' , hp=3),
                'e' : player(grid=self.grid , Gameboard=self , agent_id='a' , unit_id='e' , hp=3),
                'f' : player(grid=self.grid , Gameboard=self , agent_id='b' , unit_id='f' , hp=3),
                'g' : player(grid=self.grid , Gameboard=self , agent_id='a' , unit_id='g' , hp=3),
                'h' : player(grid=self.grid , Gameboard=self , agent_id='b' , unit_id='h' , hp=3)
            }
            
        self.actions = ["up", "down", "left", "right", "bomb", "detonate"]

        self.weight = 0.1

        self.myTeam = None
        
        self.maja = lambda x : [14-x[1] , x[0]] #MAJA FUNCTION i.e is convert col , row to row , col (want to know reason call us :)

        self.h = lambda start , end : abs(start.row - end.row) + abs(start.col - end.col) #Herustic function

        self.linear_fucn = lambda l : l[1] + l[0] * 15 

        self.bomb_is_here = lambda x : True if self.grid[self.p[x].id].obj_type == 'b' else False


        self.this_player = 'f'

    def render(self, game=False):

        print()

        for i in range(225):
            if i % 15 == 0:
                print()

            if game:
                self.grid[i].bg = self.grid[i].obj_type 
            else:
                self.grid[i].bg = self.grid[i].g_score 

            for j in self.p:

                if self.p[j].id == i:
                    self.grid[i].bg = j
         
            print(self.grid[i].bg , end=' ')
        
        print()

    def update_board(self , gameState , tick_number=None): #Everytime the board get updated with current values 

        self.ammo_found = False
        self.ammos = []

        self.power_up_found = False
        # self.power_up = None

        self.gameState = gameState 
        # print(self.gameState)

        self.tick_number = tick_number

        for i in range(225):
            self.grid[i].board_reset(self.weight)

        #ENTITIES i.e WOOD , STONE , METAL , BOMB , AMMO , FIRE , POWERUP => w , o , m , b , a , x , bp
        for i in self.gameState['entities']:

            x_ = self.maja([i['x'] , i['y']])
            l_ = self.linear_fucn(x_)   

            self.grid[l_].obj_type = i['type']
            
            if i['type']   == 'w':
                # self.grid[l_].weight = i['hp'] * 10
                self.grid[l_].weight = 1

            elif i['type'] == 'o':
                self.grid[l_].weight = i['hp'] * 30
            
            elif i['type'] == 'm':
                self.grid[l_].weight = float("inf")
            
            # elif i['type'] == 'a':
            
            #     self.ammo_found = True
            #     self.ammos.append(self.grid[l_])

            #     self.grid[l_].expires = i['expires']
            #     self.grid[l_].weight = self.weight

            # elif i['type'] == 'bp':

            #     self.grid[l_].weight = self.weight
            #     self.ammos.append(self.grid[l_])

            #     self.power_up_found = True
            #     self.power_up = l_
            #     self.grid[l_].expires = i['expires']

            
            elif i['type'] == 'fp':

                self.grid[l_].weight = self.weight
                self.ammos.append(self.grid[l_])

                self.power_up_found = True
                self.power_up = l_
                self.grid[l_].expires = i['expires']

            elif i['type'] == 'b':

                self.grid[l_].weight = float("inf")
                self.grid[l_].blast_diameter = i['blast_diameter']
                self.grid[l_].expires = i['expires']

            elif i['type'] == 'x':

                # self.grid[l_].weight = float("inf")
                self.grid[l_].weight = 90
                # self.grid[l_].weight = 10

        # BOTs
        # OPPONENT TEAM => c , e , g 
        # OUR TEAM      => d , f , h 
        for i in self.total_players:
            
            x_ = self.maja(self.gameState['unit_state'][i]['coordinates'])
            l_ = self.linear_fucn(x_)
            
            self.grid[l_].player = i

            self.p[i].row = x_[0]
            self.p[i].col = x_[1]

            self.p[i].id  = l_

            self.p[i].hp = self.gameState['unit_state'][i]['hp']
            self.p[i].bombs = self.gameState['unit_state'][i]['inventory']['bombs']
            self.p[i].blast_diameter = self.gameState['unit_state'][i]['blast_diameter']
            self.p[i].invulnerability = self.gameState['unit_state'][i]['invulnerable']
            self.p[i].stunned = self.gameState['unit_state'][i]['stunned']

            if i in self.myTeam:

                if self.p[i].hp > 0:
                    self.grid[l_].weight = self.weight

                else:
                    self.grid[l_].weight = float("inf")

            else:
                self.grid[l_].weight = float("inf")
            
        self.render(game=True)

    def active_agents(self, my_units):
        
        self.myTeam = []
        self.total_players = ['c','d','e','f','g','h']

        for i in my_units:

            if self.p[i].hp > 0:
                self.myTeam.append(i)
            
            else:
                self.total_players.remove(i)
                
        return self.myTeam

    def move_away_from_bomb(self , unit):
        
        start = self.grid[self.p[unit].id]
    
        neibour = random.choice(start.neibours)
        print(" BOMB IS HERE, RUN RA PANDA ") 
        print(neibour.id)
        return self.path_finding(unit=unit , end_point=neibour.id)

    
    def sort_ammo(self , unit):

        prior_list = [self.h(self.p[unit] , i) for i in self.ammos]
        ele = self.ammos.pop(prior_list.index(min(prior_list)))
    
        return ele.id
        
    def catch_spans(self , unit_id):
        
        # if self.ammo_found:

        #     ammo = self.sort_ammo(unit_id)
        #     print("AMMO PRESENT SIR !!! " , ammo)
        #     if ammo != None:
        #         action , unit_id = self.path_finding(unit_id , ammo)
        #     else:
        #         action = None

        if self.power_up_found:
            
            bp = self.sort_ammo(unit_id)
            print("POWERUP PRESENT SIR !!! " , bp)

            if bp != None:
                action , unit_id = self.path_finding(unit_id , bp)
            else:
                action = None

        else:
            action = None
        
        return action , unit_id

    def take_action(self , came_from , current , start , end , unit , bomb):
        
        bomb = float("inf")
        path = []
        tot_cost = 0
        while current in came_from:
            current = came_from[current]
    
            if current != start:
                path.append(current)
                tot_cost += current.weight

        path.insert(0 , end)
        n = path[len(path)-1]
        # print("UNIT LETS SEE : " , unit , " PATH LEN : " , len(path))
        
        try:
            print(" TOTAL WEIGHT ", tot_cost)
            # if n.obj_type == 'w' and bomb:
            if tot_cost <= bomb:

                print("UNIT ", unit , start.id)

                if start.obj_type == 'b':
                
                    neibour = random.choice(start.neibours)
                    print(" BOMB IS HERE, RUN RA PANDA ") 
                    print(neibour.id)
                    return self.path_finding(unit=unit , end_point=neibour.id)

                elif n.player in self.myTeam:

                    if len(path) > 1:
                        # print(" CALLED BY " , unit)
                        n2 = path[len(path)-2]
                        action , unit = self.p[n.player].move_on(start , to_node=n2)
                        return action , unit

                    else:
                        action , unit = self.p[n.player].move_on(start , to_node=None , told_by=n.player , single_Step=True)
                        self.this_player = 'd'
                        return action , unit

                elif n.obj_type == 'w':
                    print(unit , " => BOMB")
                    # self.p[unit].next_node(unit , self.actions[4])
                    return self.actions[4] , unit
                
                elif n.obj_type == 'o':
                    print(unit , " => BOMB")
                    # self.p[unit].next_node(unit , self.actions[4])
                    return self.actions[4] , unit

                elif n.id == start.id:
                    print(unit , " => SAME SPOT")
                    self.p[unit].next_node(None)
                    return None , unit

                elif n.col > start.col: 
                    print(unit , " => RIGTH  ", n.id)
                    self.p[unit].next_node(self.actions[3])
                    return self.actions[3] , unit

                elif n.col < start.col:
                    print(unit , " => LEFT ", n.id)
                    self.p[unit].next_node(self.actions[2])
                    return self.actions[2] , unit

                elif n.row > start.row: 
                    print(unit , " => DOWN ", n.id)
                    self.p[unit].next_node(self.actions[1])
                    return self.actions[1] , unit

                elif n.row < start.row: 
                    print(unit , " => UP ", n.id)
                    self.p[unit].next_node(self.actions[0])
                    return self.actions[0] , unit
                
                # else:
                #     action = None
                #     return action , unit
            else:

                print("CAN'T REACH , Weight exceed priority")
                print(" CALLING HELP ")

                return None , unit

        except Exception as e:
            print("ERROR IS : " , e)

    def path_finding(self , unit , end_point , bomb=10 , check=False): 
        
        if check:
            self.update_board(self.gameState)

        # print(" PATH FINDING UNIT : " , unit)

        start = self.grid[self.p[unit].id]#UNIT postion

        if type(end_point) == list:
            end_point = self.linear_fucn(end_point)

        end = self.grid[end_point]
        
        if start == end:
            action = None
            # print("SAME POINT : ", unit)
            return action , unit

        path = {}

        count = 0

        start.f_score = self.h(start , end)
        start.g_score = 0

        open_set = PriorityQueue()
        open_set.put((start.f_score , count , start))
        open_set_hash = {start}

        while not open_set.empty():

            current = open_set.get()[2]
            # current = open_set.get()[2]

            if current == end:

                action , unit_player = self.take_action(came_from=path, current=current , start=start ,end=end ,unit=unit , bomb=bomb )
                # print(" REACHED " , action , unit_player)
                return action , unit_player

            open_set_hash.remove(current)

            current.add_neibour(self.grid) 

            for neibour in current.neibours:
                
                temp_g_score = current.g_score + neibour.weight
                
                if temp_g_score < neibour.g_score:
                    
                    path[neibour] = current
                    neibour.g_score = temp_g_score
                    neibour.f_score = temp_g_score + self.h(neibour , end)
                    
                    if neibour not in open_set_hash:
                        count += 1 
                        open_set.put((neibour.f_score , count ,  neibour))
                        open_set_hash.add(neibour)
        
        # print("CAN'T REACH" , unit)
        return None , unit


    def AI(self , unit_id):
          
        # action , unit_id = self.path_finding(unit=unit_id , end_point=[0 , 7])
        if self.power_up_found:
            action , unit_id = self.catch_spans(unit_id=unit_id)

        else:        
            action , unit_id = self.path_finding(unit=unit_id , end_point=self.p[unit_id].goto[-1])

        
        for i in self.myTeam:
            if self.p[unit_id].next_node_pos == self.p[i].next_node_pos and i != unit_id:
                self.p[unit_id].next_node(None)

                action = None

        print("ACTION : " , action , "UNIT : " , unit_id)

        return action , unit_id
        