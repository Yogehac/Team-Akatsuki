import json
from tabulate import tabulate
import time
import os
import random


def fg(text, color): return "\33[38;5;" + str(color) + "m" + text + "\33[0m"
def bg(text, color): return "\33[48;5;" + str(color) + "m" + text + "\33[0m"


class GameBoard:
    def __init__(self, path):
        self.gameJson = self.getJson(path)
        self.initialBoard()
        self.colCode = {
            'w': bg('  ', 88),
            'o': bg('  ', 11),
            'm': bg('  ', 243),
            'a': 226,
            'b': 199
        }
        self.makeBoard()

    def getJson(self, p):
        with open(p, 'r') as file:
            return json.load(file)

    def initialBoard(self):
        board = list()
        for _ in range(15):
            a = ['  ' for i in range(15)]
            board.append(a)
        self.Board = board

    def display(self, g=False):
        if g:
            print(tabulate(self.Board, tablefmt='fancy_grid'))
        else:
            for x in self.Board:
                for y in x:
                    print(y, end='')
                print()

    def fillUnits(self):
        for i in self.gameJson['units']:
            x, y = i['coordinates']
            self.Board[x][y] = fg(' {}'.format(
                i['unit_id']), self.colCode[i['agent_id']])

    def fillObs(self):
        for i in self.gameJson['entities']:
            x, y = i['x'], i['y']
            self.Board[x][y] = self.colCode[i['type']]

    def makeBoard(self):
        self.fillUnits()
        self.fillObs()


class Engine(GameBoard):
    def __init__(self, path):
        super().__init__(path)
        self.makeUnits(self.gameJson['units'])
        self.makeEntity(self.gameJson['entities'])

    def makeUnits(self, units):
        d = {}
        for x in units:
            d[x['unit_id']] = x
        self.units = d

    def makeEntity(self, entities):
        d = {}
        for i in entities:
            x, y = i['x'], i['y']
            d[y + x*15] = i
        self.entities = d

    def placeUnit(self, unit, o, n):
        unitInfo = self.units[unit]
        x, y = n
        xo, yo = o
        self.Board[x][y] = fg(' {}'.format(
            unit), self.colCode[unitInfo['agent_id']])
        self.Board[xo][yo] = '  '
        self.units[unit]['coordinates'] = n
        os.system('cls')
        self.display()

    def move(self, unit, action):
        x, y = self.units[unit]['coordinates']

        if action == 'up':
            nx = x-1
            if nx >= 0 and self.Board[nx][y] == '  ':
                self.placeUnit(unit, [x, y], [nx, y])
                print(f'Unit - {unit} - moved up ({nx}, {y})')
            else:
                print('Cannot move')

        elif action == 'down':
            nx = x+1
            if nx <= 14 and self.Board[nx][y] == '  ':
                self.placeUnit(unit, [x, y], [nx, y])
                print(f'Unit - {unit} - moved down ({nx}, {y})')
            else:
                print('Cannot move')

        elif action == 'left':
            ny = y-1
            if ny >= 0 and self.Board[x][ny] == '  ':
                self.placeUnit(unit, [x, y], [x, ny])
                print(f'Unit - {unit} - moved left ({x}, {ny})')
            else:
                print('Cannot move')

        elif action == 'right':
            ny = y+1
            if ny <= 14 and self.Board[x][ny] == '  ':
                self.placeUnit(unit, [x, y], [x, ny])
                print(f'Unit - {unit} - moved right ({x}, {ny})')
            else:
                print('Cannot move')

        else:
            print('UNKNOWN ACTION')

    def randomAct(self, max, unit=0):
        a = ['up', 'right', 'down', 'left']
        # Uncomment below to move all the units
        # Uncoment me and down too (comment 141 before running)
        # unit = list(self.units.keys())
        for _ in range(max):
            self.move(unit, random.choice(a))
            # self.move(random.choice(unit), random.choice(a))#im down , uncomment me
        print(self.units[unit])



game = Engine('F:/Akatsuki/Team-Akatsuki/found0.json')
game.display()
game.randomAct(100, 'c')
# game.randomAct(1000)

