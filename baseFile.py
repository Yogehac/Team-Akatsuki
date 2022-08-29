#I'M TOO FAR YOUNG TO WORRY ABOUT MY FAILURES.

# from typing import Union
# from game_state import GameState
# import asyncio
# import random
# import os
# import time
# from queue import PriorityQueue
# from operator import itemgetter
# import numpy as np

from typing import Union

from game_state import GameState
import asyncio
import random
import os
import time
from queue import PriorityQueue
from operator import itemgetter
import numpy as np

uri = os.environ.get(
    'GAME_CONNECTION_STRING') or "ws://127.0.0.1:3000/?role=agent&agentId=agentId&name=defaultName"

actions = ["up", "down", "left", "right", "bomb", "detonate"]

class player:

    def __init__(self , grid , Gameboard , agent_id , unit_id):
        
        self.row = 0
        self.col = 0

        self.id = self.col + self.row * 15
        
        self.grid = grid
        self.gameBoard = Gameboard

        self.agent_id = agent_id 
        self.unit_id = unit_id

        self.bombs = None
        self.hp = None
        self.blast_diameter = None
        self.invulnerability = 0
        
        self.next_node_pos = None

    def next_node(self , action):
        
        if action == 'left':
            self.next_node_pos = self.id - 1
        
        elif action == 'right':
            self.next_node_pos = self.id + 1 
        
        elif action == 'up':
            self.next_node_pos = self.id - 15

        elif action == 'down':
            self.next_node_pos = self.id + 15
        
        elif action == 'bomb' or action == None:
            self.next_node_pos = self.id
        
        # elif action == 'bomb':
            # self.next_node_pos = self.id


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
        self.weight = weight
        
        self.bg = '.'
        
        self.bombs = None
        self.hp = None
        self.expires = None
        self.blast_diameter = None
        self.invulnerability = 0
    
        self.h_score = 0
        self.g_score = float("inf")
        self.f_score = float("inf")

    def add_neibour(self , grid ):

        if self.row > 0 and grid[self.id - 15].weight !=  float("inf"): #UP
            self.neibours.append(grid[self.id - 15])

        if self.row < 14 and grid[self.id + 15].weight !=  float("inf"): #DOWN
            self.neibours.append(grid[self.id + 15])

        if self.col > 0 and grid[self.id -1].weight !=  float("inf") : #LEFT
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
                'c' : player(grid=self.grid , Gameboard=self , agent_id='a' , unit_id='c'),
                'd' : player(grid=self.grid , Gameboard=self , agent_id='b' , unit_id='d'),
                'e' : player(grid=self.grid , Gameboard=self , agent_id='a' , unit_id='e'),
                'f' : player(grid=self.grid , Gameboard=self , agent_id='b' , unit_id='f'),
                'g' : player(grid=self.grid , Gameboard=self , agent_id='a' , unit_id='g'),
                'h' : player(grid=self.grid , Gameboard=self , agent_id='b' , unit_id='h')
            }

        self.weight = 0.1

        # self.hyper

        self.myTeam = None
        
        self.maja = lambda x : [14-x[1] , x[0]] #MAJA FUNCTION i.e is convert col , row to row , col (want to know reason call us :)

        self.h = lambda start , end : abs(start.row - end.row) + abs(start.col - end.col) #Herustic function

        self.linear_fucn = lambda l : l[1] + l[0] * 15 

    def render(self):

        print()

        for i in range(225):
            if i % 15 == 0:
                print()
            
            self.grid[i].bg = self.grid[i].obj_type 
            
            for j in self.p:

                if self.p[j].id == i:
                    self.grid[i].bg = j
         
            print(self.grid[i].bg , end=' ')

        print()

    def update_board(self , gameState): #Everytime the board get updated with current values 

        self.ammo_found = False
        self.ammos = []

        self.power_up_found = False
        self.power_up = None


        self.gameState = gameState 
        # print(self.gameState)

        for i in range(225):
            self.grid[i].board_reset(self.weight)

        #ENTITIES i.e WOOD , STONE , METAL , BOMB , AMMO , FIRE , POWERUP => w , o , m , b , a , x , bp
        for i in self.gameState['entities']:

            x_ = self.maja([i['x'] , i['y']])
            l_ = self.linear_fucn(x_)   

            self.grid[l_].obj_type = i['type']
            
            if i['type']   == 'w':
                # self.grid[l_].weight = i['hp']
                self.grid[l_].weight = 10

            elif i['type'] == 'o':
                # self.grid[l_].weight = i['hp']
                self.grid[l_].weight = 30
            
            elif i['type'] == 'm':
                self.grid[l_].weight = float("inf")
            
            elif i['type'] == 'a':
            
                self.ammo_found = True
                self.ammos.append(self.grid[l_])

                self.grid[l_].expires = i['expires']
                self.grid[l_].weight = self.weight

            elif i['type'] == 'bp':

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

                self.grid[l_].weight = float("inf")

        # BOTs
        # OPPONENT TEAM => c , e , g 
        # OUR TEAM      => d , f , h 
        for i in 'cdefgh':
            
            x_ = self.maja(self.gameState['unit_state'][i]['coordinates'])
            l_ = self.linear_fucn(x_)
            
            self.p[i].row = x_[0]
            self.p[i].col = x_[1]

            self.p[i].id  = l_

            self.p[i].hp = self.gameState['unit_state'][i]['hp']
            self.p[i].bombs = self.gameState['unit_state'][i]['inventory']['bombs']
            self.p[i].blast_diameter = self.gameState['unit_state'][i]['blast_diameter']
            self.p[i].invulnerability = self.gameState['unit_state'][i]['invulnerability']


            if i in self.myTeam:

                if not self.p[i].hp < 1:
                    self.grid[l_].weight = self.weight

                else:
                    self.grid[l_].weight = float("inf")

            else:
                self.grid[l_].weight = float("inf")

        self.render()
        
    def sort_ammo(self , unit):
        
        prior_list = [self.h(self.p[unit] , i) for i in self.ammos]

        return self.ammos[prior_list.index(min(prior_list))].id
        
    def catch_spans(self , unit_id):
        
        if self.ammo_found:

            ammo = self.sort_ammo(unit_id)
            print("AMMO PRESENT SIR !!! " , ammo)
            action , unit_id = self.path_finding(unit_id , ammo)

        elif self.power_up_found:
            
            bp = self.sort_ammo(unit_id)
            print("POWERUP PRESENT SIR !!! " , bp)
            action , unit_id = self.path_finding(unit_id , bp)

        else:
            action = None
        
        return action , unit_id


    def take_action(self , came_from , current , start , end , unit , bomb):
        
        path = []
        tot_cost = 0
        while current in came_from:
            current = came_from[current]
    
            if current != start:
                path.append(current)
                tot_cost += current.weight

        path.insert(0 , end)
        n = path[len(path)-1]
        
        try:
            print(n.row , n.col)
            # if n.obj_type == 'w' and bomb:
            if tot_cost <= bomb:
            # if True:

                print("UNIT ", unit)

                # if n.obj_type == 'w' and False:
                if n.obj_type == 'w':
                    print(unit , " => BOMB")
                    self.p[unit].next_node(actions[4])
                    return actions[4] , unit
                
                else:    
                    if n.id == start.id:
                        print(unit , " => SAME SPOT")
                        self.p[unit].next_node(None)
                        return None , unit
                        # return actions[2] , unit

                    elif n.col > start.col: 
                        print(unit , " => RIGTH")
                        self.p[unit].next_node(actions[3])
                        return actions[3] , unit

                    elif n.col < start.col:
                        print(unit , " => LEFT")
                        self.p[unit].next_node(actions[2])
                        return actions[2] , unit

                    elif n.row > start.row: 
                        print(unit , " => DOWN")
                        self.p[unit].next_node(actions[1])
                        return actions[1] , unit

                    elif n.row < start.row: 
                        print(unit , " => UP")
                        self.p[unit].next_node(actions[0])
                        return actions[0] , unit
            else:

                print("CAN'T REACH , Weight exceed priority")
                print(" CALLING HELP ")

                return None , unit

        except Exception as e:
            print("ERROR IS : " , e)

    def path_finding(self , unit , end_point , bomb=3): 

        start = self.grid[self.p[unit].id]#UNIT postion

        if type(end_point) == list:
            end_point = self.linear_fucn(end_point)

        end = self.grid[end_point]
        
        print(start.id , end.id)
        path = {}

        count = 0
        open_set = PriorityQueue()


        start.f_score = self.h(start , end)
        start.g_score = 0

        open_set.put((start.f_score , count , start))
        open_set_hash = {start}

        while not open_set.empty():

            current = open_set.get()[2]
            open_set_hash.remove(current)

            current.add_neibour(self.grid) 

            if current == end:

                action , unit_player = self.take_action(came_from=path, current=current , start=start ,end=end ,unit=unit , bomb=bomb)
                print(" REACHED " , action , unit_player)
                return action , unit_player

            for neibour in current.neibours:
                
                temp_g_score = current.g_score + neibour.weight
                
                if temp_g_score < neibour.g_score:
                    
                    path[neibour] = current
                    neibour.g_score = temp_g_score
                    neibour.f_score = temp_g_score + self.h(neibour , end)
                    
                    if neibour not in open_set_hash:
                        count += 1 
                        open_set.put((neibour.f_score , count , neibour))
                        open_set_hash.add(neibour)
        
        print("CAN'T REACH" , unit)
        return None , unit

