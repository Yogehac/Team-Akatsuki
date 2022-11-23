# OUR IMPORTS
from queue import PriorityQueue
from operator import itemgetter
import numpy as np
import random
from collections import deque



class player:

    def __init__(self, grid, Gameboard, agent_id, unit_id, hp):

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

        self.invulnerable = 0

        self.stunned = 0

        self.evade_loc = False

        self.next_node_pos = None

        self.bomb_hash = {}

        # self.
        # self.previous_target_ammo = [] #PREVIOUS
        self.previous_target_ammo = set()  # PREVIOUS
        self.target_ammo = []  # CURRENT

        # self.goto = [7]
        # self.goto = [None , 17]
        # self.goto = [None , 135]

        self.go = None

        # if self.unit_id == 'd':
        #     self.goto = [None , 112]
        #     self.center = 112

        # elif self.unit_id == 'f':
        #     self.goto = [None , 127]
        #     self.center = 127

        # elif self.unit_id == 'h':
        #     self.goto = [None , 98 ] # self.grid[77].`obj_type == 'b' => self.grid[77].obj_type == '.'
        #     self.center = 98

        # self.grid[77].`obj_type == 'b' => self.grid[77].obj_type == '.'
        self.goto = [None, 112]
        self.center = 112

        # ************

        # self.goto = [None , 112]
        # self.safe = {
        #     'safe' : False,
        #     'safe_spot' : 78,
        #     'target_list' : []
        # }
        # self.goto[-1] = 23

        # self.goto = 112
        # self.goto = 51
