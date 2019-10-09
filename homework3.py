### Homework Assingment 1 - CSCI 561

import queue 
from collections import deque

outputFile = open("output.txt", "w")
noOfTargetSites = 0

class Coordinates:
	def __init__(self, x, y):
	    self.x = x
	    self.y = y

	def __lt__(self, other):
		if isinstance(other, Coordinates):
			if self.x < other.x or self.y < other.y:
				return True
			return False

def readInputFile():
	algorithm = ""
	landingCoordinate = Coordinates(0, 0)
	terrain = []
	targetsites = []
	w = 0
	h = 0
	threshold = 0
#	noOfTargetSites = 0
	line = ""

	with open('input100.txt', 'r') as inputFile:
		line = inputFile.readline()
		count = 1
		while line:
			if count == 1:
				algorithm = line.rstrip()
			elif count == 2:
				w, h = line.split()
				w = int(w)
				h = int(h)

			elif count == 3:
				landing_w, landing_h = line.split()
				landingCoordinate = Coordinates(int(landing_h), int(landing_w))
			elif count == 4:
				threshold = line
			elif count == 5:
				noOfTargetSites = int(line)
			elif count == 6:
				for i in range(0, noOfTargetSites):
					target_w, target_h = line.split()
					targetsites.append(Coordinates(int(target_h), int(target_w)))
					if i < noOfTargetSites - 1:
						line = inputFile.readline()
			elif count == 7:
				for i in range(0, h):
					terrain.append(line.rstrip())
					terrain[i] = terrain[i].split()
					line = inputFile.readline()
			elif count == 8:
				break
			
			line = inputFile.readline()
			count += 1

	findPaths(algorithm, landingCoordinate, terrain, targetsites, threshold)

def findPaths(algorithm, landingCoordinate, terrain, targetsites, threshold):
	if algorithm == "A*":
		for targetsite in targetsites:
			findPathsUsingAStar(landingCoordinate, terrain, targetsite, threshold)
	elif algorithm == "BFS": 
		for targetsite in targetsites:
			findPathsUsingBFS(landingCoordinate, terrain, targetsite, threshold)
	elif algorithm == "UCS": 
		for targetsite in targetsites:
			findPathsUsingUCS(landingCoordinate, terrain, targetsite, threshold)

def findPathsUsingBFS(landingCoordinate, terrain, targetsite, threshold):
	w, h = len(terrain), len(terrain[0])
	count = 0

	frontierQueue = deque()
	exploredQueue = deque()
	parentChildList = []
	paths = []

	visited = [[False for i in range(0, h)] for j in range(0, w)]

	if (targetsite.x == landingCoordinate.x and targetsite.y == landingCoordinate.y):
		paths.append(landingCoordinate)
		writePathIntoFile(paths)
		return "Success"

	frontierQueue.append(landingCoordinate)

	while True :
		if not frontierQueue:
			writePathIntoFile("FAIL")
			return "FAIL"

		node = frontierQueue.popleft()
		node.x = int(node.x)
		node.y = int(node.y)

		if (targetsite.x == node.x and targetsite.y == node.y):
			parentChildList.append([node, childNodes])
			findParent(landingCoordinate, parentChildList, node, paths)
			paths.append(node)
			writePathIntoFile(paths)
			return "Success"

		exploredQueue.append(node)
		visited[node.x][node.y] = True

		childNodes = deque()

		result = findNeighbors(node, w, h, terrain, threshold, visited, frontierQueue, childNodes, parentChildList, paths, targetsite, landingCoordinate, exploredQueue)
		if result == "Success":
			break;

def findNeighbors(node, w, h, terrain, threshold, visited, frontierQueue, childNodes, parentChildList, paths, targetsite, landingCoordinate, exploredQueue):
	for i in range(-1, 2):
		for j in range(-1, 2):
			if (((((node.x + i) >= 0 and (node.x + i) <= (int(w) - 1)) and ((node.y + j) >= 0 and (node.y + j) <= (int(h) - 1))) and (i != 0 or j != 0)) and not isVisited(visited, Coordinates(node.x + i, node.y + j)) and abs((int(terrain[node.x + i][node.y + j]) - int(terrain[node.x][node.y]))) <= int(threshold)) :
				neighbor = Coordinates(node.x + i, node.y + j)

				isPresent = False

				if (targetsite.x == neighbor.x and targetsite.y == neighbor.y):
					parentChildList.append([neighbor, childNodes])
					findParent(landingCoordinate, parentChildList, node, paths)
					paths.append(node)
					paths.append(neighbor)
					writePathIntoFile(paths)
					return "Success"

				isPresent = isVisited(visited, neighbor)

				if isPresent == False:
					frontierQueue.append(neighbor)
					visited[neighbor.x][neighbor.y] = True
					childNodes.append(neighbor)

	parentChildList.append([node, childNodes])

def findPathsUsingUCS(landingCoordinate, terrain, targetsite, threshold):
	w, h = len(terrain), len(terrain[0])
	count = 0
	pathCost = 0

	frontierQueue = queue.PriorityQueue(0)
	exploredQueue = deque()
	parentChildList = []
	paths = []

	visited = [[False for i in range(0, h)] for j in range(0, w)]

	if (targetsite.x == landingCoordinate.x and targetsite.y == landingCoordinate.y):
		paths.append(landingCoordinate)
		writePathIntoFile(paths)
		return "Success"

	frontierQueue.put((pathCost, landingCoordinate))

	while True :
		if frontierQueue.empty():
			writePathIntoFile("FAIL")
			return "FAIL"

		data = frontierQueue.get()
		pathCost = data[0]
		node = data[1]
		node.x = int(node.x)
		node.y = int(node.y)

		if (targetsite.x == node.x and targetsite.y == node.y):
			parentChildList.append([node, childNodes])
			findParent(landingCoordinate, parentChildList, node, paths)
			paths.append(node)
			writePathIntoFile(paths)
			return "Success"

		visited[node.x][node.y] = True

		childNodes = deque()

		findUCSNeighbor(node, w, h, terrain, threshold, visited, frontierQueue, childNodes, parentChildList, pathCost)

