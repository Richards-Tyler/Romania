from collections import namedtuple
#Tyler Richards
hungary = {
    #Create a Dictionary of Tuples that stores where any one point can go and the distance to the next step
    "Arad": [("Sibiu", 140), ("Timisoara", 118), ("Zerind", 75)],
    "Bucharest": [("Urziceni", 85), ("Giurgiu", 90), ("Pitesti", 101), ("Fagaras", 211)],
    "Craiova": [("Pitesti", 138), ("Rimmicu", 146), ("Dobreta", 120)],
    "Dobreta": [("Craiova", 120), ("Mehadia", 75)],
    "Eforie": [("Hirsova", 86)],
    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
    "Giurgiu": [("Bucharest", 90)],
    "Hirsova": [("Eforie", 86), ("Urziceni", 98)],
    "Iasi": [("Neamt", 87), ("Vaslui", 92)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia": [("Lugoj", 70), ("Dobreta", 75)],
    "Neamt": [("Iasi", 87)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Pitesti": [("Rimmicu", 97), ("Bucharest", 101), ("Craiova", 138)],
    "Rimmicu": [("Pitesti", 97), ("Sibiu", 80), ("Craiova", 146)],
    "Sibiu": [("Oradea", 151), ("Fagaras", 99), ("Arad", 140), ("Rimmicu", 80)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
    "Zerind": [("Arad", 75), ("Oradea", 71)]
}

class PriorityQueue(object): 

    def __init__(self):
        self.data = []

    def empty(self): #Checks if the Queue is empty and returns if true
        return len(self.data) == 0 # in Python == checks value equality, not reference equality

    def front(self): #Returns first index of Queue if possible, if not it'll call empty()
        return self.data[0] if not self.empty() else None

    def pop(self): # Pops the end of the Priority Queue, looks for the lowest 
        # The lambda tells python that there is going to be an in-line method, e: e[1][0] returns the price of each jump as you step through the queue
        index = min(enumerate(self.data), key=lambda e: e[1][0])[0] #Enumerates through the first index of the 
        # priority queue and finds for the lowest # priority entry, then sets it to index and returns it as our next step
        return self.data.pop(index) #returns the found entry

    def push(self, priority, datum): #This is where we assign the priority to our Queue, which in turns decides the behavior of our search
        self.data.append((priority, datum)) #this will add the data to the correct position in the Queue

    def __iter__(self): #Iterates through our data
        for datum in self.data: #for every piece of data in the Queue
            for d in datum[1]: #looks for the name portion 
                yield d #return the retrieved data, yeild returns the data as a Generator-type, which can only be iterated over once and saves memory

class Path(object): # A Class to keep track of the path that we're on

    def __init__(self, nodes = None): #initiates our path, either empty or with the nodes that we pass to it on run time
        self.nodes = nodes or []

    def __len__(self): #overwritten method, returns length of path
        return len(self.nodes)

    def __repr__(self): #returns a string representation of all the nodes in the path
        return " to ".join(str(x) for x in self.nodes)

    def __iter__(self): #Iterates through the path, necessary for repr and checking path cost
        for node in self.nodes:
            yield node[0] 

    def end(self): #returns the last node in the path, we use this to check our goal
        return self.nodes[-1]

def graph_search(graph, start, goal, priority): #our actual search method, accepts 4 arguments, priority being the most important for our logic

    starting = Path([(start, 0)]) #create an initial path and initialize it with our Path class, accepts the start we pass and sets the cost to 0
    frontier = PriorityQueue() #Instantiate our priority queue
    frontier.push(0, starting) #push our starting path to our queue with 0 priority
    explored = [start] #initiate an array to keep track of where we've been. Add start to it
    steps = 0 # Keeps track of Steps

    while(True): #Keeps going forever

        if frontier.empty(): #If we hit a dead end
            return False #We fail
        cost, path = frontier.pop() #Take the lowest priority item off our  queue and store them in local variables
        state = path.end()[0] # take the end of our current node and make it our new state (making a jump)
        steps += 1 # add a step       
        if state == goal:#Check if our new state is our goal state
            return path, steps #If it is we return our answer
        for node in graph[state]: #iterate through our graph looking for our current state
            if node[0] not in explored or node[0] not in frontier: #check every corresponding node to see if we've been there
                new_path = Path(path.nodes + [node]) #if we haven't its a new path, so we create a new object of this jump as a path type
                frontier.push(priority(new_path), new_path) #which we then push to our PriorityQueue with our priority, depending on the search        
        explored.append(state)

def ufcp(path): #Defines the ufc-cost Search priority system

    return sum(node[1] for node in path.nodes) #will find the sum cost for the current path and set that as it's priority, so
    # lower cost paths will be expanded first because our queue looks for the lowest priority

def bfsp(path):# Defines the bfs-First Search Priority

    return len(path) #returns the length of the path, shorter paths are popped first then ones that have been there the longest

def dfsp(path): #Defines the dfs-First Priority  

    return bfsp(path) * -1 # The same as the bfs search except we set the values to negative, so the longest and most recent path is
    #always expanded first, since the Queue pulls the lowest value
#Create objects of our searches and pass our test to them

bfs = graph_search(hungary, "Arad", "Bucharest", bfsp)
dfs = graph_search(hungary, "Arad", "Bucharest", dfsp)
ufc = graph_search(hungary, "Arad", "Bucharest", ufcp)

#Print our results
print "Breath First: %s | steps taken to find goal: %d -- cost of path: %d" % (bfs[0], bfs[1], ufcp(bfs[0]))
print "Depth First: %s | steps taken to find goal: %d -- cost of path: %d" % (dfs[0], dfs[1], ufcp(dfs[0]))
print "Uniform Cost: %s | steps taken to find goal: %d -- cost of path: %d" % (ufc[0], ufc[1], ufcp(ufc[0]))
