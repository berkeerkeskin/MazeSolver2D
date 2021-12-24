from collections import deque
#global variables
starting = []
trap = []
goal = []

#string[start: end: step]
def readSquares(squares):
    for line in squares.splitlines():
        index = int(line[2:])
        if line[0] == "S":
            starting.append(index)
        elif line[0] == "T":
            trap.append(index)
        elif line[0] == "G":
            goal.append(index)


def coordinate_from_index(index):
    return "(" + str((index % 8) + 1) + ", " + str((index // 8) + 1) + ")"


def IsGoalState(goal, cellIndex):
    for i in range(len(goal)):
        if goal[i] == cellIndex:
            return 1
    return 0

#read maze
with open('maze.txt', 'r') as file:
    text = file.read()

#read important squares
with open('square_indexes_and_types.txt', 'r') as file:
    squares = file.read()
#read important squares
readSquares(squares)

#split text file into an array
array = text.split(";\n")
#dictionary for possible moves
possibleMoves={}

for i in range(64):
    array[i] = array[i].replace("\'", "")
    cell_name = array[i].split(", ")
    cell_index = []
    for possibleMove in cell_name:
        if "east" in possibleMove:
            cell_index.append(i + 1)
        elif "south" in possibleMove:
            cell_index.append(i + 8)
        elif "west" in possibleMove:
            cell_index.append(i - 1)
        elif "north" in possibleMove:
            cell_index.append(i - 8)
    
    possibleMoves[i] = cell_index
print(possibleMoves)

#priority_queue:
#key = path as a string
#value = cost of the path
def dequeue(priority_queue):
    costs = []
    extracted_element = 0
    
    #find min cost element which is max priority
    for element in priority_queue:
        costs.append(priority_queue[element])
    min_cost = min(costs)
    min_cost_index = costs.index(min_cost)
    index = 0
    
    #extract max priority element
    for element in priority_queue:
        if index == min_cost_index:
            priority_queue.pop(element)
            extracted_element = element
            break
        index = index + 1
    #return statement in string
    return extracted_element

def GetCellCost(trap, goal, currentcell):
    if currentcell in trap:
        return 10
    elif currentcell in goal:
        return 0
    else:
        return 1

def uniform_cost_search(starting, bonus, goal, possibleMoves):
    ####initialization of variables####
    startcell = starting[0]
    currentcell = startcell
    #initialization of priority queue
    priority_queue = {}
    #holding path values for every visited cell
    paths = {}
    costs = {}
    paths[startcell] = str(startcell)
    costs[startcell] = 0
    explored_set = []
    #root node in the priority queue at the beginning
    priority_queue[startcell] = 0
    #step1-expand node
    #step2-add it to the explored set
    #step3-choose minimum cost, if equal expand east, south, west, north in order
    #step4-check if its goal state, if yes print all the outputs,else return to the step1
    while bool(priority_queue):
        #dequeue - extracted element is an integer
        extracted_element = dequeue(priority_queue)
        #update the current cell
        currentcell = extracted_element
        #add to the explored set
        explored_set.append(extracted_element)
        #expand the node into its children and add it to frontier
        children = possibleMoves[currentcell]
        for child in children:
            if child not in explored_set:
                if IsGoalState(goal, child):
                    path = paths[currentcell] + "-" + str(child)
                    cost = costs[currentcell] + GetCellCost(bonus, goal, child)
                    print(path)
                    print(cost)
                    return "finished"
                else:
                    path = paths[currentcell] + "-" + str(child)
                    paths[child] = path
                    cost = costs[currentcell] + GetCellCost(bonus, goal, child)
                    costs[child] = cost
                    priority_queue[child] = cost

uniform_cost_search(starting, trap, goal, possibleMoves)

print("!!!!!!!!!!!!!!!!!!!!!!!")


def dfs(startindex, graph):
    frontier = list()
    frontier_max_size = 0
    frontier.append(startindex)
    expanded = list()
    explored = list()
    solutionpath = list()
    solutioncost = 0
    while len(frontier) != 0:
        currentindex = frontier.pop()
        if currentindex in expanded:
            continue
        if IsGoalState(goal, currentindex):
            print("expanded set: " + "-".join(map(str, expanded)))
            print("frontier: " + "-".join(map(str, frontier)))
            print("frontier max size: " + str(frontier_max_size))
            solutionpath.append(currentindex)
            print("solution path: " + " – ".join(map(coordinate_from_index, solutionpath)))
            for solindex in solutionpath:
                solutioncost += GetCellCost(trap, goal, solindex)
            print("solution cost: " + str(solutioncost))
            for expandednode in expanded:
                #  all items of "graph[expandednode]" are in "expanded"
                if all(item in expanded for item in graph[expandednode]):
                    explored.append(expandednode)
            print("explored set: " + "-".join(map(str, explored)))
            print("explored maximum size: " + str(len(explored)))
            return
        for neighbour in graph[currentindex]:
            if neighbour in frontier:
                frontier.remove(neighbour)
            if neighbour not in expanded:
                frontier.append(neighbour)
                if len(frontier) > frontier_max_size:
                    frontier_max_size = len(frontier)
        expanded.append(currentindex)
        solutionpath.append(currentindex)
        checkdeadendindex = currentindex
        while all(item in expanded for item in graph[checkdeadendindex]):
            solutionpath.pop()
            checkdeadendindex = solutionpath[len(solutionpath)-1]


dfs(starting[0], possibleMoves)

# breadth first search algorithm


def bfs(bonus):
    # initialization of queue
    queue = deque()
    # root node in the queue at the beginning
    queue.append(starting[0])
    # initialization of the variables
    start_cell = starting[0]
    current_cell = start_cell
    # paths and costs
    paths = {}
    costs = {}
    list_queue = {}
    # assign values paths and costs
    paths[start_cell] = str(start_cell)
    costs[start_cell] = 0
    explored_set = []

    while len(queue) != 0:
        # pop
        current_cell = queue.pop()
        # append current cell to explored set
        explored_set.append(current_cell)
        # expand the node into its children and add it to frontier
        children = possibleMoves[current_cell]
        for child in children:
            if child not in explored_set:
                if IsGoalState(goal, child):
                    path = paths[current_cell] + "-" + str(child)
                    cost = costs[current_cell] + GetCellCost(bonus, goal, child)
                    print("The cost of solution is " + str(cost))
                    print("The maximum size of frontier is " + str(len(children)))
                    print("The maximum size of explored cell is " + str(len(explored_set)))
                    print("The solution path is " + path)

                    return "finished"
                else:
                    queue.appendleft(child)
                    path = paths[current_cell] + "-" + str(child)
                    paths[child] = path
                    cost = costs[current_cell] + GetCellCost(bonus, goal, child)
                    costs[child] = cost
                    list_queue[child] = cost


print("\n---Breadth First Search---")
bfs(trap)




