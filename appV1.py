import time
from curses import wrapper
import curses
import json
import random
from turtle import color


class GameBoard:
    def __init__(self, path):
        self.gameJson = self.getJson(path)
        self.initialBoard()

    def getJson(self, p):
        with open(p, 'r') as file:
            return json.load(file)

    def initialBoard(self):
        board = dict()

        for x in self.gameJson['units']:
            id = x['coordinates'][1] + x['coordinates'][0] * 15
            board[id] = x
            board[id]['type'] = 'agent'

        for y in self.gameJson['entities']:
            id = y['y'] + y['x'] * 15
            board[id] = y

        self.Board = board


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

    def move(self, unit, action):
        x, y = self.units[unit]['coordinates']
        if action == 'up' and x-1 >= 0:
            nx = x-1
            nPos = y + (nx) * 15
            try:
                self.Board[nPos]
                print('Not vacant')
                return False
            except:
                pos = y + x * 15
                self.Board[nPos] = self.Board[pos]
                self.Board.pop(pos)
                self.units[unit]['coordinates'] = [nx, y]
                print(f'Unit - {unit} - moved up ({nx}, {y})')
                return [x, y, nx, y, self.Board[nPos]['agent_id']]

        elif action == 'down' and x+1 <= 14:
            nx = x+1
            nPos = y + (nx) * 15
            try:
                self.Board[nPos]
                print('Not vacant')
                return False
            except:
                pos = y + x * 15
                self.Board[nPos] = self.Board[pos]
                self.Board.pop(pos)
                self.units[unit]['coordinates'] = [nx, y]
                print(f'Unit - {unit} - moved up ({nx}, {y})')
                return [x, y, nx, y, self.Board[nPos]['agent_id']]

        elif action == 'right' and y+1 <= 14:
            ny = y+1
            nPos = ny + x * 15
            try:
                self.Board[nPos]
                print('Not vacant')
                return False
            except:
                pos = y + x * 15
                self.Board[nPos] = self.Board[pos]
                self.Board.pop(pos)
                self.units[unit]['coordinates'] = [x, ny]
                print(f'Unit - {unit} - moved up ({x}, {ny})')
                return [x, y, x, ny, self.Board[nPos]['agent_id']]

        elif action == 'left' and y-1 >= 0:
            ny = y-1
            nPos = ny + x * 15
            try:
                self.Board[nPos]
                print('Not vacant')
                return False
            except:
                pos = y + x * 15
                self.Board[nPos] = self.Board[pos]
                self.Board.pop(pos)
                self.units[unit]['coordinates'] = [x, ny]
                print(f'Unit - {unit} - moved up ({x}, {ny})')
                return [x, y, x, ny, self.Board[nPos]['agent_id']]

        else:
            print('Cannot move')

    def main(self, stdscr):
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)

        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_GREEN)
        colors = {
            'w': curses.color_pair(2),
            'o': curses.color_pair(6),
            'm':  curses.color_pair(5),
            'a': curses.color_pair(7),
            'b': curses.color_pair(8),
            'bomb': curses.color_pair(10)
        }

        stdscr.clear()
        yAxix = 70
        stdscr.addstr(2, yAxix, 'Information')
        stdscr.addstr(4, yAxix, '  ', colors['w'])
        stdscr.addstr(4, yAxix+5, 'WOOD')
        stdscr.addstr(6, yAxix, '  ', colors['o'])
        stdscr.addstr(6, yAxix+5, 'STONE')
        stdscr.addstr(8, yAxix, '  ', colors['m'])
        stdscr.addstr(8, yAxix+5, 'METAL')
        stdscr.addstr(10, yAxix, 'a', colors['a'])
        stdscr.addstr(10, yAxix+5, 'Team A')
        stdscr.addstr(12, yAxix, 'b', colors['b'])
        stdscr.addstr(12, yAxix+5, 'Team B')
        stdscr.refresh()

        newWin = curses.newwin(5, 20, 2, 10)
        newWin.addstr('Bombardland Game')
        newWin.refresh()

        span = 10
        dSpan = 2
        for i in self.Board.values():
            if i['type'] == 'agent':
                x, y = i['coordinates']
                x = x if x == 0 else x*dSpan
                y = abs(y-14)
                stdscr.addstr(y+span, x+span, i['unit_id'],
                              colors[i['agent_id']] | curses.A_BOLD)
            else:
                x, y = i['x'], i['y']
                x = x if x == 0 else x*dSpan
                y = abs(y-14)
                stdscr.addstr(y+span, x+span,  '  ', colors[i['type']])

            stdscr.refresh()

        a = ['up', 'right', 'down', 'left']
        un = list(self.units.keys())
        for i in range(100):
            # time.sleep(0.1)
            unit = random.choice(un)
            action = random.choice(a)
            # unit = stdscr.getkey()

            # unit = 'e'
            # action = 'down'
            m = self.move(unit, action)
            if m:
                x, y, nx, ny, agId = m
                x = x if x == 0 else x*dSpan
                nx = nx if nx == 0 else nx*dSpan
                y, ny = abs(y-14), abs(ny-14)
                stdscr.addstr(y+span, x+span, ' b', colors['bomb'])
                stdscr.addstr(ny+span, nx+span,  unit,
                              colors[agId] | curses.A_BOLD)
                stdscr.refresh()

                newWin.clear()
                newWin.addstr(f'Bombardland Game\n\n{unit} - moved {action}')
                newWin.refresh()
            else:
                newWin.clear()
                newWin.addstr(f'Bombardland Game\n\n{unit} - Cannot move')
                newWin.refresh()
        print(self.units)
        stdscr.getch()


game = Engine('F:/Akatsuki/Team-Akatsuki/found0.json')
# game.randomAct(1000, 'h')
# game.randomAct(1000)


wrapper(game.main)
# time.sleep(0.5)
# game.move('d', 'up')
