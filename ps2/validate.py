from __future__ import division
import random
import train

def validate(tree, vData, expected, attrDict):
	predicted = tree.validate(vData, attrDict)
	correct = 0
	#dumb = []
	#print predicted
	for i in range(len(expected)):
		if expected[i] == predicted[i]:
			correct += 1
	#	if expected[i] == 0:
#			correct += 1
	print "RESULT!!!!"
	print correct/len(expected)



def nFold(allData, expected, attrDict, N):
	totalLength = len(expected)
	toChoose = int(totalLength / N)
	indices = random.sample(xrange(0,totalLength), totalLength)

	expectedLists = []
	vLists = []
	tLists = []
	tLabelLists = []

	indexLists = []
	for i in range(N):
		indexLists.append(indices[i*toChoose:(i+1)*toChoose])

	for i in range(N):
		expectedLists.append([])
		vLists.append([])
		for index in indexLists[i]:
			expectedLists[i].append(expected[index])
			vLists[i].append(allData[index])

	for i in range(N):
		tLists.append([])
		tLabelLists.append([])
		for j in range(N):
			if i != j:
				tLists[i].extend(vLists[j])
				tLabelLists[i].extend(expectedLists[j])

	sumAcc = 0
	for i in range(N):
		attrKeys = attrDict.keys()
		tTree = train.GenerateDTree(tLists[i], attrKeys, attrDict, tLabelLists[i])
		sumAcc += validate(tTree, vLists[i], expectedLists[i], attrDict)

	print "N-VALIDATION RESULT:"
	print sumAcc/N