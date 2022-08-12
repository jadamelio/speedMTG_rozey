#takes a spreadsheet sorted by time entry
f = open("archermethod.csv", 'r')

data = []
#Loading
i = 0
for line in f:
	if i >0:
		bit = line.split(',')
		bit[0] = int(bit[0])
		bit[1] = int(bit[1])
		bit[2] = int(bit[2])
		bit[3] = int(bit[3].replace("\n", ""))
		data.append(bit)
		#print(data[-1])
	i+=1
#Finds places where someone's timer should be running
gapStarts = []
for i in range(1,len(data)):
	previousGlobalTime = data[i-1][0]
	mostRecentGlobalTime = data[i][0]
	print((mostRecentGlobalTime - previousGlobalTime)/1000)

	threshold_seconds = .1
	if (mostRecentGlobalTime - previousGlobalTime)/1000 > threshold_seconds: #Gap occured starting at previousGlobal time, comparing seconds
		gapStarts.append(i-1)
print(len(gapStarts))

theoreticalPoints = []
clock7_lastKnown = 0
clock14_lastKnown = 0
for i in range(len(gapStarts)-1):
	if data[gapStarts[i]][2] == 7:
		clock7_lastKnown = data[gapStarts[i]][3]
	else: 
		clock14_lastKnown = data[gapStarts[i]][3]


	lastKnowTime = data[gapStarts[i]][0]
	lastKnowPriority = data[gapStarts[i]][1]
	nextReading = data[gapStarts[i+1]][0]#in practice we don't know this, but we loop until we do, to demonstrate, nextReading is only used to terminate loop

	
	resolution_mS = (threshold_seconds)*1000
	j = 1

	newPoint = lastKnowTime + resolution_mS*j#Creates a new data point global timestamp
	while newPoint < nextReading:
		
		clockID = ''
		timeToWrite = 0
		if lastKnowPriority == 1:
			clockID = "7"
			timeToWrite = clock7_lastKnown + resolution_mS*j#adjusts player clock
		else:
			clockID = "14"
			timeToWrite = clock14_lastKnown + resolution_mS*j#adjusts player clock
		theoreticalPoints.append([newPoint,lastKnowPriority,clockID, timeToWrite ])

		j+=1
		newPoint = lastKnowTime + resolution_mS*j

		
		

nf = open("hereItIsBaby.csv", 'w')

for i in range(len(theoreticalPoints)):
	tp = theoreticalPoints[i]
	nf.write(str(tp[0]) + "," +str(tp[1]) + "," +str(tp[2]) + "," +str(tp[3]) + "," + "theoreticalPoints" + "," + "\n")
for i in range(len(data)):
	tp = data[i]
	nf.write(str(tp[0]) + "," +str(tp[1]) + "," +str(tp[2]) + "," +str(tp[3]) + "," + "observedPoints" + "," +"\n")


