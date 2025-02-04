MAX_DEPTH = 4  #sets max depth for faster calculations with slightly less accuracy

class color: #makes the moves more readable
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def print_board(board):
    for row in board:
        formatted_row = []
        for cell in row:
            if cell == 'X':
                formatted_row.append(f"{color.BOLD}{color.RED}{cell:2}{color.END}")
            elif cell == 'O':
                formatted_row.append(f"{color.BOLD}{color.CYAN}{cell:2}{color.END}")
            else:
                formatted_row.append(f"{cell:2}")
        print(" | ".join(formatted_row))  # Ensures all the cells have a minimum of 2 characters width
        print("-" * 24)

def check_winner(board, mark):
    #checks for 5 in a row on a 5x5 board
    for row in board:
        if row.count(mark) == 5: #horizontal win
            return True
    for col in range(5):
        if [board[row][col] for row in range(5)].count(mark) == 5: #vertical win
            return True
    if [board[i][i] for i in range(5)].count(mark) == 5 or [board[i][4 - i] for i in range(5)].count(mark) == 5: #diagonal win
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

def score(board, player, opponent): #keep a score, which is important for a minimax algorithm
    if check_winner(board, player):
        return 10
    elif check_winner(board, opponent):
        return -10
    else:
        return 0
    
def heuristic_evaluation(board, player, opponent):
    player_score = 0
    opponent_score = 0

    #evals row
    for row in board:
        player_score += row.count(player)
        opponent_score += row.count(opponent)

    #evals column
    for col in range(5):
        player_score += [board[row][col] for row in range(5)].count(player)
        opponent_score += [board[row][col] for row in range(5)].count(opponent)

    #evals diagnoal
    player_score += [board[i][i] for i in range(5)].count(player)
    player_score += [board[i][4 - i] for i in range(5)].count(player)
    opponent_score += [board[i][i] for i in range(5)].count(opponent)
    opponent_score += [board[i][4 - i] for i in range(5)].count(opponent)

    return player_score - opponent_score
    
"""PSUEDOCODE
function minimax(node, depth, isMaximizingPlayer, alpha, beta):

    if node is a leaf node :
        return value of the node
    
    if isMaximizingPlayer :
        bestVal = -INFINITY 
        for each child node :
            value = minimax(node, depth+1, false, alpha, beta)
            bestVal = max( bestVal, value) 
            alpha = max( alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else :
        bestVal = +INFINITY 
        for each child node :
            value = minimax(node, depth+1, true, alpha, beta)
            bestVal = min( bestVal, value) 
            beta = min( beta, bestVal)
            if beta <= alpha:
                break
        return bestVal"""

def minimax(board, depth, is_maximizing, player, opponent, alpha, beta):
    # Debug statement to track progress
    # print(f"Minimax call: depth={depth}, is_maximizing={is_maximizing}, alpha={alpha}, beta={beta}")

    #evaluate the current board state
    board_score = score(board, player, opponent)
    
    #check if the game is won or lost and return the score
    if board_score == 10 or board_score == -10:
        return board_score
    
    #return 0 if draw
    if check_draw(board):
        return 0
    
    if depth >= MAX_DEPTH:
        return heuristic_evaluation(board, player, opponent)

    # if maximizing is true ( computer's turn )
    if is_maximizing:
        # initialise best to negative infinity to ensure any valid move will be higher
        best = -float('inf')
        
        #iterate over all empty positions
        for move in get_empty_positions(board):
            #simluates move by placing computer's marker
            board[move[0]][move[1]] = player
            
            # recursively calls minimax for the next move with the minimizing
            best = max(best, minimax(board, depth + 1, False, player, opponent, alpha, beta))
            
            #resets position
            board[move[0]][move[1]] = str(5 * move[0] + move[1] + 1)

            alpha = max(alpha, best)

            if beta <= alpha:
                break
        
        # returns best score
        return best
    else:
        # for the human player's turn (minimizer), initialise best to positive infinity
        best = float('inf')
        
        for move in get_empty_positions(board):
            board[move[0]][move[1]] = opponent
            
            # recursively calls minimax for the next move with the minimizing - taking the minimum move (where the opponent does not win)
            best = min(best, minimax(board, depth + 1, True, player, opponent, -float('inf'), float('inf')))
       
            board[move[0]][move[1]] = str(5 * move[0] + move[1] + 1)
            beta = min(beta, best)
            if beta <= alpha:
                break
        
        return best


def player_move(board, player_marker):
    print("Your turn:")
    while True:
        try:
            move = int(input("Enter the position (1-25): ")) - 1
            if move < 0 or move >= 25:
                print("This is out of bounds of this board, please choose between 1 and 25.")
                continue
            row, col = divmod(move, 5)
            if board[row][col] not in ['X', 'O']:
                board[row][col] = player_marker
                break
            else:
                print("There is already a marker in this position, try again.")
        except ValueError:
            print("Invalid input. Enter a number between 1 and 9.")

def computer_move(board, computer_marker):
    print("Computer's turn:")
    opponent_marker = 'X' if computer_marker == 'O' else 'O'
    best_val = -float('inf')  
    best_move = None 

    # Iterate over all empty positions on the board.
    for move in get_empty_positions(board):
        board[move[0]][move[1]] = computer_marker  # simulate move by placing computer marker
        move_val = minimax(board, 0, False, computer_marker, opponent_marker, -float('inf'), float('inf'))  # evaluate with minimax
        board[move[0]][move[1]] = str(5 * move[0] + move[1] + 1)  #undo move

        if move_val > best_val:
            best_move = move  
            best_val = move_val  

    # make the best move found
    if best_move:
        board[best_move[0]][best_move[1]] = computer_marker

def main():
    board = [[str(5 * i + j + 1) for j in range(5)] for i in range(5)]
    print("Initial board:")
    print_board(board)

    player_marker = input("Choose your marker (X/O): ").upper()
    while player_marker not in ['X', 'O']:
       player_marker = input("The options are 'x' and 'o', choose your marker (X/O): ").upper()
    
    computer_marker = 'O' if player_marker == 'X' else 'X'

    first_move = input("Do you want to go first? (yes/no): ").lower()
    while first_move not in ['yes', 'no']:
        first_move = input("Be serious, do you want to go first? (yes/no): ").lower()#provides the choice to go first or second

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

        player_turn = not player_turn #swaps turn

main()


#https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/ 

