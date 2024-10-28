import random


# 初始盤面3*3的二維矩陣
def initialize_board():
    board = []
    for _ in range(3):
        row = []
        for _ in range(3):
            row.append("_")
        board.append(row)
    return board


# 列印盤面
def print_board(board):
    # 上方的數字行，因為要列印左邊數字列所以要空格
    print("  1 2 3")
    # Loop board並印出
    for i, row in enumerate(board):
        print(f"{i + 1} {' '.join(row)}")
    print()


# 檢查是否有贏家，return 'X' 或 'O'表示該玩家獲勝，如果平局則return None
def check_winner(board):
    # 檢查橫行
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "_":
            return row[0]
    # 檢查直行
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "_":
            return board[0][col]
    # 檢查對角線
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "_":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "_":
        return board[0][2]
    # 檢查是否平局
    if all(cell != "_" for row in board for cell in row):
        return "Draw"

    return None


def minimax(board, depth, is_maximizing, alpha, beta):
    # 終止條件，一方勝利或平局
    winner = check_winner(board)
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif winner == "Draw":
        return 0

    # 'O'玩家邏輯
    if is_maximizing:
        # 分數設為負無限大，代表最低可能的分數
        max_eval = -float("inf")
        # Loop盤面
        for i in range(3):
            for j in range(3):
                # 找到空格並暫時填入'O'
                if board[i][j] == "_":
                    board[i][j] = "O"
                    # 計算分數
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    # 還原盤面
                    board[i][j] = "_"
                    # 更新分數
                    max_eval = max(max_eval, eval)
                    # 更新alpha值
                    alpha = max(alpha, eval)
                    # beta小於alpha則剪枝
                    if beta <= alpha:
                        break
        return max_eval
    # 邏輯同上，但提供給'X'玩家
    else:
        min_eval = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = "X"
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = "_"
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval


# 電腦移動
def computer_move(board, player):
    # 設成正負無限大，紀錄能找到的最佳分數，X的邏輯是要想辦法下出對'O'最不利的步，反之
    best_score = -float("inf") if player == "O" else float("inf")
    # 紀錄移動位置
    move = None
    # Loop盤面，如果找到空格，則先放置並計算minmax分數
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = player
                score = minimax(board, 0, player == "X", -float("inf"), float("inf"))
                board[i][j] = "_"
                if (player == "O" and score > best_score) or (
                    player == "X" and score < best_score
                ):
                    best_score = score
                    move = (i, j)
    # 實際移動最佳步
    if move:
        board[move[0]][move[1]] = player


# 玩家移動，輸入row跟col
def human_move(board, row, col):
    if board[row][col] == "_":
        board[row][col] = "X"
        return True
    return False


# 人機對下邏輯
def play_human_vs_computer():
    # 初始化盤面
    board = initialize_board()
    print("Initial Board:")
    print_board(board)

    # Loop直到完成遊戲
    while True:
        # 玩家選擇要下的位置
        row, col = map(int, input("Enter your move (row col): ").split())
        # 防呆
        if not human_move(board, row - 1, col - 1):
            print("Invalid move. Try again.")
            continue
        # 顯示盤面
        print("After your move:")
        print_board(board)
        # 檢查是否有贏家
        result = check_winner(board)
        if result:
            break

        # 電腦選擇要下的位置
        print("Computer's move:")
        computer_move(board, "O")
        # 顯示盤面
        print_board(board)
        # 檢查是否有贏家
        result = check_winner(board)
        if result:
            break

    # 顯示獲勝方或平局
    if result == "X":
        print("You win!")
    elif result == "O":
        print("Computer wins!")
    else:
        print("It's a draw!")


# 增加隨機初始步，增加盤面變化
def random_first_move(board, player):
    # 隨機選擇棋盤上的一個位置，棋盤為初始空棋盤
    move = (random.randint(0, 2), random.randint(0, 2))
    board[move[0]][move[1]] = player


# 電腦對下邏輯
def simulate_self_play(games):
    # 初始化紀錄的變數
    win = 0
    loss = 0
    draw = 0
    game_boards = []

    # 執行遊戲
    for _ in range(games):
        # 初始化盤面
        board = initialize_board()
        # 'X'先手
        turn = "X"
        # 隨機初始步
        random_first_move(board, turn)
        turn = "O"

        # 根據角色，執行computer_move
        while True:
            computer_move(board, turn)
            result = check_winner(board)
            if result:
                break
            turn = "X" if turn == "O" else "O"

        # 紀錄盤面
        game_boards.append((board, result))

        # 紀錄勝敗場次
        if result == "X":
            win += 1
        elif result == "O":
            loss += 1
        else:
            draw += 1

    print(f"Results: Wins: {win}, Losses: {loss}, Draws: {draw}\n")

    for idx, (board, result) in enumerate(game_boards, 1):
        print(
            f"Game {idx} Result: {'Win' if result == 'X' else 'Loss' if result == 'O' else 'Draw'}"
        )
        print_board(board)


if __name__ == "__main__":
    # 選擇模式 1. 人機對下 2.電腦互下
    mode = input("Choose mode: (1) Human vs Computer, (2) Self Play: ")
    if mode == "1":
        play_human_vs_computer()
    elif mode == "2":
        # 要執行的局數
        games = int(input("Enter the number of games: "))
        simulate_self_play(games)
    # 如果輸入1或2以外的模式則報錯
    else:
        print("Invalid mode.")
