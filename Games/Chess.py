"""Edited version of https://github.com/BiancaNCoelho/ChessCLI"""
import curses
import re

inputTranslator = {
    "1": 7,
    "2": 6,
    "3": 5,
    "4": 4,
    "5": 3,
    "6": 2,
    "7": 1,
    "8": 0,
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
}

class Chess:
    def __init__(self, whiteName, blackName, turnRepository):
        self.sideSize = 8
        self.table = Table()
        self.blackPlayer = Player(blackName, turnRepository)
        self.whitePlayer = Player(whiteName, turnRepository)

    def playTurn(self, userInput):
        regex = re.compile("^[a-h][1-8] [a-h][1-8]$")
        if regex.match(userInput) is not None:
            fromPos = Position(inputTranslator[userInput[1]], inputTranslator[userInput[0]])
            toPos = Position(inputTranslator[userInput[4]], inputTranslator[userInput[3]])
            if self.table.movePiece(fromPos, toPos):
                return True
        return False

    def __repr__(self):
        return self.table.__repr__()

class Player:
    def __init__(self, name, turnRepository):
        self.name = name
        self.turnRepository = turnRepository

    def play(self, chess, fromPosition, toPosition):
        if not self._canPlay():
            return
        print("playing")

    def _canPlay(self):
        return self.turnRepository.getCurrent() == self.name

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TurnRepository:
    def __init__(self, whiteName, blackName):
        self.turns = [(whiteName, "WHITE"), (blackName, "BLACK")]
        self.winner = None

    def getCurrent(self):
        return self.turns[0][0]

    def getCurrentColor(self):
        return self.turns[0][1]
    
    def nextTurn(self):
        self.turns.reverse()

    def finished(self):
        return self.winner is not None

class Table:
    def __init__(self):
        self.size = 8
        self.table = [[" "] * self.size for _ in range(self.size)]
        self._initPieces()

    def __repr__(self):
        repr_str = ""
        repr_str += "     A     B     C     D     E     F     G     H\n"
        repr_str += "    _____________________________________________\n"
        aux = ["8", "7", "6", "5", "4", "3", "2", "1"]
        for i in range(self.size):
            repr_str += aux[i] + " | " + " | ".join(self.table[i][j].__repr__() for j in range(self.size)) + " |\n"
            repr_str += "    _____________________________________________\n"
        return repr_str
        
    def _initPieces(self):
        for i in range(self.size):
            self.table[1][i] = Pawn("W")
            self.table[6][i] = Pawn("B")

        self.table[0][0] = Rook("W")
        self.table[7][0] = Rook("B")

        self.table[0][1] = Knight("W")
        self.table[7][1] = Knight("B")

        self.table[0][2] = Bishop("W")
        self.table[7][2] = Bishop("B")

        self.table[0][3] = Queen("W")
        self.table[7][3] = Queen("B")

        self.table[0][4] = King("W")
        self.table[7][4] = King("B")

        self.table[0][5] = Bishop("W")
        self.table[7][5] = Bishop("B")

        self.table[0][6] = Knight("W")
        self.table[7][6] = Knight("B")
        
        self.table[0][7] = Rook("W")
        self.table[7][7] = Rook("B")

    def movePiece(self, fromPos, toPos):
        piece = self.table[fromPos.x][fromPos.y]
        if piece == " ":
            return False
        intermediatePieces = self.getIntermediatepiecesFromTo(fromPos, toPos)
        if not piece.canMoveTo(fromPos, toPos, intermediatePieces):
            return False
        secondPiece = self.table[toPos.x][toPos.y]
        if secondPiece != " ":
            # Handle capturing the piece
            pass
        self.table[fromPos.x][fromPos.y] = " "
        self.table[toPos.x][toPos.y] = piece
        return True

    def getIntermediatepiecesFromTo(self, fromPos, toPos):
        return []

class Pawn:
    def __init__(self, colorId):
        self.colorId = colorId
    def __repr__(self):
        return "P-" + self.colorId
    def canMoveTo(self, fromPos, toPos, intermediatePieces):
        return True

class Bishop:
    def __init__(self, colorId):
        self.colorId = colorId
    def __repr__(self):
        return "B-" + self.colorId
    def canMoveTo(self, fromPos, toPos, intermediatePieces):
        return True

class Knight:
    def __init__(self, colorId):
        self.colorId = colorId
    def __repr__(self):
        return "N-" + self.colorId
    def canMoveTo(self, fromPos, toPos, intermediatePieces):
        return True

class Rook:
    def __init__(self, colorId):
        self.colorId = colorId
    def __repr__(self):
        return "R-" + self.colorId
    def canMoveTo(self, fromPos, toPos, intermediatePieces):
        return True

class Queen:
    def __init__(self, colorId):
        self.colorId = colorId
    def __repr__(self):
        return "Q-" + self.colorId
    def canMoveTo(self, fromPos, toPos, intermediatePieces):
        return True

class King:
    def __init__(self, colorId):
        self.colorId = colorId
    def __repr__(self):
        return "K-" + self.colorId
    def canMoveTo(self, fromPos, toPos, intermediatePieces):
        return True

def draw_board(stdscr, chess, turnRepository):
    stdscr.clear()
    try:
        height, width = stdscr.getmaxyx()
        if height < 20 or width < 40:
            raise ValueError("Window too small")
        stdscr.addstr(0, 0, f"It's the turn of {turnRepository.getCurrent()} - {turnRepository.getCurrentColor()}\n")
        stdscr.addstr(1, 0, str(chess))
    except ValueError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, str(e))
        stdscr.addstr(1, 0, "Please resize the window and rerun the main.py")
    stdscr.refresh()

def get_input(stdscr, prompt):
    stdscr.addstr(prompt)
    stdscr.refresh()
    curses.echo()
    input_str = stdscr.getstr().decode('utf-8')
    curses.noecho()
    return input_str

def game(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    stdscr.addstr("Welcome to Chess\n")
    whiteName = get_input(stdscr, "Please enter the name of the player who will be white: ")
    blackName = get_input(stdscr, "Please enter the name of the player who will be black: ")

    turnRepository = TurnRepository(whiteName, blackName)
    chess = Chess(whiteName, blackName, turnRepository)
    while not turnRepository.finished():
        draw_board(stdscr, chess, turnRepository)
        played = False
        while not played:
            userInput = get_input(stdscr, f"{turnRepository.getCurrent()} > ")
            if not chess.playTurn(userInput):
                height, width = stdscr.getmaxyx()
                stdscr.addstr(height - 1, 0, "Illegal move. Please enter a move in the format 'e2 e4'.")
                stdscr.refresh()
            else:
                played = True
        turnRepository.nextTurn()

def play():
    curses.wrapper(game)
