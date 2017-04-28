# Global Init
board = [[1,2,3],[4,5,6],[7,8,9]]
marks = ('X', 'O')
turns = 0
playerIndex = 0

def HasWinner(): # Evaluate board for a winner
    global turns
    turns += 1
    if turns > 10:
        print 'Game Over, {winner} is the winner!'.format(winner=players[playerIndex])
        return True
    return False

def EndGame():
    global turns
    if turns == 10:
        print "Game Over, it's a draw."
        return True
    return False

def PrintBoard():
    global board
    print "{x}\n{y}\n{z}".format(x=board[0], y=board[1], z=board[2])

def MarkBoard(cell):
    for row in board:
        if cell in row:
            idx = row.index(cell)
            row[idx] = marks[playerIndex]

# Start Game
print 'Welcome to Tic-Tac-Toe!'

# Get players' names 
player1 = raw_input("Player1, what's your name? ") or "Player1"
player2 = raw_input("Player2, what's your name? ") or "Player2"
players = (player1, player2)

# Play
PrintBoard()
while not HasWinner() and not EndGame():
    # Get input from current player
    print "{p}, it's your turn.".format(p=players[playerIndex])
    cell = int(raw_input("Choose cell: "))
    MarkBoard(cell)
    PrintBoard()
    # Check board
    playerIndex += 1
    playerIndex %= 2
