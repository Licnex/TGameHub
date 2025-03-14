import os
import sys
from games import tic_tac_toe, connect4, sudoku, snake, hangman, minesweeper, game_2048, battleship, chess, doom

def clear_screen():
    """Clears the terminal screen for a better user experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    """Displays the game hub menu and handles user input."""
    while True:
        clear_screen()
        print("🎮 Welcome to TGameHub! 🎮")
        print("1. Play Tic Tac Toe")
        print("2. Play Snake")
        print("3. Play Hangman")
        print("4. Play Connect 4")
        print("5. Play Minesweeper")
        print("6. Play 2048")
        print("7. Play Battleship")
        print("8. Play Sudoku")
        print("9. Play Chess")
        print("0. Exit")
        choice = input("Choose an option (0-9): ").strip()

        if choice == '1':
            tic_tac_toe.play()
        elif choice == '2':
            snake.play()
        elif choice == '3':
            hangman.play()
        elif choice == '4':
            connect4.play()
        elif choice == '5':
            minesweeper.play()
        elif choice == '6':
            game_2048.play()
        elif choice == '7':
            battleship.play()
        elif choice == '8':
            sudoku.play()
        elif choice == '9':
            chess.play()
        elif choice == '0':
            print("Thanks for playing! Goodbye. 👋")
            sys.exit()
        elif choice == '10':
            print("🎉 Congratulations! You found the secret game! 🎉 DOOM")
            doom.play()
        else:
            print("❌ Invalid choice. Please enter a number from 0 to 9.")
            input("Press Enter to try again...")

if __name__ == "__main__":
    main_menu()