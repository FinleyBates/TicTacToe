import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 10)

def check_winner(board, mark):
    #checks for 3 in a row on a 3x3 board
    for row in board:
        if row.count(mark) == 3: #horizontal win
            return True
    for col in range(3):
        if [board[row][col] for row in range(3)].count(mark) == 3: #vertical win
            return True
    if [board[i][i] for i in range(3)].count(mark) == 3 or [board[i][2 - i] for i in range(3)].count(mark) == 3: #diagonal win
        return True
    return False

def check_draw(board):
    #checks if there are any empty cells left on the board, if not then the game is a draw
    for row in board:
        for cell in row:
            if cell not in ['X', 'O']:
                return False
    return True

def get_empty_positions(board):
    #returns a list of empty positions ( not filled with x or o ), marked by co-ordinates
    empty_positions = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell not in ['X', 'O']:
                empty_positions.append((i, j))
    return empty_positions

def player_move(board, player_marker):
    print("Your turn:")
    while True:
        try:
            move = int(input("Enter the position (1-9): ")) - 1
            if move < 0 or move >= 9:
                print("This is out of bounds of this board, please choose between 1 and 9.")
                continue
            row, col = divmod(move, 3)
            if board[row][col] not in ['X', 'O']:
                board[row][col] = player_marker
                break
            else:
                print("There is already a marker in this position, try again.")
        except ValueError:
            print("Invalid input. Enter a number between 1 and 9.")

def can_win(board, mark):
    for i in range(3):
        for j in range(3):
            if board[i][j] not in ['X', 'O']:
                board[i][j] = mark
                if check_winner(board, mark):
                    board[i][j] = str(3 * i + j + 1)  # reset ce;;
                    return (i, j)
                board[i][j] = str(3 * i + j + 1)#reset cell
    return None

def computer_move(board, computer_marker):
    print("Computer's turn:")

    # Step 1: Check if there is a move to win the game
    move = can_win(board, computer_marker)
    if move:
        board[move[0]][move[1]] = computer_marker
        return

    # Step 2: Check for a move to block the opponent's game
    opponent_marker = 'X' if computer_marker == 'O' else 'O'
    move = can_win(board, opponent_marker)
    if move:
        board[move[0]][move[1]] = computer_marker
        return

    # Step 3: Claim the center if unoccupied
    if board[1][1] not in ['X', 'O']:
        board[1][1] = computer_marker
        return

    # Step 4: Place the marker on any empty cell
    empty_positions = get_empty_positions(board)
    move = random.choice(empty_positions)
    board[move[0]][move[1]] = computer_marker

def main():
    board = [[str(3 * i + j + 1) for j in range(3)] for i in range(3)]
    print("Initial board:")
    print_board(board)

    player_marker = input("Choose your marker (X/O): ").upper()
    while player_marker not in ['X', 'O']:
        player_marker = input("Invalid choice. Choose your marker (X/O): ").upper()
    
    computer_marker = 'O' if player_marker == 'X' else 'X'

    first_move = input("Do you want to go first? (yes/no): ").lower()
    while first_move not in ['yes', 'no']:
        first_move = input("Invalid choice. Do you want to go first? (yes/no): ").lower()

    player_turn = True if first_move == 'yes' else False

    while True:
        if player_turn:
            # Player move
            player_move(board, player_marker)
            print_board(board)
            if check_winner(board, player_marker):
                print("You win!")
                break
        else:
            # Computer move
            computer_move(board, computer_marker)
            print_board(board)
            if check_winner(board, computer_marker):
                print("Player 2 (Computer) wins!")
                break
        
        if check_draw(board):
            print("It's a draw!")
            break

        player_turn = not player_turn

main()
