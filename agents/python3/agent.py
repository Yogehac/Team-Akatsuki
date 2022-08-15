#I'M TOO FAR YOUNG TO WORRY ABOUT MY FAILURES.

from typing import Union
from game_state import GameState
import asyncio
import random
import os
import time
from queue import PriorityQueue

uri = os.environ.get(
    'GAME_CONNECTION_STRING') or "ws://127.0.0.1:3000/?role=agent&agentId=agentId&name=defaultName"

actions = ["up", "down", "left", "right", "bomb", "detonate"]


class node:
    
    def __init__(self , row , col):

        self.row = row
        self.col = col

        self.obj_type = '.' #Type of This node i.e ENTITY type (Refer line : 53)
    
        self.id = self.col + self.row * 15

        self.neibours = []

    def score_reset(self):

        self.h_score = 0
        self.g_score = float("inf")
        self.f_score = float("inf")

    def add_neibour(self , grid ):
         
        if self.row > 0 and grid[self.row - 1][self.col].obj_type == '.': #UP
            self.neibours.append(grid[self.row - 1][self.col])

        if self.row < 14 and grid[self.row + 1][self.col].obj_type == '.': #DOWN
            self.neibours.append(grid[self.row + 1][self.col])

        if self.col > 0 and grid[self.row ][self.col - 1].obj_type == '.': #LEFT
            self.neibours.append(grid[self.row][self.col - 1])
        
        if self.col < 14 and grid[self.row][self.col + 1].obj_type == '.': #RIGHT
            self.neibours.append(grid[self.row][self.col + 1])

class Gameboard:

    def __init__(self): 

        self.grid = [[node(i , j) for j in range(15)] for i in range(15)] #i row , j col

        self.maja = lambda x : [14-x[1] , x[0]] #MAJA FUNCTION i.e is convert col , row to row , col (want to know reason call us :)

        self.h = lambda start , end : abs(start.row - end.row) + abs(start.col - end.col) #Herustic function


    def update_board(self , gameState): #Everytime the board get updated with current values 

        self.gameState = gameState 
        
        for i in range(15):
            for j in range(15):
                self.grid[j][i].obj_type = '.' #MAJA FUNCTION i.e is convert col , row to row , col

        #ENTITIES i.e WOOD , STONE , METAL , BOMB , AMMO , FIRE , POWERUP => w , o , m , b , a , x , bp
        for i in self.gameState['entities']:
            self.grid[14-i['y']][i['x']].obj_type = i['type'] #MAJA FUNCTION i.e is convert col , row to row , col

        # BOTs
        # OPPONENT TEAM => c , e , g 
        # OUR TEAM      => d , f , h 
        for i in 'cdefgh':
            x = self.maja(self.gameState['unit_state'][i]['coordinates'])
            self.grid[x[0]][x[1]].obj_type = i


        for i in range(15):
            for j in range(15):

                print(self.grid[i][j].obj_type , end=' ')
            print()


    def take_action(self , came_from , current):
        
        path = []
        while current in came_from:
            current = came_from[current]
    
            if current != self.start:
                path.append(current)
        
        path.insert(0 , self.end)
        n = path[len(path)-1]
        print(n.row , n.col)

        try:
            print(n.row , n.col)
                  
            if n.col > self.start.col: 
                # print("RIGTH")
                return actions[3]

            elif n.col < self.start.col:
                # print("LEFT")
                return actions[2]

            elif n.row > self.start.row: 
                # print("DOWN")
                return actions[1]

            elif n.row < self.start.row: 
                # print("UP")
                return actions[0]
        except:
            pass

    def path_finding(self , unit , end): 

        start_pos = self.maja(self.gameState['unit_state'][unit]['coordinates']) #UNIT postion #if not work remember to remove him from node

        self.start = self.grid[start_pos[0]][start_pos[1]]

        # self.end = self.grid[0][7]
        self.end = self.grid[end[0]][end[1]]

        for i in range(15):
            for j in range(15):              
                self.grid[i][j].score_reset()           

        self.path = {}

        count = 0
        self.open_set = PriorityQueue()

        self.open_set.put((count , self.start))

        self.start.f_score = self.h(self.start , self.end)
        self.start.g_score = 0

        open_set_hash = {self.start}
        while not self.open_set.empty():

            current = self.open_set.get()[1]
            open_set_hash.remove(current)

            current.add_neibour(self.grid) 

            if current == self.end:
                action = self.take_action(self.path, current)
                print(" REACHED ")
                return action

            for neibour in current.neibours:
                
                temp_g_score = current.g_score + 1
                
                if temp_g_score < neibour.g_score:
                    
                    self.path[neibour] = current
                    neibour.g_score = temp_g_score
                    neibour.f_score = temp_g_score + self.h(neibour , self.end)
                    
                    if neibour not in open_set_hash:
                        count += 1 
                        self.open_set.put((count , neibour))
                        open_set_hash.add(neibour)
        
        print("CAN'T REACH")
        return False

class Agent():
    def __init__(self):
        self._client = GameState(uri)

        # any initialization code can go here
        self._client.set_game_tick_callback(self._on_game_tick)
        self.board = Gameboard()



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

        # get my units
        my_agent_id = game_state.get("connection").get("agent_id")
        my_units = game_state.get("agents").get(my_agent_id).get("unit_ids")


        for unit_id in my_units:
            
            # unit_id = 'f'
            
            self.board.update_board(self._client._state)       
            
            ammo = []
            bp   = None

            for i in range(15):
                for j in range(15):
                    if self.board.grid[i][j].obj_type == 'a':
                        ammo = [i ,j]
                        # ammo.append([i ,j])

                    if self.board.grid[i][j].obj_type == 'bp':
                        bp = [i , j]

            if ammo:
                # for  i in ammo:
                print("AMMO PRESENT SIR !!! " , ammo)
                action = self.board.path_finding(unit_id , ammo)

            elif bp:
                
                print("POWER PRESENT SIR !!! " , bp)
                action = self.board.path_finding(unit_id , bp)

            else:
                x = random.randint(0 , 14)
                y = random.randint(0 , 14)
                end = [x , y]
                print("END SIR !!! " , end)

                action = self.board.path_finding(unit_id , end)

            # action = random.choice(actions)
            print(action)
       
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
