import os
import sys
import signal
import time

from board import Board
from mario import Mario
from enemy import Enemy
from bullets import Bullet
from boss import Boss
import getInput

# On Windows, msvcrt is used for non-blocking key reads
if os.name == 'nt':
    import msvcrt

class Engine(Board, Mario, Enemy, Bullet):
    """
    Game engine that inherits from Board, Mario, Enemy, and Bullet.
    """
    def __init__(self):
        self.score = 0
        self.coins = 0
        self.lives = 3
        self.gridX = 0
        self.board = Board()
        self.mario = Mario(self)
        # Use the cross-platform getch from getInput
        self.getch = getInput.getch  # assuming getInput.py exposes getch as shown
        self.speed = 1
        self.its = 0
        self.lefTime = 300
        self.lupd = 0

    def run(self):
        # Define a timeout input function.
        def getinp(timeout=0.09):
            if os.name == 'nt':
                # Windows: use msvcrt.kbhit() in a loop until timeout.
                start_time = time.time()
                while time.time() - start_time < timeout:
                    if msvcrt.kbhit():
                        return self.getch()  # using our cross-platform getch
                return ''
            else:
                # Unix-based: use signal-based alarm
                def alarmhandler(signum, frame):
                    raise TypeError
                signal.signal(signal.SIGALRM, alarmhandler)
                signal.setitimer(signal.ITIMER_REAL, timeout)
                try:
                    ch = self.getch()
                    signal.alarm(0)
                    return ch
                except TypeError:
                    pass
                signal.signal(signal.SIGALRM, signal.SIG_IGN)
                return ''

        # Terminate the game, cleaning up sound and showing final stats.
        def terminate(s):
            # Only kill the background sound if on Unix
            if os.name != 'nt':
                os.system('killall -9 aplay')
            self.score += 5 * self.coins + self.gridX // 10
            print(s)
            print('\nGAME OVER\nYour Score : {}\nCoins Collected : {}\nCome Back Again!\n'.format(
                self.score, self.coins))
            sys.exit()

        # Initialize the board/background
        self.board.createBackground()

        # Render the board (this method should use your cross-platform clear)
        self.board.render(self)

        # Play background sound only on Unix (or adapt for Windows sound-playing)
        if os.name != 'nt':
            os.system('aplay ./sounds/bg.wav > /dev/null 2>&1 &')

        while True:
            if self.board.boss.lives <= 0:
                terminate('You Won!')
            if self.lives <= 0:
                terminate('You Lose :(')
            # Update the remaining time once per second.
            if time.time() - self.lupd > 1:
                self.lefTime -= 1
                if self.lefTime == 0:
                    terminate('Time Up...You Lose :(')
                self.lupd = time.time()

            # Get the input (with timeout)
            inp = getinp()
            if inp == 'q':
                terminate('You Lose :(')
            elif inp == ' ':
                self.mario.fireBullet(self)
            elif inp == 'w':
                self.mario.up = True
            elif inp == 's':
                self.mario.up = False
            elif inp == 'a':
                if self.gridX > 0:
                    if self.board.render(self):
                        self.gridX -= self.speed
                        # Toggle Mario's leg appearance
                        if self.mario.legs == '/    \\':
                            self.mario.legs = '\\    /'
                        else:
                            self.mario.legs = '/    \\'
            elif inp == 'd':
                if self.gridX < 1250 and self.board.render(self):
                    self.gridX += self.speed
                    if self.mario.legs == '/    \\':
                        self.mario.legs = '\\    /'
                    else:
                        self.mario.legs = '/    \\'

            self.coins = self.mario.updatePos(self, self.board, self.gridX, self.coins)
            if self.mario.legsY >= self.board.height - 3:
                self.lives -= 1
                # Only play sound command if available (Unix example)
                if os.name != 'nt':
                    os.system('aplay ./sounds/fall.wav > /dev/null 2>&1 &')
                if self.lives == 0:
                    terminate('You Lose :(')
                self.mario.newLife(self)
                self.gridX = 0

            self.its += 0.1
            self.board.render(self)