from collections import deque

#global variables
starting = []
trap = []
goal = []
node_number = 64

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
    return "(" + str((index // 8) + 1) + ", " + str((index % 8) + 1) + ")"


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

for i in range(node_number):
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
        return 1
    else:
        return 1

def uniform_cost_search(starting, trap, goal, possibleMoves):
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
    numberOfExpandedNodes = 0
    maxSizeOfFrontier = 0
    maxSizeOfExploredSet = 0
    #root node in the priority queue at the beginning
    priority_queue[startcell] = 0
    #step1-expand node
    #step2-add it to the explored set
    #step3-choose minimum cost, if equal expand east, south, west, north in order
    #step4-check if its goal state, if yes print all the outputs,else return to the step1
    while bool(priority_queue):
        if len(priority_queue) > maxSizeOfFrontier:
            maxSizeOfFrontier = len(priority_queue)
        if len(explored_set) > maxSizeOfExploredSet:
            maxSizeOfExploredSet = len(explored_set)
        #dequeue - extracted element is an integer
        #print(priority_queue)
        extracted_element = dequeue(priority_queue)
        #update the current cell
        currentcell = extracted_element
        #add to the explored set
        explored_set.append(extracted_element)
        #expand the node into its children and add it to frontier
        children = possibleMoves[currentcell]
        numberOfExpandedNodes = numberOfExpandedNodes + 1
        for child in children:
            if child not in explored_set:
                if IsGoalState(goal, child):
                    path = paths[currentcell] + "-" + str(child)
                    solution_path = list(map(int, path.split("-")))
                    cost = costs[currentcell] + GetCellCost(trap, goal, child)
                    print("--- Uniform Cost Search ---")
                    print("The cost of the solution: {0}".format(cost))
                    print("The number of expanded nodes: {0}".format(numberOfExpandedNodes))
                    print("The maximum size of the frontier: {0}".format(maxSizeOfFrontier))
                    print("The maximum size of the explored set: {0}".format(maxSizeOfExploredSet))
                    print("Solution Path: " + " - ".join(map(coordinate_from_index, solution_path)))
                    return
                else:
                    path = paths[currentcell] + "-" + str(child)
                    paths[child] = path
                    cost = costs[currentcell] + GetCellCost(trap, goal, child)
                    costs[child] = cost
                    priority_queue[child] = cost
                    
uniform_cost_search(starting, trap, goal, possibleMoves)

def FindIndex(cellIndex):
    cellIndex = cellIndex + 1
    x = cellIndex % 8
    y = (cellIndex - x) / 8
    XandY = []
    XandY.append(int(x))
    XandY.append(int(y))
    return XandY
#calculates manhattan distance, we need our square and all of the goal squares
def CalculateHN(goal, currentcell):
    currentXandY = FindIndex(currentcell)
    distances = []
    
    for goalcell in goal:
        goalXandY = FindIndex(goalcell)
        absoluteX = abs(goalXandY[0] - currentXandY[0])
        absoluteY = abs(goalXandY[1] - currentXandY[1])
        manhattanDistance = absoluteX + absoluteY
        distances.append(manhattanDistance)
    return min(distances)
    
def calculateScores(goal, cellIndex, costs, hn, gn, fn):
    #calculate hn
    hn[cellIndex] = CalculateHN(goal, cellIndex)
    #calculate gn
    gn[cellIndex] = costs[cellIndex]
    #calculate fn
    fn[cellIndex] = hn[cellIndex] + gn[cellIndex]
    return fn[cellIndex]
    
def GetLowestFScore(openlist):
    fscores = []
    extracted_element = 0
    #print(openlist)
    for item in openlist:
        #print(openlist[item])
        fscores.append(openlist[item])
    
    min_cost = min(fscores)
    min_cost_index = fscores.index(min_cost)
    index = 0
    for item in openlist:
        if index == min_cost_index:
            extracted_element = item
            break
        index = index + 1
    return extracted_element
    
def Astar(starting, trap, goal, possibleMoves):
    startcell = starting[0]
    currentcell = startcell
    openlist = {} #value holds f score
    parentlist = {}
    closedlist = {} #value holds f score
    costs = {}
    hn = {}
    gn = {}
    fn = {}
    costs[currentcell] = 0
    hn[currentcell] = 0
    gn[currentcell] = 0
    fn[currentcell] = 0
    parentlist[currentcell] = -1
    openlist[currentcell] = fn[currentcell]
    numberOfExpandedNodes = 0
    maxSizeOfFrontier = 0
    maxSizeOfExploredSet = 0
    while bool(openlist):
        if len(openlist) > maxSizeOfFrontier:
            maxSizeOfFrontier = len(openlist)
        if len(closedlist) > maxSizeOfExploredSet:
            maxSizeOfExploredSet = len(closedlist)
        #get the lowest f score
        currentcell = GetLowestFScore(openlist)
        #check if it is goal state
        #print(currentcell)
        if IsGoalState(goal, currentcell):
            path = []
            current = currentcell
            while parentlist[current] != -1:
                path.append(current)
                current = parentlist[current]
            path.append(startcell)
            print("\n--- A* Algorithm ---")
            print("The cost of the solution: {0}".format(fn[currentcell]))
            print("The number of expanded nodes: {0}".format(numberOfExpandedNodes))
            print("The maximum size of the frontier: {0}".format(maxSizeOfFrontier))
            print("The maximum size of the explored set: {0}".format(maxSizeOfExploredSet))
            print("The solution path is " + " – ".join(map(coordinate_from_index, path[::-1])))

            return path[::-1]
        #add current to the closedlist
        closedlist[currentcell] = openlist[currentcell]
        #remove current from openlist
        openlist.pop(currentcell)
        #get the children of current
        children = possibleMoves[currentcell]
        numberOfExpandedNodes = numberOfExpandedNodes + 1
        for child in children:
            # Child is on the closed list
            if child in closedlist:
                continue
            # Create the f, g, and h values
            costs[child] = costs[currentcell] + GetCellCost(trap, goal, child)
            fscore = calculateScores(goal, child, costs, hn, gn, fn)
            # Child is already in the open list
            for open_node in openlist:
                if child == open_node and gn[child] > gn[open_node]:
                    continue
            openlist[child] = fscore
            parentlist[child] = currentcell
            
Astar(starting, trap, goal, possibleMoves)


def dfs(startindex, graph):
    print("\n---Depth First Search---")
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
            # print("expanded set: " + "-".join(map(str, expanded)))
            print("number of expanded nodes: " + str(len(expanded)))
            # print("frontier: " + "-".join(map(str, frontier)))
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
            # print("explored set: " + "-".join(map(str, explored)))
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
print()

# IDS


def dls(startindex, graph, depth_limit):
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
            # print("expanded set: " + "-".join(map(str, expanded)))
            print("number of expanded nodes: " + str(len(expanded)))
            # print("frontier: " + "-".join(map(str, frontier)))
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
            # print("explored set: " + "-".join(map(str, explored)))
            print("explored maximum size: " + str(len(explored)))
            return True
        for neighbour in graph[currentindex]:
            if neighbour in frontier:
                frontier.remove(neighbour)
            if neighbour not in expanded:
                frontier.append(neighbour)
                if len(frontier) > frontier_max_size:
                    frontier_max_size = len(frontier)
        expanded.append(currentindex)
        solutionpath.append(currentindex)
        if len(solutionpath) - 1 == depth_limit:
            if solutionpath:
                solutionpath.pop()
            else:
                return False
            if solutionpath:
                checklimitindex = solutionpath.pop()
            else:
                return False
            while all(item in expanded for item in graph[checklimitindex]):
                if solutionpath:
                    checklimitindex = solutionpath.pop()
                else:
                    return False
            solutionpath.append(checklimitindex)
            for n in graph[currentindex]:
                if n in frontier:
                    frontier.remove(n)
            expanded.remove(currentindex)
            continue
        checkdeadendindex = currentindex
        while all(item in expanded for item in graph[checkdeadendindex]):
            solutionpath.pop()
            checkdeadendindex = solutionpath[-1]
        continue
    return False


def ids(startindex, graph, max_depth):
    print("---Iterative Deepening Search---")
    for i in range(max_depth + 1):
        if dls(startindex, graph, i):
            return True
    print("Path not found!")
    return False


ids(starting[0], possibleMoves, 11)


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
    # solution path
    solution_path = list()
    number_of_expanded_nodes = 0
    solution_path = []
    while len(queue) != 0:
        # pop
        current_cell = queue.pop()
        # append current cell to explored set
        explored_set.append(current_cell)
        # expand the node into its children and add it to frontier
        children = possibleMoves[current_cell]
        number_of_expanded_nodes += 1
        for child in children:
            if child not in explored_set:
                if IsGoalState(goal, child):
                    path = paths[current_cell] + "-" + str(child)
                    solution_path = list(map(int, path.split("-")))
                    cost = costs[current_cell] + GetCellCost(bonus, goal, child)
                    print("The cost of solution is " + str(cost))
                    print("The number of expanded nodes is  " + str(number_of_expanded_nodes))
                    print("The maximum size of frontier is " + str(len(children)))
                    print("The maximum size of explored cell is " + str(len(explored_set)))
                    print("The solution path is " + " – ".join(map(coordinate_from_index, solution_path)))
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

#coordinate of index
def coordinate_of_index(path):
    string_path = ""
    for coordinate in range(path):
        index = path.get(coordinate)
        row = (index % 8) + 1
        column = (index // 8) + 1
        coordinate.append(row)
        coordinate.append(column)
    return string_path



# calculate f score
def calculate_scores(goal, cellIndex, costs, hn, fn):
    #calculate hn
    hn[cellIndex] = CalculateHN(goal, cellIndex)
    #calculate fn
    fn[cellIndex] = hn[cellIndex]
    return fn[cellIndex]

# Greedy Best First Search
# key = h(n)
def gbfs(starting, trap, goal, possibleMoves):
    # initialize variables
    start_cell = starting[0]
    current_cell = start_cell
    open_list = {}
    parent_list = {}
    closed_list = {}
    costs = {}
    # f(n) = h(n)
    hn = {}
    fn = {}
    costs[current_cell] = 0
    hn[current_cell] = 0
    fn[current_cell] = 0
    parent_list[current_cell] = -1
    open_list[current_cell] = 0
    open_list[current_cell] = fn[current_cell]
    number_of_expanded_nodes = 0
    max_frontier = 0
    max_explored = 0

    while bool(open_list):
        # get the lowest f score
        current_cell = GetLowestFScore(open_list)
        if IsGoalState(goal, current_cell):
            path = []
            current = current_cell
            while parent_list[current] != -1:
                path.append(current)
                current = parent_list[current]

            path.append(start_cell)

            print("The cost of solution is " + str(costs[current_cell]))
            print("The number of expanded nodes is " + str(number_of_expanded_nodes))
            print("The maximum size of frontier is " + str(max_frontier))
            print("The maximum size of explored cell is " + str(max_explored))
            print("The solution path is " + " – ".join(map(coordinate_from_index, path[::-1])))
            return "finished"

        closed_list[current_cell] = open_list[current_cell]
        open_list.pop(current_cell)
        number_of_expanded_nodes += 1
        children = possibleMoves[current_cell]

        for child in children:
            if child in closed_list:
                continue

            costs[child] = costs[current_cell] + GetCellCost(trap, goal, child)
            fscore = calculate_scores(goal, child, costs, hn, fn)
            for open_node in open_list:
                if child == open_node and hn[child] > hn[open_node]:
                    continue
            open_list[child] = fscore
            parent_list[child] = current_cell

        if max_frontier < len(children):
            max_frontier = len(children)
        if max_explored < len(closed_list):
            max_explored = len(closed_list)

print("\n---Greedy Best First Search---")
gbfs(starting, trap, goal, possibleMoves)

