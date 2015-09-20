import json

def convertToJson(pape,citers): #This method converts things to a dict
	position = (pape.xPos,pape.yPos)
	mainDictionary = pape.getDataDict()
	radius = pape.Radius
	mainDictionary['location'] = position
	mainDictionary['radius'] = radius
	mainDictionary['citers'] = citers
	return mainDictionary



def convertAListToPoints(adjList, initPaper, width, length):
	#This is the main method for this file. It returns a JSON with info
	numLevels = 3 #depth of tree
	VERTSCALE = 2 #the smaller, the more spread out
	NonNegativeLevels = []
	NonPositiveLevels = []
	k = [1,0.1,0.01,0.001] #constants that determine bubble size
	NonNegativeLevels.append([initPaper])
	NonPositiveLevels.append([initPaper])	
	globalCounter = 1
	globalPaperDict = {} #Ends up containing every paper.
	globalPaperDict[initPaper] = globalCounter
	initPaper.xPos = width/2. #Center of page
	initPaper.yPos = length/2.

	
	for bigLevel in range(numLevels+1): #bigLevel is the level of the tree
		currentLevel = NonNegativeLevels[bigLevel]
		levelSum = 0
		scalingFactor = (float)(2*VERTSCALE**bigLevel) #depends on level oftree
		for pape in currentLevel:
			levelSum += pape.numCiters #normalize numciters across each depth
		currentK = k[bigLevel]
		levelPlus1 = [] #build the next level of the tree
		i = 1
		for pape in currentLevel:
			pape.yPos = length*1./scalingFactor #Determines position
			pape.xPos = i*width/((len(currentLevel)+1.0))
			#scale radius by k as well as by numCiters/total citations
			pape.Radius = width*pape.numCiters/(levelSum*1.0)*currentK
			i+=1	
			if pape in adjList:
				for pappe in adjList[pape]:
					if pappe in globalPaperDict:
						pass
					else:
						globalCounter +=1
						globalPaperDict[pappe] = globalCounter
						levelPlus1.append(pappe) #build next level of tree
		NonNegativeLevels.append(levelPlus1) 

	reverseDict = {} #Go the reverse direction to find predecessors
	for key in adjList.keys():
		for e in adjList[key]:
			if e not in reverseDict:
				reverseDict[e] = [key]
			else:
				reverseDict[e].append(key)

	for bigLevel in range(0,numLevels+1): #perform the same shits as above
		currentLevel = NonPositiveLevels[bigLevel]
		levelSum = 0
		scalingFactor = (float)(2*VERTSCALE**bigLevel)
		for pape in currentLevel:
			levelSum += pape.numCiters
		currentK = k[bigLevel]
		levelPlus1 = []
		i = 1
		for pape in currentLevel:
			pape.yPos = length-length*1./scalingFactor
			pape.xPos = i*width/((len(currentLevel)+1.0))
			pape.Radius = width*pape.numCiters/(levelSum*1.0)*currentK
			i+=1	
			if pape in reverseDict:
				for pappe in reverseDict[pape]:
					if pappe in globalPaperDict:
						pass
					else:
						globalCounter +=1
						globalPaperDict[pappe] = globalCounter
						levelPlus1.append(pappe)
		NonPositiveLevels.append(levelPlus1)

	finalAns = [] #Create the final ans, list of people
	for i in NonPositiveLevels:
		for j in i:
			finalAns.append(j)
	for i in range(1,len(NonNegativeLevels)):
		for j in NonNegativeLevels[i]:
			finalAns.append(j)

	#for i in globalPaperDict.keys():

	finalerAns = [] #This is the thing we will return

	for i in finalAns:
		citers = []
		if i not in adjList:
			pass
		else:
			for j in adjList[i]:
				num = globalPaperDict[j] 
				citers.append(num)
		finalerAns.append(convertToJson(i,citers)) #first method

	json_data = json.dumps(finalerAns)
	return json_data #BLAM and you're done.








class Paper:
	def __init__(self, name):
		self.name = name
		self.numCiters = 10
		self.xPos = -10
		self.yPos = -10

	def getDataDict(self):
		return {'what':'hey'}

adjList = {}
paperA = Paper('A')
paperB = Paper('B')
paperC = Paper('C')
paperD = Paper('E')
paperE = Paper('E')
paperF = Paper('F')
paperG = Paper('G')
paperH = Paper('H')
paperI = Paper('I')
paperJ = Paper('J')
paperK = Paper('K')
paperL = Paper('L')
paperM = Paper('M')
paperN = Paper('N')
paperO = Paper('O')
paperP = Paper('P')
paperQ = Paper('Q')
paperR = Paper('R')
paperS = Paper('S')
adjList[paperA] = [paperB,paperC]
adjList[paperC] = [paperE,paperF,paperG]
adjList[paperB] = [paperH,paperE]
adjList[paperL] = [paperI] 
adjList[paperI] = [paperA]
adjList[paperM] = [paperK,paperJ]
adjList[paperK] = [paperA]
adjList[paperN] = [paperK]
adjList[paperO] = [paperK]
adjList[paperJ] = [paperA]
adjList[paperH] = [paperS]
initPaper = paperA
convertAListToPoints(adjList,initPaper, 100, 100)
