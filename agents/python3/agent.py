from locale import currency
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
    def __init__(self , row , col , obj_type):
        self.row = row 
        self.col = col 
        self.type = obj_type 

        self.h_score = 0
        self.g_score = float("inf")
        self.f_score = float("inf")

        self.id = self.col + self.row * 15

        self.neibours = []

    def add_neibour(self , grid):
        # print("in add neibour")
    
        if self.row > 0 and grid[self.row - 1][self.col].type == 'free': #DOWN
            # print("DOWN" , self.row , self.col , grid[self.row - 1][self.col].type ,  grid[self.row - 1][self.col].id )
            self.neibours.append(grid[self.row - 1][self.col])

        if self.row < 14 and grid[self.row + 1][self.col].type == 'free': #UP
            # print("UP" , self.row , self.col , grid[self.row + 1][self.col].type ,  grid[self.row + 1][self.col].id)
            self.neibours.append(grid[self.row + 1][self.col])

        if self.col < 14 and grid[self.row][self.col + 1].type == 'free': #RIGHT
            # print("RIGHT" , self.row , self.col , grid[self.row][self.col + 1].type ,  grid[self.row][self.col + 1].id)
            self.neibours.append(grid[self.row][self.col + 1])

        if self.col > 0 and grid[self.row ][self.col - 1].type == 'free': #LEFT
            # print("LEFT" , self.row , self.col ,  grid[self.row ][self.col - 1].type , grid[self.row ][self.col - 1].id)
            self.neibours.append(grid[self.row][self.col - 1])

class board():
    def __init__(self , gameState , my_units , unit):
        
        self.gameState = gameState 
        self.units = my_units #D , F , H
        self.unit = unit
        self.start_pos = self.gameState['unit_state'][self.unit]['coordinates']
        # self.end = None   #END POINT TO REACH

        self.obstacle = []

        for i in range(len(self.gameState['entities'])):
            self.obstacle.append([self.gameState['entities'][i]['x'] , self.gameState['entities'][i]['y']])

        #OPPONENT TEAM
        self.obstacle.append(self.gameState['unit_state']['c']['coordinates'])
        self.obstacle.append(self.gameState['unit_state']['e']['coordinates'])
        self.obstacle.append(self.gameState['unit_state']['g']['coordinates'])
        
        #SAME TEAM 
        print(self.unit , self.units)
        # self.units.remove(self.unit)
        for i in self.units:
            
            if i != self.unit:
                self.obstacle.append(self.gameState['unit_state'][i]['coordinates'])
            

        # self.obstacle.append(self.gameState['unit_state']['f']['coordinates'])
        # self.obstacle.append(self.gameState['unit_state']['h']['coordinates'])

        # self.h = lambda start , end : abs(start.row - end.row) + abs(start.col - end.col)
        # print(self.obstacle)
        
        self.grid = [['' for i in range(15)] for j in range(15)] #INITIALIZE EMPTY GRID

        for i in range(14 , -1 , -1):
            # for j in range(14 , -1 , -1):
            for j in range(15):
                if [i , j] in self.obstacle:
                    obj_type = 'obs'
                else:
                    obj_type = 'free'
                self.grid[i][j] = node(i , j , obj_type)
        
        for i in range(14 , -1 , -1):
            # for j in range(14 , -1 , -1):
            for j in range(15):
                self.grid[i][j].add_neibour(self.grid)


        self.start = self.grid[self.start_pos[0]][self.start_pos[1]]
        self.end   = self.grid[7][7]

        # print(self.start.row , self.start.col , self.start.id , self.start.type)

    def h(self ,  start , end):
        return abs(start.row - end.row) + abs(start.col - end.col)

    def take_action(self , came_from , current):
        
        print("in take action")
        while current in came_from:
            current = came_from[current]

            if current != self.start:
                n = current
            # n = current
        # actions = ["up", "down", "left", "right", "bomb", "detonate"]
        
        try:
            print(n.row , n.col , self.start.row , self.start.col , self.unit)
            
            if n.col > self.start.col: 
                print("UP")
                return actions[0]
            elif n.col < self.start.col:
                print("DOWN")
                return actions[1]

            elif n.row > self.start.row: 
                print("RIGHT")
                return actions[3]
            elif n.row < self.start.row: 
                print("LEFT")
                return actions[2]
        except:
            pass

    def path_finding(self):
        
        self.path = {}

        # self.open_set = []
        count = 0
        self.open_set = PriorityQueue()

        # self.open_set.append(self.start)
        self.open_set.put((count , self.start))

        self.start.f_score = self.h(self.start , self.end)
        self.start.g_score = 0

        open_set_hash = {self.start}
        # while self.open_set:
        while not self.open_set.empty():

            
            # current = self.open_set[0]
            # for i in self.open_set:
                # if i.f_score < current.f_score:
                    # current = i 
            current = self.open_set.get()[1]
            open_set_hash.remove(current)

            # print("current : " , current.id )
            # print("current neibour : " , current.neibours )
            # for i in current.neibours:
            #     print(current.id , "NEIBOUR:" , i.id)
            
            if current == self.end:
                action = self.take_action(self.path, current)
                print(" REACHED ")
                return action

            # self.open_set.remove(current)

            for neibour in current.neibours:
                
                # print(neibour.id)
                temp_g_score = current.g_score + 1
                
                if temp_g_score < neibour.g_score:
                    
                    self.path[neibour] = current
                    neibour.g_score = temp_g_score
                    neibour.f_score = temp_g_score + self.h(neibour , self.end)
                    
                    # if neibour not in self.open_set:
                    if neibour not in open_set_hash:
                        count += 1 
                        self.open_set.put((count , neibour))
                        open_set_hash.add(neibour)
                        # self.open_set.append(neibour)
        
        print("CAN'T REACH")
        return False

class Agent():
    def __init__(self):
        self._client = GameState(uri)

        # any initialization code can go here
        self._client.set_game_tick_callback(self._on_game_tick)

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


        #TODO : a function which returns two values , a Action and which unit
        #TODO : Graph position is different 

        #TODO : need to add custom end path to route

        for unit_id in my_units:
            # unit_id = 'd'
            
            b = board(self._client._state , my_units , unit_id)
            # unit_id = 'd'
            #send each unit a random action
            # action = random.choice(actions)
            # print(self._client._state['unit_state']['d']['coordinates'])
            # print(action)
            # print(self._client._state['unit_state']['d']['coordinates'])

            action = b.path_finding()
            del b
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
