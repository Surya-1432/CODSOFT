
import math

HUMAN = "X"
AI = "O"
EMPTY = " "

winning_positions = [
    (0,1,2), (3,4,5), (6,7,8),  
    (0,3,6), (1,4,7), (2,5,8),  
    (0,4,8), (2,4,6)            
]

def print_board(board):
    print()
    for i in range(3):
        row = " | ".join(board[3*i:3*i+3])
        print(" " + row)
        if i < 2:
            print("---+---+---")
    print()

def available_moves(board):
    return [i for i, v in enumerate(board) if v == EMPTY]

def check_winner(board):
    for a,b,c in winning_positions:
        if board[a] == board[b] == board[c] and board[a] != EMPTY:
            return board[a]
    if EMPTY not in board:
        return "Draw"
    return None

def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == AI:
        return 1
    elif winner == HUMAN:
        return -1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for move in available_moves(board):
            board[move] = AI
            eval = minimax(board, depth+1, False, alpha, beta)
            board[move] = EMPTY
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in available_moves(board):
            board[move] = HUMAN
            eval = minimax(board, depth+1, True, alpha, beta)
            board[move] = EMPTY
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board):
    best_score = -math.inf
    move_choice = None
    for move in available_moves(board):
        board[move] = AI
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            move_choice = move
    return move_choice

def human_turn(board):
    moves = available_moves(board)
    while True:
        try:
            user = int(input(f"Enter your move (1-9). Available: {[m+1 for m in moves]}: "))
            idx = user - 1
            if idx in moves:
                board[idx] = HUMAN
                return
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number 1-9.")

def ai_turn(board):
    move = best_move(board)
   
    if move is None:
        move = available_moves(board)[0]
    board[move] = AI
    print(f"AI places {AI} at position {move+1}")

def main():
    print("Tic-Tac-Toe: You are X. AI is O. Board positions are 1..9 left-to-right, top-to-bottom.")
    board = [EMPTY]*9


    while True:
        choice = input("Do you want to go first? (y/n): ").lower().strip()
        if choice in ("y","n"):
            human_first = (choice == "y")
            break

    current = "human" if human_first else "ai"
    print_board([str(i+1) for i in range(9)]) 

    while True:
        if current == "human":
            print_board(board)
            human_turn(board)
            current = "ai"
        else:
            ai_turn(board)
            current = "human"

        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == HUMAN:
                print("Congratulations — you win! 🎉")
            elif winner == AI:
                print("AI wins. Better luck next time!")
            else:
                print("It's a draw!")
            break

if __name__ == "__main__":
    main()
