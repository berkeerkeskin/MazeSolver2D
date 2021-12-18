#global variables
starting = []
bonus = []
goal = []

#string[start: end: step]
def readSquares(squares):
    for line in squares.splitlines():
        index = int(line[2:])
        if line[0] == "S":
            starting.append(index)
        elif line[0] == "T":
            bonus.append(index)
        elif line[0] == "G":
            goal.append(index)
            
def checkGoalState(goal, cellIndex):
    for i in range(len(goal)):
        if goal[i] == cellIndex:
            #yazım asamasında
            return 0
            
#read maze
with open('../input/project-maze-input2/maze.txt', 'r') as file:
    text = file.read()

#read important squares into string
with open('../input/squares/square_indexes_and_types.txt', 'r') as file:
    squares = file.read()
#read important squares into lists
readSquares(squares)

#split text file into an array
array = text.split("; ")
#dictionary for possible moves
possibleMoves={}

for i in range(64):
    array[i] = array[i].replace("\'", "")
    cell = array[i].split(", ")
    possibleMoves[i] = cell
