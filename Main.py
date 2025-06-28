import os
import sys
import traceback

try:
    from Games import TicTacToe, Connect4, Sudoku, Snake, Hangman, BattleShip, Chess
except ImportError as e:
    print(f"❌ Error importing games: {e}")
    print("Please make sure all game files are present in the Games folder.")
    print("Also ensure you've installed the required packages: pip install -r requirements.txt")
    sys.exit(1)

def clear_screen():
    """Clears the terminal screen for a better user experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def launch_game(game_module, game_name):
    """Safely launches a game with error handling."""
    try:
        print(f"🎮 Starting {game_name}...")
        print("Press Ctrl+C at any time to return to the main menu.")
        print("-" * 40)
        game_module.play()
    except KeyboardInterrupt:
        print(f"\n🔄 Returning to main menu from {game_name}...")
    except AttributeError:
        print(f"❌ Error: {game_name} doesn't have a 'play()' function.")
        print("This might be a game file issue.")
    except Exception as e:
        print(f"❌ An error occurred while playing {game_name}:")
        print(f"Error: {str(e)}")
        print("\nThis might be due to:")
        print("• Missing dependencies (check requirements.txt)")
        print("• Terminal size too small")
        print("• Incompatible terminal type")
        print("\nTry:")
        print("• Making your terminal window larger")
        print("• Installing missing packages")
        print("• Running in a different terminal")
    finally:
        input("\nPress Enter to return to main menu...")
        clear_screen()

def main_menu():
    """Displays the game hub menu and handles user input. Make sure you have installed all the requirements manually before using this."""
    while True:
        clear_screen()
        print("🎮 Welcome to TGameHub! 🎮")
        print("=" * 50)
        print("📋 Available Games:")
        print("1. 🎯 Tic Tac Toe     - Classic 3x3 grid strategy game")
        print("2. 🐍 Snake           - Eat food, grow longer, avoid walls")
        print("3. 🎪 Hangman         - Guess the word letter by letter")
        print("4. 🔴 Connect 4       - Drop discs to get 4 in a row")
        print("5. ⚓ Battleship      - Sink the enemy fleet")
        print("6. 🔢 Sudoku          - Fill 9x9 grid with numbers 1-9")
        print("7. ♛ Chess           - Strategic board game")
        print("=" * 50)
        print("8. 🚪 Exit")
        print("9. ❓ Help & Info")
        print("=" * 50)
        choice = input("Choose an option (1-9): ").strip()

        if choice == '1':
            launch_game(TicTacToe, "Tic Tac Toe")
        elif choice == '2':
            launch_game(Snake, "Snake")
        elif choice == '3':
            launch_game(Hangman, "Hangman")
        elif choice == '4':
            launch_game(Connect4, "Connect 4")
        elif choice == '5':
            launch_game(BattleShip, "Battleship")
        elif choice == '6':
            launch_game(Sudoku, "Sudoku")
        elif choice == '7':
            launch_game(Chess, "Chess")
        elif choice == '8':
            print("Thanks for playing TGameHub! 👋")
            print("Come back anytime for more classic games!")
            sys.exit()
        elif choice == '9':
            clear_screen()
            print("📖 TGameHub Help & Information")
            print("=" * 50)
            print("🎮 About:")
            print("TGameHub is a collection of classic games written in Python.")
            print("All games run in your terminal for a retro gaming experience!")
            print()
            print("🎯 How to Play:")
            print("• Use the menu numbers (1-9) to select options")
            print("• Follow on-screen instructions for each game")
            print("• Most games use arrow keys for navigation")
            print("• Press Ctrl+C during any game to return to this menu")
            print()
            print("⚠️  Important Notes:")
            print("• Keep your terminal window large and zoom out for best display")
            print("• Install requirements manually: pip install -r requirements.txt")
            print("• Some packages might already be installed on your system")
            print("• If games don't display correctly, try a different terminal")
            print()
            print("📚 For specific game help, refer to README.md")
            print("🐛 Report issues at: https://github.com/Licnex/tgamehub")
            print("=" * 50)
            input("Press Enter to return to main menu...")
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 9.")
            print("💡 Tip: Make sure you're typing just the number (e.g., '1', not 'one')")
            input("Press Enter to try again...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using TGameHub! Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please report this issue at: https://github.com/Licnex/tgamehub")
        sys.exit(1)

if __name__ == "__main__":
    main_menu()