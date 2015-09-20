import json

def convertToJson(pape,citers):
	position = (pape.xPos,pape.yPos)
	mainDictionary = pape.getDataDict()
	radius = pape.Radius
	mainDictionary['location'] = position
	mainDictionary['radius'] = radius
	mainDictionary['citers'] = citers
	return mainDictionary



def convertAListToPoints(adjList, initPaper, width, length):
	numLevels = 3
	VERTSCALE = 2
	NonNegativeLevels = []
	NonPositiveLevels = []
	k = [1,0.1,0.01,0.001]
	NonNegativeLevels.append([initPaper])
	NonPositiveLevels.append([initPaper])	
	globalCounter = 1
	globalPaperDict = {}
	globalPaperDict[initPaper] = globalCounter
	initPaper.xPos = width/2.
	initPaper.yPos = length/2.

	
	for bigLevel in range(numLevels+1):
		currentLevel = NonNegativeLevels[bigLevel]
		levelSum = 0
		scalingFactor = (float)(2*VERTSCALE**bigLevel)
		for pape in currentLevel:
			levelSum += pape.numCiters
		currentK = k[bigLevel]
		levelPlus1 = []
		i = 1
		for pape in currentLevel:
			pape.yPos = length*1./scalingFactor
			pape.xPos = i*width/((len(currentLevel)+1.0))

			pape.Radius = width*pape.numCiters/(levelSum*1.0)*currentK
			i+=1	
			if pape in adjList:
				for pappe in adjList[pape]:
					if pappe in globalPaperDict:
						pass
					else:
						globalCounter +=1
						globalPaperDict[pappe] = globalCounter
						levelPlus1.append(pappe)
		NonNegativeLevels.append(levelPlus1)
	"""
	print "hi"
	print len(NonNegativeLevels)
	print "yo"
	for x in NonNegativeLevels:
		#print len(x)
		print 'yo'
		for pape in x:
			print pape.name
			print pape.xPos
			print pape.yPos
			print pape.Radius
	"""


	"""
	Level1Sum = 0
	for pape in Level1:  #build level1
		Level1Sum += pape.numCiters
	k1 = 0.01
	i = 1
	Level2 = []
	for pape in Level1:
		pape.yPos = length*1./4.
		pape.Radius = width*pape.numCiters/(Level1Sum*1.0)*k1
		pape.xPos = i*width/((len(Level1)+1)*1.0)
		i+=1
		globalCounter+=1
		globalPaperDict[pape] = globalCounter
		#print (pape.xPos,pape.yPos,pape.Radius)
		for pappe in adjList[pape]
	"""	
	reverseDict = {}
	for key in adjList.keys():
		for e in adjList[key]:
			if e not in reverseDict:
				reverseDict[e] = [key]
			else:
				reverseDict[e].append(key)

	for bigLevel in range(0,numLevels+1):
		#print bigLevel
		currentLevel = NonPositiveLevels[bigLevel]
		levelSum = 0
		scalingFactor = (float)(2*VERTSCALE**bigLevel)
		for pape in currentLevel:
			levelSum += pape.numCiters
		#print bigLevel
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

	finalAns = []
	for i in NonPositiveLevels:
		for j in i:
			finalAns.append(j)
	for i in range(1,len(NonNegativeLevels)):
		for j in NonNegativeLevels[i]:
			finalAns.append(j)

	for i in globalPaperDict.keys():
		#print i.name

	finalerAns = []

	for i in finalAns:
		citers = []
		if i not in adjList:
			pass
		else:
			for j in adjList[i]:
				num = globalPaperDict[j]
				citers.append(num)
		#print i.name
		#print convertToJson(i,citers)
		finalerAns.append(convertToJson(i,citers))

	json_data = json.dumps(finalerAns)
	return json_data





	
	#return finalAns




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