#######################################################################################################################
        # Team 7

        # Team 7
        self.eInfo = {
            'attack': False,
        }
        self.role = None
        self.breakWood = False

    # Team 7

    def resetEn(self):

        u = self.eInfo['unit']
        
        del self.gameBoard.currAtks[u]
        
        self.eInfo = {
            'attack': False
        }
        
        if self.gameBoard.teamN == 0:
        
            self.goto[1] = 127
            self.gameBoard.teamN += 1

    def updEn(self, unit):  # UNIT => ENEMY

        eId = self.gameBoard.p[unit].id  # GETTING ENEMY ID

        self.goto[1] = self.eInfo['id'] = eId

        # self.eInfo['attack'] = True
        self.eInfo['unit'] = unit  # ENEMY UNIT

        neibour = self.grid[eId].add_neibour(
            self.grid, evade=True, atk=True)  # EMPTY SPOTS

        h = 1000

        for i in neibour:

            # j = self.gameBoard.h(self.grid[self.id], i)
            j = self.gameBoard.h(self, i)

            if j < h:
                h = j
                # end_node = i
                print('insiside E_NEIGH')
                self.eInfo['eNeigh'] = i

        if self.eInfo['eNeigh'].id == self.id:
            self.eInfo['attack'] = True

        else:
            self.eInfo['attack'] = False

    def whoseThr(self, node, l, who=False):

        n = node  # 112

        start = n - (l*15)  # 97

        end = n + (l*15)  # 127

        temp = list()
        enemy = list()
        obs = list()

        for i in range(start, end+1, 15):  # 97  -  127 , 15 => O(1)
            for x in range(i-l, i+l+1):  # 96   -  99

                if x == n or x < 0 or x > 224:  # x => 112
                    pass
                else:
                    if who:
                        if self.grid[x].obj_type == 'w' or self.grid[x].obj_type == 'o':
                            obs.append(x)
                        elif self.grid[x].enemy:
                            enemy.append(x)
                    temp.append(x)
        if who:
            return enemy, obs
        else:
            return temp

    def attack(self):

        print(" INSIDE ATTACK ")

        center = 112

        surr = self.whoseThr(center, 1)

        if self.id in surr or self.id == center or True:
            # nearest enemy finder
            temp = float('inf')
            e = None  # closer enemy var

            for i in self.gameBoard.eTeam:  # C , E , G

                print(" ENEMY : ", i)
                manHat = self.gameBoard.h(self, self.gameBoard.p[i])

                if temp > manHat:
                    temp = manHat

                    e = i  # C

                    try:
                        self.gameBoard.currAtks[e]

                    except Exception as err:
                        # ENEMY => TEAMATE
                        self.gameBoard.currAtks[e] = self.unit_id
                        break

            if e:
                self.updEn(e)
                print('eINFO ..................')
                
            try:
                self.board.update_board(self._client._state , tick_number)       

                action , unit_id = self.board.AI(unit_id=unit_id)

            except Exception as e:
                action = None
                print(" [ ERROR ] " , e)
            
                print(self.eInfo)

    def kingAtk(self, unit):
        self.updEn(unit)

    def coreAtk(self):

        surr = self.whoseThr(self.center, 1)

        if self.id in surr or self.id == self.center or self.breakWood:

            fxf = self.whoseThr(self.center, 2, True)

            if len(fxf[0]) > 0:

                self.kingAtk(self.grid[fxf[0][0]].player)
                self.breakWood = True

                return self.gameBoard.path_finding(
                    unit=self.unit_id, end_point=self.goto[1])

            else:

                try:
                    self.breakWood = False
                    self.eInfo['unit']
                    self.resetEn()

                except Exception as e:
                    print("NO Enemy **" , e)
                # self.resetEn()

            return None, self.unit_id

        else:

            action, unit_id = self.gameBoard.path_finding(
                unit=self.unit_id, end_point=self.goto[1])

            return action, unit_id

    def soldier(self):
        # if self.eInfo['unit'] not in self.gameBoard.eTeam:

        if self.eInfo['unit'] not in self.gameBoard.eTeam and len(self.gameBoard.eTeam) > 0:
          
            lowCost = dict()
          
            for i in self.gameBoard.eTeam:
                # if i not in self.gameBoard.currAtks.keys():
                temp = self.gameBoard.path_finding(
                    unit=self.unit_id, end_point=self.gameBoard.p[i].id, team7=True)
          
                lowCost[temp] = i
          
            minD = min(lowCost.keys())
          
            self.updEn(lowCost[minD])
        # elif self.eInfo['unit'] not in self.gameBoard.eTeam and len(self.gameBoard.eTeam) == 1:
        #     self.setRole('king')
        #     self.resetEn()

            # return self.coreAtk()

        self.updEn(self.eInfo['unit'])

        if self.eInfo['attack']:

            if self.gameBoard.can_i(self.unit_id):
                return self.gameBoard.actions[4], self.unit_id
            else:
                return None , self.unit_id
        else:
            return self.gameBoard.path_finding(unit=self.unit_id, end_point=self.eInfo['eNeigh'].id)

    def farmer(self):

        txt = self.whoseThr(self.id, 1, True)
        # comment this if and change next to elif to if

        if self.breakWood:  # jiggle rectified

            return self.gameBoard.path_finding(
                unit=self.unit_id, end_point=self.goto[1])

        elif len(txt[0]) > 0:
            
            self.kingAtk(self.grid[txt[0][0]].player)
            self.breakWood = True
            
            return self.gameBoard.path_finding(
                unit=self.unit_id, end_point=self.goto[1])
        
        elif len(txt[1]) > 0:
            self.breakWood = True
            return self.gameBoard.path_finding(unit=self.unit_id, end_point=txt[1][0])
        
        else:
        
            self.breakWood = False
        
            try:
                self.eInfo['unit']
                self.resetEn()
        
            except Exception as e:
                print("NO Enemy **")
        
            return self.gameBoard.path_finding(unit=self.unit_id, end_point=self.center)

    def setRole(self, type):
        
        if type == 'king':

            print(f'UNIT {self.unit_id} - ROLE ASSIGNED - "CORE ATTACKER"')

            self.role = self.coreAtk
            self.title = 'KING'

        elif type == 'soldier':
            
            print(f'UNIT {self.unit_id} - ROLE ASSIGNED - "Brave Soldier"')

            self.role = self.soldier
            self.title = 'SOLDIER'

        elif type == 'farmer':
            
            print(f'UNIT {self.unit_id} - ROLE ASSIGNED - "Tiredless Farmer"')

            self.role = self.farmer
            self.title = 'FARMER'

        else:
            print(f'UNIT {self.unit_id} - ROLE ASSIGNED - "sucide"')

    ###################################################################################################################

    def next_node(self, action,  unit=None):

        if action == 'left':
            self.next_node_pos = self.id - 1

        elif action == 'right':
            self.next_node_pos = self.id + 1

        elif action == 'up':
            self.next_node_pos = self.id - 15

        elif action == 'down':
            self.next_node_pos = self.id + 15

        elif action == 'bomb':

            self.next_node_pos = self.id

        elif action == None or action == 'detonate':

            self.next_node_pos = self.id

    # def move_on(self, start, to_node=None, told_by=None, single_Step=False):

    #     if not single_Step:

    #         print(" FUCNTION CALLED ", self.unit_id)
    #         neibour = self.grid[self.id].add_neibour(self.grid)

    #         # neibour = self.grid[self.id].neibours

    #         neibour.remove(start)
    #         neibour.remove(to_node)

    #         least_Weight = float("inf")
    #         for i in neibour:
    #             if i.weight < least_Weight:
    #                 least_Weight = i.weight
    #                 to_ = i

    #         if len(neibour) > 0:
    #             print(" CHOOSING TYPE : ", to_.obj_type, " LOC : ", to_.id)
    #             # to_ = random.choice(neibour)

    #             print("UNIT NAME : ", self.unit_id)
    #             self.goto.append(to_.id)
    #             # self.go = to_.id
    #             return self.gameBoard.path_finding(unit=self.unit_id, end_point=self.goto[-1], check=True)

    #         return None , self.unit_id
    #         # return self.gameBoard.path_finding(unit=self.unit_id , end_point=self.go , check=True)

    #     else:
    #         # action , unit = self.p[n.player].move_on(start , to_node=None , told_by=n.player , single_Step=True)

    #         neibour = self.grid[self.id].add_neibour(self.grid)
    #         # neibour = self.grid[self.id].neibours

    #         neibour.remove(start)

    #         least_Weight = float("inf")
    #         for i in neibour:
    #             if i.weight < least_Weight:
    #                 least_Weight = i.weight
    #                 to_ = i

    #         if len(neibour) > 0:
            
    #             print(" CHOOSING TYPE : ", to_.obj_type, " LOC : ", to_.id)
    #             # to_ = random.choice(neibour)

    #             print("UNIT NAME : ", self.unit_id)
    #             self.goto.append(to_.id)
    #             # return self.gameBoard.path_finding(unit=self.unit_id , end_point=self.goto[-1] , check=True)

    #             # self.go = to_.id
    #             return self.gameBoard.path_finding(unit=self.unit_id, end_point=self.goto[-1], check=True)


    #         return None , self.unit_id
            
            # return self.gameBoard.path_finding(unit=self.unit_id , end_point=self.go , check=True)

    # HELP TEAM MATES TO OPEN A PATH OR SOMETHING
    # def help_me(self , unit , pos):

    #     print("BEFORE INSIDE HELP ME FUNCTION : " , unit)
    #     action , unit = self.gameBoard.path_finding(unit=unit , end_point=pos , bomb=10 ,help=True)
    #     print("AFTER INSIDE HELP ME FUNCTION : " , action , unit)
    #     return action , unit

    def move_bro(self, path , friendly_unit=False , last=False): #f_unit => FRIEND UNIT
        
        # D => H
        start = self.grid[self.id]#UNIT postion

        visited = []

        q = deque()
        q.append(start)
        start.is_visited = True

        while q:

            a = q.popleft()

            if a in path: 

                neibours = a.add_neibour(self.grid , move=True , friendly_unit=friendly_unit) #GET ALL EMPTY NODE  

                for i in neibours: 

                    # 135 -> 120, 136
                    if i.is_visited == False:
                        
                        q.append(i)
                            
                        i.is_visited = True
                        visited.append(i)

            else:
                break

        start.is_visited = False
        for i in visited:
            i.is_visited = False
        
        if a in path and not last:

            action , unit = self.move_bro( path , friendly_unit=True , last=True)
            
            return action , unit

        action , unit = self.gameBoard.path_finding(unit=self.unit_id , end_point=a.id , check=True)
        # action , unit = self.gameBoard.path_finding(unit=self.unit_id , end_point=self.goto[1] , check=True)

        return action , unit 



