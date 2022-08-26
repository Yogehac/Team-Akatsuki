import time
from curses import wrapper
import curses
import json
import random
import time


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
        self.actions = ['up', 'right', 'down', 'left']
        self.startTime = time.time()
        self.gameOver = False
        self.actionQueue = list()
        self.bombs = list()
        self.blasted = list()

    def makeUnits(self, units):
        d = {}
        teamA = list()
        teamB = list()
        for x in units:
            if x['agent_id'] == 'a':
                teamA.append(x['unit_id'])
            else:
                teamB.append(x['unit_id'])
            d[x['unit_id']] = x
        self.units = d
        self.teamA = teamA
        self.teamB = teamB

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

        elif action == 'bomb':
            info = self.units[unit]
            try:
                info['placed']
            except:
                if info['inventory']['bombs'] > 0:
                    info['inventory']['bombs'] -= 1
                    self.units[unit] = info

                    info['type'] = 'agent'
                    info['placed'] = {
                        'diameter': info['blast_diameter'],
                        'coordinates': [x, y],
                        'by': unit,
                        'time': time.time()
                    }

                    pos = y + x * 15
                    self.bombs.append(info['placed'])
                    self.Board[pos] = info
                    return [x, y]

        else:
            print('Cannot move')

    def agentA(self):
        units = self.teamA  # ['c', 'e', 'g']
        action = self.actions  # ['up', 'right', 'down', 'left']

        # action_space = (random.choice(action), random.choice(units))
        action_space = ('bomb', 'g')

        # parameter (action, unit)
        self.actionQueue.append(action_space)

    def agentB(self):
        units = self.teamB  # ['d', 'f', 'h']
        action = self.actions  # ['up', 'right', 'down', 'left']

        # action_space = (random.choice(action), random.choice(units))
        action_space = ('bomb', 'h')

        # # parameter (action, unit)
        self.actionQueue.append(action_space)

    def spanned(self, x, y):
        span = 10
        dSpan = 2
        x = x if x == 0 else x*dSpan
        y = abs(y-14)
        return [x+span, y+span]

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
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(11, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_WHITE)
        colors = {
            'w': curses.color_pair(2),
            'o': curses.color_pair(6),
            'm':  curses.color_pair(5),
            'a': curses.color_pair(7),
            'b': curses.color_pair(8),
            'bomb': curses.color_pair(10),
            'blast': curses.color_pair(11),
            'died': curses.color_pair(12)
        }

        def makeCBoard(d):
            for i in d:
                print(i['type'])
                if i['type'] == 'agent':
                    x, y = self.spanned(*i['coordinates'])
                    stdscr.addstr(y, x, i['unit_id']+'  ',
                                  colors[i['agent_id']] | curses.A_BOLD)
                elif i['type'] == 'agent_died':

                    x, y = self.spanned(*i['coordinates'])
                    stdscr.addstr(y, x, i['unit_id']+'  ', colors['died'])
                else:
                    x, y = self.spanned(i['x'], i['y'])
                    stdscr.addstr(y, x,  '  ', colors[i['type']])

            stdscr.refresh()

        def infoBoard():
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

        def mainBoard(s=''):
            newWin.clear()
            newWin.addstr(f'Bombardland Game\n\n{s}')

        def blast():
            for bomb in self.bombs:
                if time.time() >= bomb['time'] + 5:
                    x, y = bomb['coordinates']
                    d = {}
                    d['time'] = time.time()
                    d['pos'] = list()

                    cx, cy = self.spanned(x, y)
                    stdscr.addstr(cy, cx, '  ', colors['blast'])
                    pos = y + x * 15
                    d['pos'].append([x, y])
                    try:
                        print(self.Board[pos])
                        if self.Board[pos]['hp'] == 0:
                            if self.Board[pos]['type'] == 'agent':
                                self.Board[pos]['type'] == 'agent_died'
                                self.Board[pos]['hp'] -= 1
                            else:
                                self.Board.pop(pos)
                        else:
                            self.Board[pos]['hp'] -= 1
                    except:
                        pass

                    lx, ly = self.spanned(x-1, y)
                    stdscr.addstr(ly, lx, '  ', colors['blast'])
                    pos = y + (x-1) * 15
                    d['pos'].append([x-1, y])
                    try:
                        self.Board[pos]
                        if self.Board[pos]['hp']-1 <= 0:
                            if self.Board[pos]['type'] == 'agent':
                                self.Board[pos]['type'] == 'agent_died'
                                self.Board[pos]['hp'] -= 1
                            else:
                                self.Board.pop(pos)
                        else:
                            self.Board[pos]['hp'] -= 1
                    except:
                        pass

                    rx, ry = self.spanned(x+1, y)
                    stdscr.addstr(ry, rx, '  ', colors['blast'])
                    pos = y + (x+1) * 15
                    d['pos'].append([x+1, y])
                    try:
                        if self.Board[pos]['hp']-1 <= 0:
                            if self.Board[pos]['type'] == 'agent':
                                self.Board[pos]['type'] == 'agent_died'
                                self.Board[pos]['hp'] -= 1
                            else:
                                self.Board.pop(pos)
                        else:
                            self.Board[pos]['hp'] -= 1
                    except:
                        pass

                    ux, uy = self.spanned(x, y+1)
                    stdscr.addstr(uy, ux, '  ', colors['blast'])
                    pos = (y+1) + x * 15
                    d['pos'].append([x, y+1])
                    try:
                        if self.Board[pos]['hp']-1 <= 0:
                            if self.Board[pos]['type'] == 'agent':
                                self.Board[pos]['type'] == 'agent_died'
                                self.Board[pos]['hp'] -= 1
                            else:
                                self.Board.pop(pos)
                        else:
                            self.Board[pos]['hp'] -= 1
                    except:
                        pass

                    dx, dy = self.spanned(x, y-1)
                    stdscr.addstr(dy, dx, '  ', colors['blast'])
                    pos = (y-1) + x * 15
                    d['pos'].append([x, y-1])
                    try:
                        if self.Board[pos]['hp']-1 <= 0:
                            if self.Board[pos]['type'] == 'agent':
                                self.Board[pos]['type'] == 'agent_died'
                                self.Board[pos]['hp'] -= 1
                            else:
                                self.Board.pop(pos)
                        else:
                            self.Board[pos]['hp'] -= 1
                    except:
                        pass

                    self.blasted.append(d)
                    self.bombs.remove(bomb)
                    try:
                        self.Board[y + x * 15].pop('placed')
                    except:
                        pass

        def afterBlast():
            for x in self.blasted:
                if time.time() >= x['time'] + 1:
                    for y in x['pos']:
                        try:
                            self.Board[y[1] + y[0] * 15]
                        except:
                            a, b = self.spanned(*y)
                            stdscr.addstr(b, a,  '  ')

                    makeCBoard(self.Board.values())
                    self.blasted.remove(x)

        stdscr.clear()
        infoBoard()

        newWin = curses.newwin(5, 20, 2, 10)
        mainBoard()
        newWin.refresh()

        makeCBoard(self.Board.values())

        while not self.gameOver:

            self.agentA()
            self.agentB()
            actQueue = self.actionQueue
            blast()
            afterBlast()
            if len(actQueue) != 0:
                for i in actQueue:
                    time.sleep(0.1)
                    # print(self.bombs)
                    unit = i[1]
                    action = i[0]
                    m = self.move(unit, action)
                    if m:
                        # print(self.units[unit])
                        if action == 'bomb':
                            mainBoard(f'{unit} - bomb placed')
                            x, y = self.spanned(*m)
                            stdscr.addstr(y, x, unit + ' ', colors['bomb'])

                        else:
                            agId = m[4]
                            x, y = self.spanned(m[0], m[1])
                            nx, ny = self.spanned(m[2], m[3])
                            stdscr.addstr(y, x, '  ')
                            stdscr.addstr(
                                ny, nx, unit, colors[agId] | curses.A_BOLD)

                            mainBoard(f'{unit} - moved {action}')
                    else:
                        mainBoard(f'{unit} - Cannot move')

                    stdscr.refresh()
                    newWin.refresh()
                self.actionQueue = list()

            if time.time() >= self.startTime + 20:
                self.gameOver = True

        newWin.clear()
        newWin.addstr(f'Bombardland Game\n\nGAME OVER')
        newWin.refresh()

        print(self.units)
        stdscr.getch()


game = Engine('F:/Akatsuki/Team-Akatsuki/found0.json')
wrapper(game.main)
