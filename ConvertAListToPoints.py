def convertAListToPoints(adjList, initPaper, width, length):
	numLevels = 3
	VERTSCALE = 1.5
	NonNegativeLevels = []
	NonPositiveLevels = []
	k = [1,0.1,0.01,0.001]
	NonNegativeLevels.append([initPaper])
	NonPositiveLevels.append([initPaper])	
	#print NonNegativeLevels
	globalCounter = 1
	globalPaperDict = {}
	globalPaperDict[initPaper] = globalCounter
	#print globalPaperDict
	initPaper.xPos = width/2.
	initPaper.yPos = length/2.
	#Level1 = adjList[initPaper]
	#print NonNegativeLevels[0][0].xPos
	#print Level1
	
	"""
	for bigLevel in range(numLevels-1):
		nodeList = NonNegativeLevels[bigLevel]
		tempNodeList = []
		for i in range(len(nodeList)):
			for x in adjList[i]:
				adjList[x]:

	"""
	
	for bigLevel in range(numLevels+1):
		currentLevel = NonNegativeLevels[bigLevel]
		#print currentLevel
		levelSum = 0
		scalingFactor = (float)(2*VERTSCALE**bigLevel)
		for pape in currentLevel:
			levelSum += pape.numCiters
		currentK = k[bigLevel]
		levelPlus1 = []
		i = 1
		for pape in currentLevel:
			#print pape.name
			pape.yPos = length*1./scalingFactor
			pape.xPos = i*width/((len(currentLevel)+1.0))
			#print pape.xPos
			#print pape.yPos
			pape.Radius = width*pape.numCiters/(levelSum*1.0)*currentK
			#print pape.Radius
			i+=1	
			#globalCounter+=1
			#globalPaperDict[pape] = globalCounter
			if pape in adjList:
				for pappe in adjList[pape]:
					if pappe in globalPaperDict:
						pass
					else:
						globalCounter +=1
						globalPaperDict[pappe] = globalCounter
						levelPlus1.append(pappe)
						#print len(levelPlus1)
				#print levelPlus1
		NonNegativeLevels.append(levelPlus1)
				#print NonNegativeLevels
	#print NonNegativeLevels
	#print NonNegativeLevels[2]#[2].xPos
	#print len(NonNegativeLevels)
	print globalCounter
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
		print bigLevel
		currentLevel = NonPositiveLevels[bigLevel]
		#print currentLevel
		levelSum = 0
		scalingFactor = (float)(2*VERTSCALE**bigLevel)
		for pape in currentLevel:
			levelSum += pape.numCiters
		print bigLevel
		currentK = k[bigLevel]
		levelPlus1 = []
		i = 1
		for pape in currentLevel:
			#print pape.name
			pape.yPos = length-length*1./scalingFactor
			pape.xPos = i*width/((len(currentLevel)+1.0))
			#print pape.xPos
			#print pape.yPos
			pape.Radius = width*pape.numCiters/(levelSum*1.0)*currentK
			#print pape.Radius
			i+=1	
			#globalCounter+=1
			#globalPaperDict[pape] = globalCounter
			if pape in reverseDict:
				for pappe in reverseDict[pape]:
					if pappe in globalPaperDict:
						pass
					else:
						globalCounter +=1
						globalPaperDict[pappe] = globalCounter
						levelPlus1.append(pappe)
						#print len(levelPlus1)
				#print levelPlus1
		NonPositiveLevels.append(levelPlus1)
				#print NonNegativeLevels
	#print NonNegativeLevels
	#print NonNegativeLevels[2]#[2].xPos
	#print len(NonNegativeLevels)
	#print globalCounter

	finalAns = []
	for i in NonPositiveLevels:
		for j in i:
			#print (j.name,j.xPos,j.yPos,j.Radius)
			finalAns.append(j)
	for i in range(1,len(NonNegativeLevels)):
		for j in NonNegativeLevels[i]:
			finalAns.append(j)

	for i in finalAns:
		print (i.name,i.xPos,i.yPos,i.Radius) 

	return finalAns




class Paper:
	def __init__(self, name):
		self.name = name
		self.numCiters = 10
		self.xPos = -10
		self.yPos = -10

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