class node:

    def __init__(self, row, col):

        self.row = row
        self.col = col
        self.id = self.col + self.row * 15

    def board_reset(self, weight):

        # Type of This node i.e ENTITY type (Refer line : 53)
        self.obj_type = '.'

        self.bg = '.'

        self.player = None
        self.enemy = False

        self.in_safe = True

        self.weight = weight

        self.is_visited = False

        self.bombs = None
        self.hp = None
        self.expires = None
        self.blast_diameter = None
        self.invulnerability = 0
        self.bomb_x_and_y = None

        self.h_score = 0
        self.g_score = float("inf")
        self.f_score = float("inf")

    # def add_neibour(self , grid , evade=False  ):

    def add_neibour(self, grid, evade=False, atk=False , directed=False , diameter=None , move=False , fire=False , friendly_unit=False):

        # neibour = self.grid[eId].add_neibour(self.grid, evade=True, atk=True)

        if evade and atk:

            eNeigh = []

            if self.row > 0 and grid[self.id - 15].obj_type == '.' and grid[self.id - 15].player == None:  # UP
                eNeigh.append(grid[self.id - 15])

            if self.row < 14 and grid[self.id + 15].obj_type == '.' and grid[self.id + 15].player == None:  # DOWN
                eNeigh.append(grid[self.id + 15])

            if self.col > 0 and grid[self.id - 1].obj_type == '.' and grid[self.id - 1].player == None:  # LEFT
                eNeigh.append(grid[self.id - 1])

            if self.col < 14 and grid[self.id + 1].obj_type == '.' and grid[self.id + 1].player == None: # RIGHT
                eNeigh.append(grid[self.id + 1])

            return eNeigh

        elif fire:

            evade_neibours = []

            if self.row > 0 and (grid[self.id - 15].obj_type ==  '.' or  grid[self.id - 15].obj_type ==  'x'): #UP
                evade_neibours.append(grid[self.id - 15])

            if self.row < 14 and (grid[self.id + 15].obj_type ==  '.' or  grid[self.id + 15].obj_type ==  'x'): #DOWN
                evade_neibours.append(grid[self.id + 15])

            if self.col > 0 and (grid[self.id -1].obj_type ==  '.'  or grid[self.id - 1].obj_type ==  'x'): #LEFT
                evade_neibours.append(grid[self.id - 1])
            
            if self.col < 14 and (grid[self.id + 1].obj_type ==  '.' or  grid[self.id + 1].obj_type ==  'x'):#RIGHT
                evade_neibours.append(grid[self.id + 1])        
        
            return evade_neibours


        elif move:
            

            if not friendly_unit:
                
                evade_neibours = []
                
                if self.row > 0 and grid[self.id - 15].obj_type ==  '.' and  not grid[self.id - 15].player : #UP
                    evade_neibours.append(grid[self.id - 15])

                if self.row < 14 and grid[self.id + 15].obj_type ==  '.' and  not grid[self.id + 15].player : #DOWN
                    evade_neibours.append(grid[self.id + 15])

                if self.col > 0 and grid[self.id -1].obj_type ==  '.'  and  not grid[self.id - 1].player  : #LEFT
                    evade_neibours.append(grid[self.id - 1])
                
                if self.col < 14 and grid[self.id + 1].obj_type ==  '.' and  not grid[self.id + 1].player  : #RIGHT
                    evade_neibours.append(grid[self.id + 1])        
            
            else:
                
                evade_neibours = []

                if self.row > 0 and grid[self.id - 15].obj_type ==  '.'  and not grid[self.id - 15].enemy: #UP
                    evade_neibours.append(grid[self.id - 15])

                if self.row < 14 and grid[self.id + 15].obj_type ==  '.'  and not grid[self.id + 15].enemy: #DOWN
                    evade_neibours.append(grid[self.id + 15])

                if self.col > 0 and grid[self.id -1].obj_type ==  '.'  and not grid[self.id - 1].enemy: #LEFT
                    evade_neibours.append(grid[self.id - 1])
                
                if self.col < 14 and grid[self.id + 1].obj_type ==  '.' and not grid[self.id + 1].enemy: #RIGHT
                    evade_neibours.append(grid[self.id + 1])    


            return evade_neibours

        
        elif evade:
            
            evade_neibours = []
            

            if self.row > 0 and grid[self.id - 15].obj_type ==  '.' and  grid[self.id - 15].player == None: #UP
                evade_neibours.append(grid[self.id - 15])

            if self.row < 14 and grid[self.id + 15].obj_type ==  '.' and  grid[self.id + 15].player == None: #DOWN
                evade_neibours.append(grid[self.id + 15])

            if self.col > 0 and grid[self.id -1].obj_type ==  '.'  and  grid[self.id - 1].player == None: #LEFT
                evade_neibours.append(grid[self.id - 1])
            
            if self.col < 14 and grid[self.id + 1].obj_type ==  '.' and  grid[self.id + 1].player == None: #RIGHT
                evade_neibours.append(grid[self.id + 1])        
        
            return evade_neibours

        elif directed:
                
            u_id = d_id = l_id = r_id = self.id

            radius = (diameter - 1) // 2 # => 2

            # print("DIAMETER : ", diameter , "RADIUS : " , radius)

            up = down = left = right = radius 

            arun_list = []


            arun_list.append(grid[self.id])

            while grid[u_id].row > 0 and grid[u_id - 15].obj_type ==  '.' and up: #UP
                up -= 1
                arun_list.append(grid[u_id - 15])
                
                u_id -= 15
                

            while  grid[d_id].row < 14 and grid[d_id + 15].obj_type ==  '.' and down: #DOWN => 2
                down -= 1 # => 1
                arun_list.append(grid[d_id + 15]) # => 149
                
                d_id += 15
              

            while  grid[l_id].col > 0 and grid[l_id -1].obj_type ==  '.'  and left: #LEFT
                left -= 1
                arun_list.append(grid[l_id - 1])
                
                l_id -= 1

                
            while grid[r_id].col < 14 and grid[r_id + 1].obj_type ==  '.' and right: #RIGHT
                right -= 1
                arun_list.append(grid[r_id + 1])        
                
                r_id += 1 

            return arun_list 

        else:

            neibours = []
            
            if self.row > 0 and grid[self.id - 15].weight !=  float("inf") : #UP
                neibours.append(grid[self.id - 15])

            if self.row < 14 and grid[self.id + 15].weight !=  float("inf") : #DOWN
                neibours.append(grid[self.id + 15])

            if self.col > 0 and grid[self.id -1].weight !=  float("inf") : #LEFT
                neibours.append(grid[self.id - 1])
            
            if self.col < 14 and grid[self.id + 1].weight !=  float("inf") : #RIGHT
                neibours.append(grid[self.id + 1])        



            # if self.row > 0 and grid[self.id - 15].weight !=  float("inf") and not grid[self.id - 15].enemy: #UP
            #     neibours.append(grid[self.id - 15])

            # if self.row < 14 and grid[self.id + 15].weight !=  float("inf") and not grid[self.id + 15].enemy: #DOWN
            #     neibours.append(grid[self.id + 15])

            # if self.col > 0 and grid[self.id -1].weight !=  float("inf") and not grid[self.id -1].enemy: #LEFT
            #     neibours.append(grid[self.id - 1])
            
            # if self.col < 14 and grid[self.id + 1].weight !=  float("inf") and not grid[self.id + 1].enemy: #RIGHT
            #     neibours.append(grid[self.id + 1])        

            return neibours


