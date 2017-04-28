print 'Welcome to Tic-Tac-Toe!'

# Global Init
board = [[1,2,3],[4,5,6],[7,8,9]]
turns = 0
playerIndex = 0

def HasWinner(): # Evaluate board for a winner
    global turns
    turns += 1
    if turns > 4:
        return True
    return False

players = ("Player1", "Player2") # Get players' names
# Play
print "{x}\n{y}\n{z}".format(x=board[0], y=board[1], z=board[2])
while not HasWinner():
    print "{p}, it's your turn.".format(p=players[playerIndex])
    # Get input from current player
    # Check board
    playerIndex += 1
    playerIndex %= 2
    
print 'Game Over, {winner} is the winner!'.format(winner=players[playerIndex])