class Agent():
    def __init__(self):
        self._client = GameState(uri)

        # any initialization code can go here
        self._client.set_game_tick_callback(self._on_game_tick)
        self.board = Gameboard()
        print(" CHECK ")

        loop = asyncio.get_event_loop()
        connection = loop.run_until_complete(self._client.connect())
        tasks = [
            asyncio.ensure_future(self._client._handle_messages(connection)),
        ]
        loop.run_until_complete(asyncio.wait(tasks))


    # returns coordinates of the first bomb placed by a unit
    def _get_bomb_to_detonate(self, unit) -> Union[int, int] or None:
        entities = self._client._state.get("entities")
        bombs = list(filter(lambda entity: entity.get(
            "unit_id") == unit and entity.get("type") == "b", entities))
        bomb = next(iter(bombs or []), None)
        if bomb != None:
            return [bomb.get("x"), bomb.get("y")]
        else:
            return None

    async def _on_game_tick(self, tick_number, game_state):

        my_agent_id = game_state.get("connection").get("agent_id")
        my_units = game_state.get("agents").get(my_agent_id).get("unit_ids")

        self.board.myTeam = my_units

        for unit_id in my_units:

            self.board.update_board(self._client._state)       
            
            action , unit_id = self.board.catch_spans(unit_id) #METHOD TO CATCH SPAN 
            
            #to avoid multiple agent tring to jump in one position 
            for i in my_units:

                if self.board.p[unit_id].next_node_pos == self.board.p[i].next_node_pos and i != unit_id:
                    action = None


            if action in ["up", "left", "right", "down"]:
                await self._client.send_move(action, unit_id)

            elif action == "bomb":
                await self._client.send_bomb(unit_id)

            elif action == "detonate":
                bomb_coordinates = self._get_bomb_to_detonate(unit_id)
                if bomb_coordinates != None:
                    x, y = bomb_coordinates
                    await self._client.send_detonate(x, y, unit_id)
            else:
                print(f"Unhandled action: {action} for unit {unit_id}")


def main():
    for i in range(0,10):
        while True:
            try:
                Agent()
            except:
                time.sleep(5)
                continue
            break


if __name__ == "__main__":
    main()