class Gameboard:

    def __init__(self):
        self.bara = 1
        g = []
        for i in range(15):
            for j in range(15):
                g.append(node(i, j))

        self.grid = np.array(g)

        self.p = {
            'c': player(grid=self.grid, Gameboard=self, agent_id='a', unit_id='c', hp=3),
            'd': player(grid=self.grid, Gameboard=self, agent_id='b', unit_id='d', hp=3),
            'e': player(grid=self.grid, Gameboard=self, agent_id='a', unit_id='e', hp=3),
            'f': player(grid=self.grid, Gameboard=self, agent_id='b', unit_id='f', hp=3),
            'g': player(grid=self.grid, Gameboard=self, agent_id='a', unit_id='g', hp=3),
            'h': player(grid=self.grid, Gameboard=self, agent_id='b', unit_id='h', hp=3)
        }

        self.actions = ["up", "down", "left", "right", "bomb", "detonate"]

        self.weight = 0.1

        self.myTeam = []

        # MAJA FUNCTION i.e is convert col , row to row , col (want to know reason call us :)
        self.maja = lambda x: [14-x[1], x[0]]

        # RETUNS COL , ROW VALUE OR INVERSE MAJA FUNCTION #USE FOR BOMB DETONATION
        self.arun = lambda x: (x[1], 14-x[0])

        self.h = lambda start, end: abs(
            start.row - end.row) + abs(start.col - end.col)  # Herustic function

        self.linear_fucn = lambda l: l[1] + l[0] * 15

        self.inf_space = []

        self.currAtks = {}
        self.teamN = 0

        self.moniter = False

        self.bomb_spot = []

        self.bombs = []

        self.s = False

        # self.attack_spot = set()

        # self.bomb_is_here = lambda x : True if self.grid[self.p[x].id].obj_type == 'b' else False

    def render(self, game=False ,low=False ,inf=False , path_trace=False , path=None , atk=False , atk_spot=None):

        print()

        for i in range(225):
            if i % 15 == 0:
                print()

            if game:
                self.grid[i].bg = self.grid[i].obj_type 
            
            if inf:
                if self.grid[i].weight == float("inf"):
                
                    self.grid[i].bg = '*'
                else:
                    self.grid[i].bg = '.'
            
            if low:
                if self.grid[i].weight == 0.1:
                
                    self.grid[i].bg = '*'
                else:
                    self.grid[i].bg = '.'


            if atk:
                if self.grid[i] in atk_spot:
                    # print(" ATTACK NODES " , self.grid[i].id)
                    self.grid[i].bg = '#'
                
                else:
                    self.grid[i].bg = '.'


            if path_trace:
                

                if self.grid[i] in path:
                    self.grid[i].bg = '*'

                else:
                    self.grid[i].bg = '.'


            for j in self.p:
                
                # if self.p[j].id == i and not atk:
                if self.p[j].id == i and not path_trace:
                    self.grid[i].bg = j
         
            print(self.grid[i].bg , end=' ')
        
        print()

    def nodes_reset(self):

        for i in range(225):
            self.grid[i].board_reset(self.weight)

    def nearCen(self):
        pass

    # def update_board(self , gameState , tick_number=None): #Everytime the board get updated with current values
    # Everytime the board get updated with current values
    def update_board(self, gameState, tick_number=None, call=True):

        self.tick_number = tick_number

        self.eTeam = []

        self.bomb_loc = {
            'c': [],
            'd': [],
            'e': [],
            'f': [],
            'g': [],
            'h': []
        }

        self.ammo_found = False
        self.ammos = []

        self.power_up_found = False

        self.gameState = gameState
        # print(self.gameState)

        self.bombs = []
        self.fire = []

        self.nodes_reset()  # METHOD

        # print("MY TEAM MATES : " , self.myTeam)

        # ENTITIES i.e WOOD , STONE , METAL , BOMB , AMMO , FIRE , POWERUP => w , o , m , b , a , x , bp
        for i in self.gameState['entities']:

            x_ = self.maja([i['x'], i['y']])
            l_ = self.linear_fucn(x_)

            self.grid[l_].obj_type = i['type']

            if i['type'] == 'w':
                # self.grid[l_].weight = i['hp'] * 10
                self.grid[l_].weight = 10

            elif i['type'] == 'o':
                self.grid[l_].weight = i['hp'] * 30

            elif i['type'] == 'm':
                self.grid[l_].weight = float("inf")

            elif i['type'] == 'bp':

                self.grid[l_].weight = self.weight
                self.ammos.append(self.grid[l_])

                self.power_up_found = True
                self.power_up = l_
                self.grid[l_].expires = i['expires']

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

                self.bombs.append(self.grid[l_])

                self.bomb_loc[i["unit_id"]].append(self.grid[l_])

            elif i['type'] == 'x':

                self.grid[l_].weight = float("inf")

                self.fire.append(self.grid[l_])

        # BOTs
        # OPPONENT TEAM => c , e , g
        # OUR TEAM      => d , f , h
        # for i in self.total_players:
        for i in 'cdefgh':

            x_ = self.maja(self.gameState['unit_state'][i]['coordinates'])
            l_ = self.linear_fucn(x_)

            self.p[i].row = x_[0]
            self.p[i].col = x_[1]

            self.p[i].id = l_

            self.grid[l_].player = i

            self.p[i].hp = self.gameState['unit_state'][i]['hp']
            self.p[i].bombs = self.gameState['unit_state'][i]['inventory']['bombs']
            self.p[i].blast_diameter = self.gameState['unit_state'][i]['blast_diameter']
            self.p[i].invulnerable = self.gameState['unit_state'][i]['invulnerable']
            self.p[i].stunned = self.gameState['unit_state'][i]['stunned']

            if i in self.myTeam:

                if self.p[i].hp > 0:
                    self.grid[l_].weight = self.weight
                    # self.grid[l_].weight = float("inf")

                else:
                    self.grid[l_].weight = float("inf")

                # print(i , self.p[i].invulnerable , self.tick_number)
                if self.p[i].invulnerable >= self.tick_number:

                    for k in self.fire:

                        k.weight = self.weight
                        #CHANGES : FROM OBJ_TYPE 'x' TO '.'

            else:

                # self.grid[l_].weight = float("inf")
                self.grid[l_].weight = 0.1
                self.grid[l_].enemy = True

                if self.p[i].hp > 0:
                    self.eTeam.append(i)

                else:
                    self.grid[l_].weight = float("inf")
                    # self.grid[l_].obj_type = 'm'

            # print("UNIT ", i ,"UNIT CELL WEIGHT : " , self.grid[l_].weight)

        for i in self.inf_space:
            i.weight = float("inf")

        # if self.s:
        #     for i in self.bomb_spot:
        #         i.weight = float("inf")

        #     self.s = False

        # self.bomb_spot = []

        self.render(game=True)
        # self.render(low=True)

        # Team 7
        if tick_number < 2 and call and self.bara == 1:
            # - to find closer unit to center - KING
            lowCost = []

            for i in self.myTeam:
            
                temp = self.path_finding(
                    unit=i, end_point=self.p[i].center, team7=True)
                
                
                lowCost.append(temp)
            
            low = min(lowCost)
            
            d = dict(zip(lowCost, self.myTeam))
            
            self.p[d[low]].setRole('king')

            # - to find which enemy closer to which unit i.e 2nd unit - SOLDIER
            notAss = list()

            for i in self.myTeam:
                if not self.p[i].role:
            
                    notAss.append(i)
            
            print('Notass = ', notAss)
            
            if len(notAss) == 2:
            
                lowCost = list()
                d = dict()
                m = dict()
            
                for i in notAss:
                    for j in self.eTeam:
            
                        temp = self.path_finding(
                            unit=i, end_point=self.p[j].id, team7=True)
                        lowCost.append(temp)
            
                    m[min(lowCost)] = i
                    d[i] = dict(zip(lowCost, self.eTeam))
            
                    lowCost = list()
            
                print('mainD', d)
                print('m', m)

                minF = min(m.keys())
            
                print('minF', minF)

                self.p[m[minF]].updEn(d[m[minF]][minF])
                self.currAtks[d[m[minF]][minF]] = m[minF]
                self.p[m[minF]].setRole('soldier')

                self.currAtks[d[m[minF]][minF]] = m[minF]
            
                del d[m[minF]]

                # - Remaining unit - obstacle braker - FARMER
                for i in d.keys():
                    self.p[i].setRole('farmer')

        self.bara += 1

    def sort_ammo(self, unit):

        prior_list = [self.h(self.p[unit], i)
                      for i in self.ammos if self.h(self.p[unit], i) < 5 and i.obj_type == 'fp']
        if prior_list:
            ele = self.ammos.pop(prior_list.index(min(prior_list)))
            return ele.id
        return None

    def catch_spans(self, unit_id):

        if self.power_up_found:

            bp = self.sort_ammo(unit_id)
            print("POWERUP PRESENT SIR !!! ", bp)

            if bp != None:
                action, unit_id = self.path_finding(unit_id, bp)
            else:
                return None

        else:
            return None

        return action, unit_id


    def on_fire(self , unit):
        
        # print(" UNIT : " , unit , " UNIT ID : " , self.p[unit].id )

        start = self.grid[self.p[unit].id]

        # print(" START : " , start , " ID : " , start.id)

        if start.obj_type == 'x':
            
            visited = []

            q = deque()
            q.append(start)

            start.is_visited = True

            while q:

                a = q.popleft()

                if a.obj_type == 'x': 

                    neibours = a.add_neibour(self.grid , fire=True) #GET ALL EMPTY NODE  

                    for i in neibours: 
                        
                        if i.is_visited == False:
                            
                            q.append(i)
                                
                            i.is_visited = True
                            visited.append(i)

                else:
                    break


            start.is_visited = False
            for i in visited:
                i.is_visited = False

            return a.id
        
        return None


    def evalution(self, unit, bomb_blast) -> bool:

        for i in bomb_blast:
            # if i.player in self.myTeam and i.player != unit:
            if i.player in self.myTeam:
                return False

        return True

    def bomb_detonate(self, unit, fake=False):  # IF MY UNIT AREN'T THERE DETONATE

        if fake:
            self.bomb_loc[unit].append(self.grid[self.p[unit].id])

        this_bomb = self.bomb_loc[unit]  # LIST OF THAT UNIT

        for bomb in this_bomb:

            if abs(bomb.expires - self.tick_number) < 25:

                bomb_blast = bomb.add_neibour(
                    self.grid, directed=True, diameter=bomb.blast_diameter)  # RETURN LIST

                blast = self.evalution(unit, bomb_blast)  # RETURN BOOL

                if blast:

                    self.bomb_x_and_y = self.arun([bomb.row, bomb.col])

                    # if len(self.p[unit].goto) > 1:
                    #     self.p[unit].goto.pop()

                    self.p[unit].next_node(self.actions[5])

                    return self.actions[5], unit

        return None, unit

    # ALTERNATIVE EVADE FUNCTION
 
    def bomb_evade(self , unit=None , end_node=None , teamCheck=False) -> int: #IF RADIUS IS EQUAL TO 2 


        start = self.grid[self.p[unit].id]#UNIT postion
        
        safe_spot = None


        if end_node != None:
            
            # check = True
            safe_spot = start
            print(" FAKE BOMB " , end_node , start.id )
            b_ = self.grid[end_node]
            self.bombs.append(b_)
            # self.grid[end_node].blast_diameter = self.p[unit].blast_diameter #END NODE DIAMETER
            self.grid[end_node].blast_diameter = self.p[self.grid[end_node].player].blast_diameter #END NODE DIAMETER
            

        visited = []

        check = False

        # safe_spot = start

        self.attack_spot = set() #MAY BE I CAN GET THIS INFO FROM BOMB_DETONATE

        need_to_check = []

        for b in self.bombs:

            bomb = b

            if 2*self.h(b , self.p[unit]) - 3 < b.blast_diameter: 
                
                # print(" CHECK BOMB " , b.id)

                bomb_blast = bomb.add_neibour(self.grid , directed=True , diameter=bomb.blast_diameter) #RETURN LIST 

                need_to_check.append(b)

                # self.attack_spot.update(bomb_blast)

                check = True

            bomb_blast = bomb.add_neibour(self.grid , directed=True , diameter=bomb.blast_diameter) #RETURN LIST 

            self.attack_spot.update(bomb_blast)

        # print(" CHECK : " , check)
        # WE NEED TO MAINTAIN TWO SET 

        self.render(atk=True , atk_spot=self.attack_spot)

        # next_pos = [self.p['d'].next_node_pos , self.p['f'].next_node_pos , self.p['h'].next_node_pos ]
        next_pos = []
        for i in self.myTeam:
            if i != unit:
                next_pos.append(self.p[i].next_node_pos)


        print("NEXT POSITION : ", next_pos)


        # atk_hash = "".join(map(lambda x : str(x.id) , self.attack_spot))

        atk_hash = "".join(map(lambda x : str(x.id) , need_to_check))

        # atk_pos = " ".join(map(lambda x : str(x.id) , self.attack_spot))

        # print("ATTACK HASH " , atk_hash , " ATTACK SPOT : " , atk_pos)

        for i , j in self.p[unit].bomb_hash.items():
            print(" HASH ID : " , i)
            print(" HASH VALUE : " , j)

        try:

            atk = self.p[unit].bomb_hash[atk_hash]
            
            print(" INSIDE TRY ATK : ", atk )
            # if atk in self.attack_spot:
                # raise Exception(" GO FIND SAFE SPOT ")
            
            for i in self.attack_spot:
                if i.id == atk:
                    raise Exception(" GO FIND SAFE SPOT ")


            # elif atk == None:
            if atk == None:
                self.p[unit].goto[1] = 112
                return None

            else:
                self.p[unit].goto[1] = atk        
                return atk

        except:
            # pass
            self.p[unit].bomb_hash = {}

            # print(" INSIDE EXCEPTION ")
            if check:

                q = deque()
                q.append(start)

                start.is_visited = True
                # visited.append(start)

                while q:

                    a = q.popleft()

                    # if a in self.attack_spot and a.id not in next_pos : 
                    # if a in self.attack_spot and a in next_pos : 

                    # if a in self.attack_spot or a.id not in next_pos : 
                    if a in self.attack_spot or a.id in next_pos: 


                        neibours = a.add_neibour(self.grid , evade=True) #NEED TO CHECK WETHER ALL ARE INFINITY  

                        # self.attack_spot.add(a.id)
                    
                        for i in neibours: # => CHECK ALL NEIBOUR AND GIVE START AS SAFE SPOT
                            
                            # 135 -> 120, 136
                            if i.is_visited == False:
                                
                                q.append(i)
                                    
                                i.is_visited = True
                                visited.append(i)


                    else:
                        #2 CASES => HE MAY BE IN THE START POSITION ITSELF OR OTHER SPOT  
                        # safe_spot = a.id #MAY BE THE START POSITION OF THE UNIT #if start.id == a.id => None
                        safe_spot = a #MAY BE THE START POSITION OF THE UNIT #if start.id == a.id => None
                        print(" WHILE SAFE SPOT  ", safe_spot.id , " UNIT " , unit)
                        break

                start.is_visited = False
                for i in visited:
                    i.is_visited = False

                # self.safe_spot = safe_spot
                
                for i in self.attack_spot:
                    print(" ATTACK SPOT " , i.id)


                if safe_spot in self.attack_spot:

                    print(" SAFE SPOT " , safe_spot.id)
                    self.p[unit].bomb_hash[atk_hash] = None

                    return None

                if safe_spot == None:
                    print(" SAFE SPOT " , safe_spot)
                    self.p[unit].bomb_hash[atk_hash] = None

                    return None

                safe_spot = safe_spot.id
                self.p[unit].bomb_hash[atk_hash] = safe_spot
                return safe_spot
        


            # print(" SAFE SPOT : " , safe_spot , " UNIT " , unit)    

            return safe_spot
            # if safe_spot:
            #     print(" SAFE SPOT : " , safe_spot.id , " UNIT " , unit)    
            # else:
            #     print(" SAFE SPOT : " , safe_spot , " UNIT " , unit)     



    def can_i(self , unit) -> bool:

        fun = True

        for i in self.myTeam:

            print("in for loop : " ,i)
            # if i != unit:
            evade = self.bomb_evade( unit=i , end_node=self.p[unit].id)
            
            print(f" BOMBING : {i} RETURN {evade}" )
            if evade == None:
                fun =False

        return fun 
        

    # def take_action(self , came_from , current , start , end , unit , once_check=False):
    
    def take_action(self , came_from , current , start , end , unit ):
        
        # print("UNIT : " , self.p[unit].goto)
        
        # print(" INSIDE TAKE ACTION ", unit)
        path = []

        tot_cost = 0
        
        while current in came_from:
            current = came_from[current]
    
            if current != start:
                path.append(current)
                tot_cost += current.weight

        path.insert(0 , end)
        n = path[len(path)-1]

        print(" NEXT NODE DETAIL : " , unit , n.id , n.player , n.weight)
        # for i in path:
            # print(i.id)
        # self.render(inf=True)
        self.render(path_trace=True , path=path)


        # try:
            # print(" TOTAL WEIGHT ", tot_cost , len(path))
        if True:
            if len(path) > 0:

                # print("UNIT ", unit , start.id)

                # if not self.p[unit].evade_loc:

                # if start.obj_type == 'b':
                    
                    # print(" BOMB IS HERE, RUN RA PANDA ") 
                #     id_ = self.bomb_evade(unit=unit , bomb=self.grid[self.p[unit].id])
                #     self.p[unit].goto.append(id_)

                #     # self.p[unit].evade_loc = True
                #     # self.p[unit].target_ammo.append(start)

                    # print(" ID " , id_)

                #     # action , unit = self.path_finding(unit=unit , end_point=self.p[unit].goto[-1] , check=True , once_check=True)
                #     action , unit = self.path_finding(unit=unit , end_point=self.p[unit].goto[-1] , check=True)
                    # return action , unit
                        
                    
                # self.actions = ["up", "down", "left", "right", "bomb", "detonate"]
                # if n.obj_type == 'x':

                    # print(unit , " => BOMB NEXT MOVE ")
                #     # # self.p[unit].next_node(unit , self.actions[4])
                #     # id_ = self.bomb_evade(unit=unit , bomb=n)
                #     # self.p[unit].goto.append(id_)
                #     # # return self.actions[3] , unit
                    # print(" ID " , id_)

                #     # action , unit = self.path_finding(unit=unit , end_point=self.p[unit].goto[-1] , check=True)
                    
                #     action = None
                #     return action , unit

                if n.player in self.eTeam:

                    print(" NEAR ENEMY " , n.player)
                    # print(unit , " => BOMB" , "END NODE : " , self.p[unit].id)

                    # evade = self.bomb_evade( unit=unit , end_node=self.p[unit].id)
                    # evade = self.bomb_evade( unit=unit , end_node=self.p[unit].id)
                    
                    # can_i = True

                    # for i in self.myTeam:

                    #     print("in for loop : " ,i)
                    #     # if i != unit:
                    #     evade = self.bomb_evade( unit=i , end_node=self.p[unit].id)
                        
                    #     print(f" BOMBING : {i} RETURN {evade}" )
                    #     if evade == None:
                    #         can_i =False

                    # print( " CAN I  : " , can_i) 

                    # # if evade != None:
                    # if can_i:
                    if self.can_i(unit):

                        if len(self.inf_space) > 0:
                            self.inf_space = [] 

                        self.p[unit].next_node(self.actions[4] , unit)
                        return self.actions[4] , unit

                    else:
                        
                        n.weight = float("inf")
                        self.inf_space.append(n)
                        
                        action , unit = self.path_finding(unit=unit , end_point=self.p[unit].goto[-1] , check=True)
                        # action , unit = self.path_finding(unit=unit , end_point=self.p[unit].go , check=True)
                        
                        # action = None
                        self.p[unit].next_node(action , unit)
                        # self.render(inf=True)

                        # self.render(path_trace=True , path=path)
                        return action , unit

                elif n.player in self.myTeam and n.player != unit:

                    # print("PLAYER : " , n.id)

                    print(f" INSIDE MOVE ON BRO :  WHO IS IN : {unit} , FRIEND : {n.player} ")


                    action , unit = self.p[n.player].move_bro(path=path)

                    # self.p[f_unit].reserved_node = n.id
                    print(f" NOW WHO IS IN : {unit} , FRIEND : {n.player} , ACTION : {action} ")
                    
                    self.p[unit].next_node(action , unit)
                    return action , unit

                    # if len(path) > 1:
                        # print(" CALLED BY " , unit)
                    #     n2 = path[len(path)-2]
                    #     # n2 = path[-2]
                    #     return action , unit

                    # else:

                    #     action , unit = self.p[n.player].move_bro(start , to_node=None , told_by=n.player , single_Step=True)
                    #     return action , unit

                    # if len(path) > 1:
                        # print(" CALLED BY " , unit)
                    #     n2 = path[len(path)-2]
                    #     # n2 = path[-2]
                    #     action , unit = self.p[n.player].move_on(start , to_node=n2)
                    #     return action , unit

                    # else:

                    #     action , unit = self.p[n.player].move_on(start , to_node=None , told_by=n.player , single_Step=True)
                    #     return action , unit

                # elif n.id in self.attack_spot:
                #     return None , unit

                elif n.obj_type == 'w':

                    # print(unit , " => BOMB" , "END NODE : " , self.p[unit].id)

                    # evade = self.bomb_evade( unit=unit , end_node=self.p[unit].id)
                    # can_i = True
                    # for i in self.myTeam:
                    #     evade = self.bomb_evade( unit=i , end_node=self.p[unit].id)
                        
                    #     if evade == None:
                    #         can_i =False


                                    
                    # can_i = True

                    # for i in self.myTeam:

                    #     print("in for loop : " ,i)
                    #     # if i != unit:
                    #     evade = self.bomb_evade( unit=i , end_node=self.p[unit].id)
                        
                    #     print(f" BOMBING : {i} RETURN {evade}" )
                    #     if evade == None:
                    #         can_i =False

                    # print( " CAN I  : " , can_i) 


                    # print( " EVADE END NODE : " , evade)

                    # if evade != None:
                    # if can_i:
                    if self.can_i(unit):


                        if len(self.inf_space) > 0:
                            self.inf_space = []

                        self.p[unit].next_node(self.actions[4] , unit)
                        return self.actions[4] , unit

                    else:
                        
                        n.weight = float("inf")
                        self.inf_space.append(n)
                        
                        action , unit = self.path_finding(unit=unit , end_point=self.p[unit].goto[-1] , check=True)
                        # action , unit = self.path_finding(unit=unit , end_point=self.p[unit].go , check=True)
                        
                        # action = None
                        # self.p[unit].next_node(unit ,action)
                        self.p[unit].next_node(action , unit)

                        # self.render(inf=True)

                        # self.render(path_trace=True , path=path)
                        return action , unit

                
                elif n.obj_type == 'o':
                   
                    if self.can_i(unit):


                        if len(self.inf_space) > 0:
                            self.inf_space = []

                        self.p[unit].next_node(self.actions[4] , unit)

                        return self.actions[4] , unit

                    else:

                        
                        n.weight = float("inf")
                        self.inf_space.append(n)

                        action , unit = self.path_finding(unit=unit , end_point=self.p[unit].goto[-1] , check=True)

                        self.p[unit].next_node(action , unit)
                        
                        # self.render(inf=True)
                        # self.render(path_trace=True , path=path)

                        return action , unit
    
                elif n.id == start.id:
                    # print(unit , " => SAME SPOT")
                    self.p[unit].next_node(None)
                    return None , unit

                elif n.col > start.col: 
                    # print(unit , " => RIGTH  ", n.id)
                    self.p[unit].next_node(self.actions[3])
                    return self.actions[3] , unit

                elif n.col < start.col:

                    # print(unit , " => LEFT ", n.id)
                    self.p[unit].next_node(self.actions[2])
                    return self.actions[2] , unit

                elif n.row > start.row: 
                    # print(unit , " => DOWN ", n.id)
                    self.p[unit].next_node(self.actions[1])
                    return self.actions[1] , unit

                elif n.row < start.row: 
                    # print(unit , " => UP ", n.id)
                    self.p[unit].next_node(self.actions[0])
                    return self.actions[0] , unit
                
                else:
                    action = None
                    self.p[unit].next_node(action)

                    return action , unit
            else:

                # print("CAN'T REACH , Weight exceed priority")
                # print(" CALLING HELP ")

                self.p[unit].next_node(None)

                return None , unit

        # except Exception as e:

            print("ERROR IS : " , e)
            # return None , unit

    # def bomb_monitor(self):
    #     pass

    def path_finding(self, unit, end_point, check=False, team7=False , escape=False):


        if check:
            self.update_board(self.gameState, tick_number=self.tick_number)
            
            for i in self.inf_space:
                i.weight = float("inf")

        start = self.grid[self.p[unit].id]  # UNIT postion

        if end_point == None:
            print(" LIST EMPTY ")
            return None, unit

        if type(end_point) == list:
            end_point = self.linear_fucn(end_point)

        print(" END POINT ", end_point)
        end = self.grid[end_point]

        print(" END POINT ", end.id , " END POINT TYPE  " , end.obj_type , " END POINT WEIGHT ", end.weight , " CHECK " , check)


        # if end.weight == float("inf"):  # NEED TO ADD DIAGNOL NEIBOUR # USE WHILE
        if end.obj_type == 'm' or  end.obj_type == 'x' or end.obj_type == 'b' :  # NEED TO ADD DIAGNOL NEIBOUR # USE WHILE
            #CHANGED
            neibour = end.add_neibour(self.grid)
            #  = end.neibours
            h = 1000

            for i in neibour:

                print(" NEIBOUR : ", i.id , " TYPE  " , i.obj_type , " WEIGHT ", i.weight )

                j = self.h(start, i)
                if j < h:
                    h = j
                    end_node = i


            if len(neibour) > 0:
                end = end_node

            self.p[unit].goto[1] = end.id #CHANGES


            # self.p[unit].goto.pop()
            # self.p[unit].goto.append(end.id)

            # end = end_node
            # self.p[unit].goto.pop()
            # self.p[unit].goto.append(end.id)

        # print("END NODE " , end.id)
        # if start == end:
        #     pass

        path = {}

        count = 0
        if team7:
            self.update_board(
                self.gameState, tick_number=self.tick_number, call=False)

        start.f_score = self.h(start, end)
        start.g_score = 0

        open_set = PriorityQueue()
        open_set.put((start.f_score, count, start))
        open_set_hash = {start}

        while not open_set.empty():

            current = open_set.get()[2]
            # current = open_set.get()[2]

            if current == end:
                if team7:
                    cost7 = 0
                    while current in path:
                        current = path[current]
                        if current != start:
                            cost7 += current.f_score
                    return cost7

                action, unit_player = self.take_action(
                    came_from=path, current=current, start=start, end=end, unit=unit)

                return action, unit_player

            open_set_hash.remove(current)


            if not escape:
                
                neibours = current.add_neibour(self.grid)
            
            else:

                neibours = current.add_neibour(self.grid , move=True , friendly_unit=True)


            for neibour in neibours:

                temp_g_score = current.g_score + neibour.weight

                if temp_g_score < neibour.g_score:

                    path[neibour] = current
                    neibour.g_score = temp_g_score
                    neibour.f_score = temp_g_score + self.h(neibour, end)

                    if neibour not in open_set_hash:
                        count += 1
                        open_set.put((neibour.f_score, count,  neibour))
                        open_set_hash.add(neibour)

        print("CAN'T REACH", unit)
        # print(" UNIT " , unit , " ACTION " , action)
        return None, unit

    def AI(self, unit_id):

        # self.actions = ["up", "down", "left", "right", "bomb", "detonate"]

        # unit_id = 'd'
        # unit_id = 'f'
        # unit_id = 'h'
        # if self.tick_number < 200:
        #     self.p[unit_id].attack()

        evade = self.bomb_evade(unit=unit_id)

        escape = self.on_fire(unit=unit_id) #TODO: NEED TO CHECK 

        spawns = self.catch_spans(unit_id)

        print('**********', spawns)
        # IF MY UNIT AREN'T THERE DETONATE

        detonate_action, unit_id = self.bomb_detonate(unit_id)

        if escape != None: #TODO : NEED TO CHECK 

            action , unit_id = self.path_finding(unit=unit_id , end_point=escape)


        elif evade != None:

            print(" SAFE SPOT : " , self.p[unit_id].goto[1] , " UNIT : " , unit_id)

            for k in self.fire:

                k.weight = float("inf")
            
            self.p[unit_id].goto[1] = evade

            action , unit_id = self.path_finding(unit=unit_id , end_point=self.p[unit_id].goto[1] , escape=True)


            # if evade not in self.p[unit_id].goto:

            #     self.p[unit_id].goto.append(evade)

            # print(" DETONATE FUNCTION RETURN ")

            # if detonate_action != None:
            #     action = detonate_action

            # else:
            #     action, unit_id = self.path_finding(
            #         unit=unit_id, end_point=self.p[unit_id].goto[-1])

        elif spawns and self.p[unit_id].title != 'SOLDIER':
            action, unit_id = spawns

        else:

            for k in self.fire:
                k.weight = float("inf")

            # print(" DETONATE FUNCTION RETURN ")

            # if detonate_action != None:
            #     action = detonate_action

            # else:
            print('INSIDE ELSE PART ***')
            print('einfo ', unit_id, self.p[unit_id].eInfo)

            if self.p[unit_id].role:
                
                print('INSIDE ROLE ***', self.p[unit_id].title)
                
                action, unit_id = self.p[unit_id].role()
                
                print("Role assigned goin to ", action)

                # else:

                #     action = self.actions[4]

                # print(self.p[unit_id].eInfo['attack'])

                # if self.p[unit_id].eInfo['attack']:

                #     print("INSIDE tEAM MAIN ATTACK")
                #     action = self.actions[4]

                #     self.p[unit_id].goto[1] = 112

                # else:
                #     # print('SATTI THALAYA -=-7-7-7-7-7-7-7-7-7-7-77-')
                #     print('SATTI THALAYA ')
                #     # action, unit_id = self.path_finding(unit=unit_id, end_point=self.p[unit_id].goto[-1])
                #     action, unit_id = self.path_finding(unit=unit_id, end_point=self.p[unit_id].goto[1])
                #     # action, unit_id = self.path_finding(unit=unit_id, end_point=self.p[unit_id].center)

        for i in self.myTeam:
            if self.p[unit_id].next_node_pos == self.p[i].next_node_pos and i != unit_id:
                self.p[unit_id].next_node(None)

                action = None


        if detonate_action != None:
            action = detonate_action

        for k in self.fire:

            k.weight = float("inf")

        # if len(self.inf_space) > 0:
        self.inf_space = [] 


        print("ACTION : ", action, "UNIT : ", unit_id)

        return action, unit_id