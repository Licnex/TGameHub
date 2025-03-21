import time
import os
import random
import curses
import getInput
from bullets import Bullet
from boss import Boss
from spring import Spring
from enemy import Enemy
from smartEnemy import SmartEnemy
from bridge import Bridge

def clear_terminal():
    """Clear terminal in a cross-platform way."""
    os.system('cls' if os.name == 'nt' else 'clear')

class Board:
    def __init__(self):
        self.width = 1400
        self.screenWidth = 170
        self.height = 45
        self.grid = [[' ' for i in range(self.width)]
                     for j in range(self.height)]
        # Use the cross-platform getInput; make sure _GetCh is defined accordingly in getInput.py.
        self.getch = getInput._GetCh()
        self.bricks = []
        self.enemies = []
        self.smartEnemies = []
        self.bullets = []
        self.bridge = Bridge()
        self.boss = Boss()
        self.coins = []
        self.bossBullets = []
        self.springs = []
        # Note: color info is now handled by curses color pairs.
        # You may choose to map these ANSI codes to curses color pairs in your Engine.
        self.black = 1
        self.red = 2
        self.green = 3
        self.yellow = 4
        self.blue = 5
        self.magenta = 6
        self.cyan = 7
        self.white = 8

    def render(self, engine):
        """Use curses to update the window."""
        win = engine.win  # engine.win should be set from curses.wrapper
        # Process springs (check collisions)
        for spring in self.springs:
            if spring.posX in range(engine.gridX, engine.gridX + self.screenWidth):
                spring.checkCollision(engine)

        self.updateEnemies(engine)
        self.updateBullets(engine)
        
        # Update bridge position if onscreen
        k = engine.gridX + engine.mario.legsMaxX
        if 480 <= k <= 690:
            if time.time() - self.bridge.updTime > 0.09:
                self.bridge.updatePos(engine)

        # Update Boss if onscreen
        if engine.gridX + engine.mario.legsMaxX >= 1270:
            if time.time() - self.boss.updTime1 >= 2:
                self.bullets.append(Bullet('<', self.boss.posX - 2, self.boss.posY + 5, time.time(), -1))
                self.boss.updTime1 = time.time()
            if time.time() - self.boss.updTime >= 1:
                x, y = self.boss.posX, self.boss.posY
                self.eraseBoss(x, y)
                self.boss.updatePos()
                self.boss.updTime = time.time()
            self.placeBoss(engine)

        # Place Mario and get a temporary grid representation.
        tmp_grid = self.placeMario(engine)
        if not tmp_grid:
            return False

        # Clear the curses window.
        win.clear()

        # Build a header string with stats.
        header = (' ' * 10) + 'SCORE : {}'.format(engine.score) + ' ' * 10 + \
                 'COINS COLLECTED : {}'.format(engine.coins) + ' ' * 10 + \
                 'TIME LEFT = {}'.format(engine.lefTime) + ' ' * 10 + \
                 'LIVES REMAINING : {}'.format(engine.lives) + ' ' * 10 + \
                 'BOSS LIVES : {}'.format(self.boss.lives)
        try:
            # You can set the color attribute if you initialize color pairs in your Engine.
            win.addstr(0, 0, header, curses.color_pair(self.red))
        except curses.error:
            pass

        # Render the temporary grid rows starting from line 2.
        for idx, row in enumerate(tmp_grid):
            try:
                win.addstr(idx + 2, 0, ''.join(row))
            except curses.error:
                pass  # prevents crashing on small terminals

        win.refresh()
        return True
    def createBase(self):
        # Create the ground base.
        for i in range(self.width):
            self.grid[self.height - self.height // 5][i] = self.yellow + '#' + self.reset
        for i in range(1 + self.height - self.height // 5, self.height):
            if i % 2:
                for j in range(self.width):
                    if j % 6 == 0:
                        self.grid[i][j] = self.yellow + '|' + self.reset
                    else:
                        self.grid[i][j] = ' '
            else:
                for j in range(self.width):
                    self.grid[i][j] = self.yellow + '-' + self.reset

    def createMountain(self, top, mheight, x, gap):
        l = x - 1
        for i in range(top, self.height - self.height // 5):
            self.grid[i][l] = self.magenta + '/' + self.reset
            self.grid[i][l + gap] = self.magenta + '\\' + self.reset
            l -= 1
            gap += 2

    def createCloud(self, bottom, lft):
        for i in range(lft + 6, lft + 10):
            self.grid[bottom - 2][i] = self.cyan + '_' + self.reset
        self.grid[bottom - 1][lft + 10] = self.cyan + ')' + self.reset
        for i in range(lft, lft + 5):
            self.grid[bottom - 1][i] = self.cyan + '_' + self.reset
        for i in range(lft + 11, lft + 15):
            self.grid[bottom - 1][i] = self.cyan + '_' + self.reset
        self.grid[bottom - 1][lft + 5] = self.cyan + '(' + self.reset
        self.grid[bottom][lft - 1] = self.cyan + '(' + self.reset
        for i in range(lft, lft + 15):
            self.grid[bottom][i] = self.cyan + '_' + self.reset
        self.grid[bottom][lft + 15] = self.cyan + ')' + self.reset

    def createPit(self, x, w):
        for i in range(self.height - self.height // 5, self.height - self.height // 5 + 3):
            for j in range(w):
                self.grid[i][x + j] = ' '
        for i in range(self.height - self.height // 5 + 3, self.height):
            for j in range(w):
                self.grid[i][x + j] = self.cyan + '~' + self.reset

    def createPipes(self, x, w, h):
        for i in range(self.height - self.height // 5 - h, self.height - self.height // 5):
            for j in range(w):
                self.grid[i][x + j] = self.green + '#' + self.reset

    def createBricks(self, c, x, y):
        for i in range(y, y + 3):
            for j in range(x, x + 5):
                self.grid[i][j] = c

    def createStairs(self, x, y, w, h, f):
        if f:
            for i in range(w, 0, -1):
                tx = x
                for j in range(i):
                    self.createBricks(self.green + '#' + self.reset, tx, y)
                    tx += 5
                x += 5
                y -= 3
        else:
            for i in range(w, 0, -1):
                tx = x
                for j in range(i):
                    self.createBricks(self.green + '#' + self.reset, tx, y)
                    tx += 5
                y -= 3

    def createCoins(self, x, y):
        self.grid[y][x] = 'C'
        self.grid[y][x + 1] = 'C'
        self.grid[y][x + 2] = 'C'

    def changeBrick(self, c, a, b):
        X, Y, f = -1, -1, False
        for i in self.bricks:
            if f:
                break
            x, y, f = i[1], i[2], False
            for j in range(y, y + 3):
                if f:
                    break
                if j != a:
                    continue
                for k in range(x, x + 5):
                    if f:
                        break
                    if k != b:
                        continue
                    f = True
                    X, Y = x, y
        self.bricks.remove([c, X, Y])
        if c == self.red + '3' + self.reset:
            c = self.red + '2' + self.reset
        elif c == self.red + '0' + self.reset:
            c = ' '
        elif c == self.red + '1' + self.reset:
            c = self.red + '0' + self.reset
        elif c == self.red + '2' + self.reset:
            c = self.red + '1' + self.reset
        self.createBricks(c, X, Y)
        self.bricks.append([c, X, Y])

    def removeCoins(self, engine, x, y):
        for i in self.coins:
            if i[1] == y:
                if x in list(range(i[0], i[0] + 3)):
                    os.system('aplay ./sounds/mtc.wav > /dev/null 2>&1 &')
                    for j in range(3):
                        self.grid[y][i[0] + j] = ' '
                    self.coins.remove(i)
                    engine.coins += 1
                    break

    def removeEnemy(self, x, y):
        for i in self.enemies:
            if i.posY == y:
                if x in (i.posX, i.posX + 1, i.posX + 2):
                    self.grid[y][i.posX:(i.posX + 3)] = '   '
                    self.enemies.remove(i)
                    os.system('aplay ./sounds/uki.wav > /dev/null 2>&1 &')
                    break
        for i in self.smartEnemies:
            if i.posY == y:
                if x in (i.posX, i.posX + 1, i.posX + 2):
                    self.grid[y][i.posX:(i.posX + 3)] = '   '
                    self.smartEnemies.remove(i)
                    os.system('aplay ./sounds/uki.wav > /dev/null 2>&1 &')
                    break

    def removeBullet(self, x, y):
        for i in self.bullets:
            if i.posX == x and i.posY == y:
                self.bullets.remove(i)
                os.system('aplay ./sounds/bhe.wav > /dev/null 2>&1 &')
                break

    def createBridge(self):
        self.grid[self.bridge.posY][self.bridge.posX:(self.bridge.posX + self.bridge.length)] = self.bridge.s

    def createSpring(self, spring):
        for i in range(spring.height):
            self.grid[spring.posY + i][spring.posX:(len(spring.body[i]) + spring.posX)] = spring.body[i]

    def createCastle(self):
        for i in range(28, 30):
            for j in range(1350, 1378):
                self.grid[i][j] = self.green + '#' + self.reset
        for i in range(30, 36):
            for j in range(1350, 1360):
                self.grid[i][j] = self.green + '#' + self.reset
        for i in range(30, 36):
            for j in range(1368, 1378):
                self.grid[i][j] = self.green + '#' + self.reset
        for i in range(25, 28):
            for j in range(1352, 1356):
                self.grid[i][j] = self.cyan + '#' + self.reset
        for i in range(25, 28):
            for j in range(1372, 1376):
                self.grid[i][j] = self.cyan + '#' + self.reset
        for i in range(24, 28):
            for j in range(1359, 1369):
                self.grid[i][j] = self.red + '#' + self.reset

    def createBackground(self):
        '''Generate ground'''
        self.createBase()
        '''Generate clouds'''
        x = 60
        y = 6
        while x < self.width:
            self.createCloud(4 + y, x)
            x += 50
            y = (y + 3) % 6
        '''Generate mountains'''
        self.createMountain(28, 6, 30, 1)
        self.createMountain(28, 6, 405, 1)
        self.createMountain(28, 6, 490, 1)
        self.createMountain(28, 6, 550, 1)
        self.createMountain(28, 6, 650, 1)
        self.createMountain(28, 6, 960, 1)
        self.createMountain(28, 6, 1055, 1)
        '''Generate bricks'''
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 130, 25)
        self.bricks.append([c, 130, 25])
        self.createBricks(self.green + '#' + self.reset, 150, 25)
        self.bricks.append([self.green + '#' + self.reset, 150, 25])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 155, 25)
        self.bricks.append([c, 155, 25])
        self.createBricks(self.green + '#' + self.reset, 160, 25)
        self.bricks.append([self.green + '#' + self.reset, 160, 25])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 165, 25)
        self.bricks.append([c, 165, 25])
        self.createBricks(self.green + '#' + self.reset, 170, 25)
        self.bricks.append([self.green + '#' + self.reset, 170, 25])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 160, 10)
        self.bricks.append([c, 160, 10])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 520, 24)
        self.bricks.append([c, 520, 24])
        self.createBricks(self.green + '#' + self.reset, 525, 24)
        self.bricks.append([self.green + '#' + self.reset, 525, 24])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 530, 24)
        self.bricks.append([c, 530, 24])
        for i in range(500, 560, 5):
            self.createBricks(self.green + '#' + self.reset, i, 10)
            self.bricks.append([self.green + '#' + self.reset, i, 10])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 660, 25)
        self.bricks.append([c, 660, 25])
        self.createBricks(self.green + '#' + self.reset, 705, 25)
        self.bricks.append([self.green + '#' + self.reset, 705, 25])
        self.createBricks(self.green + '#' + self.reset, 710, 25)
        self.bricks.append([self.green + '#' + self.reset, 710, 25])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 760, 25)
        self.bricks.append([c, 760, 25])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 770, 25)
        self.bricks.append([c, 770, 25])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 780, 25)
        self.bricks.append([c, 780, 25])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 770, 10)
        self.bricks.append([c, 770, 10])
        self.createBricks(self.green + '#' + self.reset, 810, 25)
        self.bricks.append([self.green + '#' + self.reset, 810, 25])
        self.createBricks(self.green + '#' + self.reset, 825, 10)
        self.bricks.append([self.green + '#' + self.reset, 825, 10])
        self.createBricks(self.green + '#' + self.reset, 830, 10)
        self.bricks.append([self.green + '#' + self.reset, 830, 10])
        self.createBricks(self.green + '#' + self.reset, 835, 10)
        self.bricks.append([self.green + '#' + self.reset, 835, 10])
        self.createBricks(self.green + '#' + self.reset, 855, 10)
        self.bricks.append([self.green + '#' + self.reset, 855, 10])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 860, 10)
        self.bricks.append([c, 860, 10])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 865, 10)
        self.bricks.append([c, 865, 10])
        self.createBricks(self.green + '#' + self.reset, 870, 10)
        self.bricks.append([self.green + '#' + self.reset, 870, 10])
        self.createBricks(self.green + '#' + self.reset, 860, 24)
        self.bricks.append([self.green + '#' + self.reset, 860, 24])
        self.createBricks(self.green + '#' + self.reset, 865, 24)
        self.bricks.append([self.green + '#' + self.reset, 865, 24])
        self.createBricks(self.green + '#' + self.reset, 1100, 24)
        self.bricks.append([self.green + '#' + self.reset, 1100, 24])
        self.createBricks(self.green + '#' + self.reset, 1105, 24)
        self.bricks.append([self.green + '#' + self.reset, 1105, 24])
        self.createBricks(self.green + '#' + self.reset, 1110, 24)
        self.bricks.append([self.green + '#' + self.reset, 1110, 24])
        c = random.choice([self.red + '1' + self.reset, self.red + '2' + self.reset, self.red + '3' + self.reset])
        self.createBricks(c, 1115, 24)
        self.bricks.append([c, 1115, 24])
        self.createBricks(self.green + '#' + self.reset, 1120, 24)
        self.bricks.append([self.green + '#' + self.reset, 1120, 24])
        '''Generate pipes'''
        self.createPipes(185, 13, 6)
        self.createPipes(250, 13, 8)
        self.createPipes(310, 13, 12)
        self.createPipes(370, 13, 12)
        self.createPipes(1070, 13, 6)
        self.createPipes(1200, 13, 6)
        '''Generate pits'''
        self.createPit(440, 40)
        self.createPit(580, 30)
        self.createPit(1005, 18)
        '''Generate stairs'''
        self.createStairs(890, 33, 4, 4, 1)
        self.createStairs(920, 33, 4, 4, 0)
        self.createStairs(980, 33, 5, 5, 1)
        self.createStairs(1023, 33, 4, 4, 0)
        self.createStairs(1230, 33, 7, 7, 1)
        '''Generate enemies'''
        self.enemies.append(Enemy('(E)', 180, 30, time.time()))
        self.enemies.append(Enemy('(E)', 263, 25, time.time()))
        self.enemies.append(Enemy('(E)', 330, 26, time.time()))
        self.enemies.append(Enemy('(E)', 365, 23, time.time()))
        self.enemies.append(Enemy('(E)', 530, 33, time.time()))
        self.smartEnemies.append(SmartEnemy('(E)', 694, 33, time.time()))
        self.smartEnemies.append(SmartEnemy('(E)', 780, 30, time.time()))
        self.enemies.append(Enemy('(E)', 850, 30, time.time()))
        self.enemies.append(Enemy('(E)', 975, 30, time.time()))
        self.enemies.append(Enemy('(E)', 950, 33, time.time()))
        self.enemies.append(Enemy('(E)', 1096, 33, time.time()))
        self.smartEnemies.append(SmartEnemy('(E)', 100, 20, time.time()))
        '''Generate coins'''
        self.createCoins(90, 33)
        self.coins.append([90, 33])
        self.createCoins(190, 27)
        self.coins.append([190, 27])
        for i in range(280, 300, 5):
            self.createCoins(i, 33)
            self.coins.append([i, 33])
        self.createCoins(420, 33)
        self.coins.append([420, 33])
        self.createCoins(525, 20)
        self.coins.append([525, 20])
        self.createCoins(570, 20)
        self.coins.append([570, 20])
        for i in range(730, 750, 5):
            self.createCoins(i, 20)
            self.coins.append([i, 20])
        for i in range(1160, 1180, 5):
            self.createCoins(i, 25)
            self.coins.append([i, 25])
        '''Generate bridge'''
        self.createBridge()
        '''Generate boundary'''
        for i in range(self.height):
            self.grid[i][self.width - 1] = '#'
        '''Generate spring'''
        self.springs.append(Spring(5, 430, 31))
        for i in self.springs:
            self.createSpring(i)
        '''Draw castle'''
        self.createCastle()

    def updateEnemies(self, engine):
        for i in self.enemies:
            if engine.gridX <= i.posX <= engine.gridX + self.screenWidth:
                if time.time() - i.updTime >= 0.2:
                    i.updatePos(self.grid)
                    i.updTime = time.time()
        for i in self.smartEnemies:
            if engine.gridX <= i.posX <= engine.gridX + self.screenWidth:
                if time.time() - i.updTime >= 0.2:
                    i.findMario(engine)
                    i.updTime = time.time()

    def updateBullets(self, engine):
        for i in self.bullets:
            if time.time() - i.updTime >= 0.1:
                i.updatePos(engine)
                i.updTime = time.time()
                if i.posX >= self.width - 2:
                    self.grid[i.posY][i.posX] = ' '
                    self.bullets.remove(i)

    def placeMario(self, engine):
        '''Copying a section of the original grid to temporary grid'''
        tmp_grid = []
        for i in range(self.height):
            s = []
            for j in self.grid[i][engine.gridX:(engine.gridX + self.screenWidth)]:
                s.append(str(j))
            tmp_grid.append(s)
        '''Place Mario's head'''
        for i in range(engine.mario.headMinX, engine.mario.headMaxX + 1):
            if tmp_grid[engine.mario.headY][i] == '<':
                self.grid[engine.mario.headY][i + engine.gridX] = ' '
                engine.lives -= 1
                self.removeBullet(i + engine.gridX, engine.mario.headY)
            tmp_grid[engine.mario.headY][i] = engine.mario.head[i - engine.mario.headMinX]
        '''Place Mario's neck'''
        for i in range(engine.mario.neckMinX, engine.mario.neckMaxX + 1):
            if tmp_grid[engine.mario.neckY][i] == '<':
                self.grid[engine.mario.neckY][i + engine.gridX] = ' '
                engine.lives -= 1
                self.removeBullet(i + engine.gridX, engine.mario.neckY)
            tmp_grid[engine.mario.neckY][i] = engine.mario.neck[i - engine.mario.neckMinX]
        '''Place Mario's middle body'''
        for i in engine.mario.bodyYs:
            for j in range(engine.mario.bodyMinX, engine.mario.bodyMaxX + 1):
                if tmp_grid[i][j] == self.green + '#' + self.reset:
                    return False
                if tmp_grid[i][j] == '#':
                    return False
                if tmp_grid[i][j] == '(':
                    if tmp_grid[i][j + 1] == 'E':
                        engine.lives -= 1
                        engine.mario.newLife(engine)
                        engine.gridX = 0
                if tmp_grid[i][j] == 'C':
                    self.removeCoins(engine, j + engine.gridX, i)
                if tmp_grid[i][j] == '<':
                    self.grid[i][j + engine.gridX] = ' '
                    engine.lives -= 1
                    self.removeBullet(j + engine.gridX, i)
                tmp_grid[i][j] = engine.mario.body[j - engine.mario.bodyMinX]
        '''Place Mario's bottom body'''
        for i in range(engine.mario.bottomMinX, engine.mario.bottomMaxX + 1):
            if tmp_grid[engine.mario.bottomY][i] == '<':
                self.grid[engine.mario.bottomY][i + engine.gridX] = ' '
                engine.lives -= 1
                self.removeBullet(i + engine.gridX, engine.mario.bottomY)
            tmp_grid[engine.mario.bottomY][i] = engine.mario.bottom[i - engine.mario.bottomMinX]
        '''Place Mario's legs'''
        for i in range(engine.mario.legsMinX, engine.mario.legsMaxX + 1):
            if tmp_grid[engine.mario.legsY][i] == '<':
                self.grid[engine.mario.legsY][i + engine.gridX] = ' '
                engine.lives -= 1
                self.removeBullet(i + engine.gridX, engine.mario.legsY)
            tmp_grid[engine.mario.legsY][i] = engine.mario.legs[i - engine.mario.legsMinX]
        return tmp_grid

    def placeBoss(self, engine):
        self.grid[self.boss.posY][self.boss.posX:(self.boss.posX + 5)] = self.boss.head
        for i in range(1, 9):
            self.grid[self.boss.posY + i][self.boss.posX + 2] = self.boss.body[i - 1]
        self.grid[self.boss.posY + 4][self.boss.posX + 1] = '/'
        self.grid[self.boss.posY + 4][self.boss.posX + 3] = '\\'

    def eraseBoss(self, x, y):
        self.grid[y][x:(x + 5)] = '     '
        for i in range(1, 9):
            self.grid[y + i][x + 2] = ' '
        self.grid[y + 4][x + 1] = ' '
        self.grid[y + 4][x + 3] = ' '
        
    def final_render(self, engine):
        '''An alternative render method if needed'''
        return self.render(engine)