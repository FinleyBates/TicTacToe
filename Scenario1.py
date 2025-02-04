import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 10)

def check_winner(board, mark):
    for row in board: #check horizontal for 3 in a row
        if row.count(mark) == 3:
            return True
    for col in range(3):
        if [board[row][col] for row in range(3)].count(mark) == 3: #check vertical for 3 in a row
            return True
    if [board[i][i] for i in range(3)].count(mark) == 3 or [board[i][2 - i] for i in range(3)].count(mark) == 3: #check diagonal for 3 in a row
        return True
    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell not in ['X', 'O']:#allow numbers but not x/o
                return False
    return True

def get_empty_positions(board):
    empty_positions = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell not in ['X', 'O']: #check that cell is not already picked
                empty_positions.append((i, j))
    return empty_positions

def player_move(board):
    print("Your turn:")
    while True:
        try:
            move = int(input("Enter the position (1-9): ")) - 1
            if move < 0 or move >= 9:
                print("Invalid move. Try again.")
                continue
            row, col = divmod(move, 3)
            if board[row][col] not in ['X', 'O']:
                board[row][col] = 'X'
                break
            else:
                print("Position already taken. Try again.")
        except ValueError:
            print("Invalid input. Enter a number between 1 and 9.")

def computer_move(board): #random placement by computer
    print("Computer's turn:")
    empty_positions = get_empty_positions(board)
    move = random.choice(empty_positions)
    board[move[0]][move[1]] = 'O'

def main():
    board = [[str(3 * i + j + 1) for j in range(3)] for i in range(3)]
    print("Initial board:")
    print_board(board)

    while True:
        #player's move
        player_move(board)
        print_board(board)
        if check_winner(board, "X"):
            print("You win!")
            break
        if check_draw(board):
            print("This game is a draw!")
            break

        #computer's random move
        computer_move(board)
        print_board(board)
        if check_winner(board, "O"):
            print("Player 2 (Computer) wins!")
            break
        if check_draw(board):
            print("This game is a draw!")
            break

main()
