import sys
import array
import Queue
import math
import copy
import time

PUZZLE_SIZE = 25
PUZZLE_WIDTH = math.sqrt(PUZZLE_SIZE)
global depth, boardNum, startTime


# Reads file in line by line
def fileRead(fileName):
	with open(fileName, "r") as f:
		s = ""
		for line in f:
			s += line
		return s

# Reads in the next puz from the fileString
def nextBoard(fileStr, puz):
	if boardNum < 10:
		fileStr = fileStr[9:]
	else:
		fileStr = fileStr[10:]

	i = 25
	while i != 0:
		num = fileStr[0]
		if fileStr[1].isdigit():
			num += fileStr[1]
			fileStr = fileStr[3:]
		else: 
			fileStr = fileStr[2:]
		puz.append(int(num))
		i -= 1
	return fileStr

# Returns the index of the zero in array
def findZero(puzzle):
	i = 0
	for x in puzzle:
		if x == 0:
			return i
		else:
			i += 1
		# return i if x == 0 else i++

# Switches to items in array
def switch(array, zero, move):
	a = copy.deepcopy(array)
	a[zero] = a[move]
	a[move] = 0
	return a

# Returns the given array values as a concat string
def arrayToString(array):
	s = ""
	for x in array:
		s += str(x)
	return s

# Checks if puz is present in opposite queue then returns
def addToHash(array, hashAdd, hashCheck, queueAdd, qsize):
	s = arrayToString(array)
	# Checks for a puz match in opposite Hash
	if s in hashCheck:
		if array == hashCheck[s]:
			print "Match found, Depth =", depth," Nodes =", (len(hashAdd) + len(hashCheck))
			print("--- %s seconds ---" % (time.time() - startTime))
			return True

	# If there was no match new board is added to Hash and Queue
	elif not(s in hashAdd):
		hashAdd[s] = array
		queueAdd.put(array)
		qsize += 1
	return False

# Adds next level to queue
def addDepth(hashAdd, hashCheck, queue, qsize):
	qsize = queue.qsize()
	while qsize != 0:
		a = queue.get()
		qsize -= 1
		i = findZero(a)
		i5 = i % PUZZLE_WIDTH

		# Logic for puzzule moves
		if i == 0 or i5 != PUZZLE_WIDTH - 1 : 
			if addToHash(switch(a, i, i + 1), hashAdd, hashCheck, queue, qsize): return True
		if i5 != 0: 
			if addToHash(switch(a, i, i - 1), hashAdd, hashCheck, queue, qsize): return True
		if i >= PUZZLE_WIDTH: 
			if addToHash(switch(a, i, i - 5), hashAdd, hashCheck, queue, qsize): return True
		if i < PUZZLE_SIZE - PUZZLE_WIDTH: 
			if addToHash(switch(a, i, i + 5), hashAdd, hashCheck, queue, qsize): return True
	return False

# Resets all variables for next search
def reset(h1, h2, q1, q2):
	h1.clear()
	h2.clear()
	depth = 0

# Begins by reading the file to a string
if len(sys.argv) < 1:
	sys.exit("File Name required")
else:
	fileStr = fileRead(sys.argv[1])

boardNum = 1

comPuz = array.array('b', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])

# Hashes and Queues
hashTop = dict()
hashBottom = dict()
queueTop = Queue.Queue()
queueBottom = Queue.Queue()

# Main loop. Must be terminated manually
while 1:
	startTime = time.time()
	puz = array.array('b')
	fileStr = nextBoard(fileStr, puz)

	reset(hashTop, hashBottom, queueTop, queueBottom)
	queueTop = Queue.Queue()
	queueBottom = Queue.Queue()

	# Adds first items to hashes and queues
	depth, topSize, bottomSize = 0, 0, 0
	addToHash(puz, hashTop, hashBottom, queueTop, topSize)
	print "Board Number =", boardNum
	boardNum += 1
	addToHash(comPuz, hashBottom, hashTop, queueBottom, bottomSize)

	# Secondary loop. Adds depths and only breaks when a result is found.
	while 1:
		depth += 1
		if addDepth(hashTop, hashBottom, queueTop, topSize): break
		depth += 1
		if addDepth(hashBottom, hashTop, queueBottom, bottomSize): break




