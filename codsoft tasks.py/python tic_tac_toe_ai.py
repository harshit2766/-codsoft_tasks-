import math
 
HUMAN = "X"
AI = "O"
EMPTY = " "
 
 
def print_board(board):
    print()
    for i in range(0, 9, 3):
        row = board[i:i + 3]
        print(" " + " | ".join(row))
        if i < 6:
            print("---+---+---")
    print()
 
 
def winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6),              # diagonals
    ]
    for a, b, c in lines:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None
 
 
def is_full(board):
    return EMPTY not in board
 
 
def available_moves(board):
    return [i for i, v in enumerate(board) if v == EMPTY]
 
 
def minimax(board, depth, alpha, beta, is_maximizing):
    win = winner(board)
    if win == AI:
        return 10 - depth
    if win == HUMAN:
        return depth - 10
    if is_full(board):
        return 0
 
    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = AI
            score = minimax(board, depth + 1, alpha, beta, False)
            board[move] = EMPTY
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = HUMAN
            score = minimax(board, depth + 1, alpha, beta, True)
            board[move] = EMPTY
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score
 
 
def best_move(board):
    best_score = -math.inf
    move = None
    for m in available_moves(board):
        board[m] = AI
        score = minimax(board, 0, -math.inf, math.inf, False)
        board[m] = EMPTY
        if score > best_score:
            best_score = score
            move = m
    return move
 
 
def get_human_move(board):
    while True:
        raw = input("Your move (1-9, left-to-right/top-to-bottom): ").strip()
        if not raw.isdigit():
            print("Please enter a number between 1 and 9.")
            continue
        pos = int(raw) - 1
        if pos < 0 or pos > 8:
            print("Please enter a number between 1 and 9.")
            continue
        if board[pos] != EMPTY:
            print("That cell is already taken. Try again.")
            continue
        return pos
 
 
def play():
    board = [EMPTY] * 9
    print("Tic-Tac-Toe: You are 'X', the AI is 'O'.")
    print("Cells are numbered 1-9, left-to-right, top-to-bottom.")
    print_board(list("123456789"))
 
    human_turn = True  # human goes first
 
    while True:
        if human_turn:
            pos = get_human_move(board)
            board[pos] = HUMAN
        else:
            print("AI is thinking...")
            pos = best_move(board)
            board[pos] = AI
 
        print_board(board)
 
        win = winner(board)
        if win:
            print(f"{'You win!' if win == HUMAN else 'AI wins!'}")
            break
        if is_full(board):
            print("It's a draw!")
            break
 
        human_turn = not human_turn
 
 
if __name__ == "__main__":
    play()
 