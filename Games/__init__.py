"""
TGameHub Games Package
Collection of classic games implemented in Python
"""

# Import all game modules to make them available when importing Games
from . import TicTacToe
from . import Connect4
from . import Sudoku
from . import Snake
from . import Hangman
from . import BattleShip
from . import Chess

__all__ = ['TicTacToe', 'Connect4', 'Sudoku', 'Snake', 'Hangman', 'BattleShip', 'Chess']