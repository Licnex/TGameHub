
# Initialize the board and game state
board = ["-"] * 9
game_on = True
current_player = None  # will be set after player selection

def display_board():
    """Display the current board with position numbers."""
    print(f"{board[0]} | {board[1]} | {board[2]}      1 | 2 | 3")
    print(f"{board[3]} | {board[4]} | {board[5]}      4 | 5 | 6")
    print(f"{board[6]} | {board[7]} | {board[8]}      7 | 8 | 9")

def choose_players():
    """Prompt Player 1 to choose a marker, and assign the other to Player 2."""
    while True:
        p1 = input("Select Player 1 marker (X or O): ").upper().strip()
        if p1 in ("X", "O"):
            p2 = "O" if p1 == "X" else "X"
            print(f"Player 1: {p1}, Player 2: {p2}")
            return p1
        print("Invalid input. Please choose X or O.")

def get_move(player):
    """Prompt the current player for a valid move and return the board index."""
    while True:
        move = input(f"Current Player {player}, choose a position (1-9): ").strip()
        if move not in map(str, range(1, 10)):
            print("Invalid input. Enter a number from 1 to 9.")
            continue

        idx = int(move) - 1
        if board[idx] != "-":
            print("That position is already taken. Try again.")
            continue

        return idx

def check_winner():
    """Check for a win or tie.
    
    Returns:
        'X' or 'O' if there is a winner,
        'Tie' if the board is full with no winner,
        None if the game should continue.
    """
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    
    for a, b, c in win_combinations:
        if board[a] == board[b] == board[c] != "-":
            return board[a]
    
    if "-" not in board:
        return "Tie"
    
    return None

def flip_player(player):
    """Return the opposite player's marker."""
    return "O" if player == "X" else "X"

def play():
    global current_player, game_on
    print("Welcome to Tic Tac Toe!")
    display_board()
    current_player = choose_players()
    
    while game_on:
        idx = get_move(current_player)
        board[idx] = current_player
        display_board()
        
        result = check_winner()
        if result:
            if result == "Tie":
                print("It's a tie!")
            else:
                print(f"Congratulations {result}, you win!")
            game_on = False
        else:
            current_player = flip_player(current_player)