def findUCSNeighbor(node, w, h, terrain, threshold, visited, frontierQueue, childNodes, parentChildList, pathCost):
	for i in range(-1, 2):
		for j in range(-1, 2):
			if (((((node.x + i) >= 0 and (node.x + i) <= (int(w) - 1)) and ((node.y + j) >= 0 and (node.y + j) <= (int(h) - 1))) and (i != 0 or j != 0)) and not isVisited(visited, Coordinates(node.x + i, node.y + j)) and abs((int(terrain[node.x + i][node.y + j]) - int(terrain[node.x][node.y]))) <= int(threshold)):
				neighbor = Coordinates(node.x + i, node.y + j)

				isPresent = False

				if i == 0 or j == 0:
					cost = pathCost + 10
				else:
					cost = pathCost + 14

				isPresent = isVisited(visited, neighbor)

				if isPresent == False:
					frontierQueue.put((cost, neighbor))
					visited[neighbor.x][neighbor.y] = True
					childNodes.append(neighbor)

	parentChildList.append([node, childNodes])

def isVisited(visited, neighbor):
	return visited[neighbor.x][neighbor.y]
	
def findPathsUsingAStar(landingCoordinate, terrain, targetsite, threshold):
	w, h = len(terrain), len(terrain[0])
	count = 0
	pathCost = 0

	frontierQueue = queue.PriorityQueue(0)
	exploredQueue = deque()
	parentChildList = []
	paths = []

	visited = [[False for i in range(0, h)] for j in range(0, w)]

	if (targetsite.x == landingCoordinate.x and targetsite.y == landingCoordinate.y):
		paths.append(landingCoordinate)
		writePathIntoFile(paths)
		return "Success"

	f = pathCost + heuristicFunction(landingCoordinate, targetsite)

	frontierQueue.put((f, (0, landingCoordinate)))

	while True :
		if frontierQueue.empty():
			writePathIntoFile("FAIL")
			return "FAIL"

		data = frontierQueue.get()

#		print(data)
#		input(" ")

		pathCost = data[1][0]
		node = data[1][1]
#		node = Coordinates(0,0)
#		pathCost = 0;
		node.x = int(node.x)
		node.y = int(node.y)

		visited[node.x][node.y] = True

		if (targetsite.x == node.x and targetsite.y == node.y):
			parentChildList.append([node, childNodes])
			findParent(landingCoordinate, parentChildList, node, paths)
			paths.append(node)
			writePathIntoFile(paths)
			return "Success"

		exploredQueue.append(node)

		childNodes = deque()

		
		for i in range(-1, 2):
			for j in range(-1, 2):
				if (((((node.x + i) >= 0 and (node.x + i) <= (int(w) - 1)) and ((node.y + j) >= 0 and (node.y + j) <= (int(h) - 1))) and (i != 0 or j != 0)) and not isVisited(visited, Coordinates(node.x + i, node.y + j)) and abs((int(terrain[node.x + i][node.y + j]) - int(terrain[node.x][node.y]))) <= int(threshold)):
					neighbor = Coordinates(node.x + i, node.y + j)

					isPresent = False

					z = abs((int(terrain[neighbor.x][neighbor.y]) - int(terrain[node.x][node.y])))
					heuristic = heuristicFunction(neighbor, targetsite)
					if i == 0 or j == 0:
						g = pathCost + 10 + z
						f = g + heuristic
					else:
						g = pathCost + 14 + z
						f = g + heuristic

					isPresent = isVisited(visited, neighbor)

					if isPresent == False:
						frontierQueue.put((f, (g , neighbor)))
						visited[neighbor.x][neighbor.y] = True
						childNodes.append(neighbor)

		parentChildList.append([node, childNodes])

def findParent(landingCoordinate, parentChildList, currentParent, paths):
	for parent, children in parentChildList:
		for child in children:
			if(child.x == currentParent.x and child.y == currentParent.y):
				if(parent.x != landingCoordinate.x or parent.y != landingCoordinate.y):
					findParent(landingCoordinate, parentChildList, parent, paths)
					
				paths.append(parent)
				return paths

def writePathIntoFile(output):
	global noOfTargetSites
	noOfTargetSites = noOfTargetSites - 1
#	count1 = noOfTargetSites - 1
	count = len(output)
	if isinstance(output, str):
		outputFile.write(output)
		outputFile.write("\n")
		return
	for coordinates in output:
		count = count - 1
		outputFile.write(str(coordinates.y))
		outputFile.write(",")
		outputFile.write(str(coordinates.x))
		if(count != 0):
			outputFile.write(" ")

	if noOfTargetSites != 0:
		outputFile.write("\n")

def heuristicFunction(currentPosition, targetsite):
	if(abs(currentPosition.x - targetsite.x) < abs(currentPosition.y - targetsite.y)):
		h = abs(currentPosition.x - targetsite.x) * 14 + (abs(abs(currentPosition.x - targetsite.x) - abs(currentPosition.y - targetsite.y)) * 10)
	else:
		h = abs(currentPosition.y - targetsite.y) * 14 + (abs(abs(currentPosition.x - targetsite.x) - abs(currentPosition.y - targetsite.y)) * 10)

	return h

noOfTargetSites = 0
readInputFile()