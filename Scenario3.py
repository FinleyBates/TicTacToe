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

def score(board, player, opponent): #keep a score, which is important for a minimax algorithm
    if check_winner(board, player):
        return 10
    elif check_winner(board, opponent):
        return -10
    else:
        return 0
    
def minimax(board, depth, is_maximizing, player, opponent, game_tree):
    #evaluate the current board state
    #print(f"Minimax call: depth={depth}, is_maximizing={is_maximizing}") #some testing 
    board_score = score(board, player, opponent)
    
    
    #check if the game is won or lost and return the score
    if board_score == 10 or board_score == -10:
        game_tree["score"] = board_score #sets score for tree
        game_tree["children"] = {} #reset children key
        return board_score
    
    #return 0 if draw
    if check_draw(board):
        game_tree["score"] = 0
        game_tree["children"] = {}
        return 0

    # if maximizing is true ( computer's turn )
    if is_maximizing:
        # initialise best to negative infinity to ensure any valid move will be higher
        best = -float('inf')
        game_tree["children"] = {}
        
        #iterate over all empty positions
        for move in get_empty_positions(board):
            #simluates move by placing computer's marker
            board[move[0]][move[1]] = player
            
            # recursively calls minimax for the next move with the minimizing
            child_tree = {} #resets child tree
            game_tree["children"][f"Move {move}"] = child_tree #adds a new child node for the current move
            best = max(best, minimax(board, depth + 1, False, player, opponent, child_tree))
            
            #resets position
            board[move[0]][move[1]] = str(3 * move[0] + move[1] + 1)
        
        # returns best score
        game_tree["score"] = best
        return best
    else:
        # for the human player's turn (minimizer), initialise best to positive infinity
        best = float('inf')
        game_tree["children"] = {}
        
        for move in get_empty_positions(board):
            board[move[0]][move[1]] = opponent
            
            # recursively calls minimax for the next move with the minimizing - taking the minimum move (where the opponent does not win)
            child_tree = {}
            game_tree["children"][f"Move {move}"] = child_tree
            best = min(best, minimax(board, depth + 1, True, player, opponent, child_tree))
       
            board[move[0]][move[1]] = str(3 * move[0] + move[1] + 1)
        
        game_tree["score"] = best
        return best
    
def print_game_tree(game_tree, depth=0):
    indent = " " * (depth * 2)
    for move, subtree in game_tree["children"].items():
        print(f"{indent}{move}: {subtree['score']}")
        print_game_tree(subtree, depth + 1) #indents further for each depth in that bracnh for readability

def computer_move(board, computer_marker, print_tree=False):
    print("Computer's turn:")
    opponent_marker = 'X' if computer_marker == 'O' else 'O'
    best_val = -float('inf')
    best_move = None
    game_tree = {"children": {}}

    for move in get_empty_positions(board):
        board[move[0]][move[1]] = computer_marker  # places computer marker to simulate the move
        move_tree = {}
        move_val = minimax(board, 0, False, computer_marker, opponent_marker, move_tree) # evaluate with minimax
        game_tree["children"][f"Move {move}"] = move_tree
        board[move[0]][move[1]] = str(3 * move[0] + move[1] + 1)  # undo temp move

        if move_val > best_val:
            best_move = move
            best_val = move_val

    # make the best move
    if best_move:
        board[best_move[0]][best_move[1]] = computer_marker
    
    if print_tree:
        print("Game Tree:")
        print_game_tree(game_tree)


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

def main():
    board = [[str(3 * i + j + 1) for j in range(3)] for i in range(3)]
    print("Initial board:")
    print_board(board)

    player_marker = input("Choose your marker (X/O): ").upper()
    while player_marker not in ['X', 'O']:
        player_marker = input("The options are 'x' and 'o', choose your marker (X/O): ").upper()
    
    computer_marker = 'O' if player_marker == 'X' else 'X'

    first_move = input("Do you want to go first? (yes/no): ").lower()
    while first_move not in ['yes', 'no']:
        first_move = input("Be serious, do you want to go first? (yes/no): ").lower()#provides the choice to go first or second

    print_tree = input("Do you want to see the game tree after each computer move? (yes/no): ").lower()
    while print_tree not in ['yes', 'no']:
        print_tree = input("Invalid choice. Do you want to see the game tree after each computer move? (yes/no): ").lower()

    player_turn = True if first_move == 'yes' else False
    print_tree_option = True if print_tree == 'yes' else False

    while True:
        if player_turn:
            # Player move
            player_move(board, player_marker)
            print_board(board)
            if check_winner(board, player_marker):
                print("You win!")
                break
        else:
            # Computer move with tree printing
            computer_move(board, computer_marker, print_tree_option)
            print_board(board)
            if check_winner(board, computer_marker):
                print("Player 2 (Computer) wins!")
                break
        
        if check_draw(board):
            print("It's a draw!")
            break

        player_turn = not player_turn #swaps turn

main()

#https://www.javatpoint.com/mini-max-algorithm-in-ai https://www.neverstopbuilding.com/blog/minimax