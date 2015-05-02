
# prune
# pruning the tree to avoid overfitting and increase accuracy

import validate
import train

def pruneWrapper(tree, dataset, expected, attrDict):
    if len(tree['branch'].keys()) == 0:
        val = tree['label']
        sumVal = 0
        for entry in expected:
            if val == entry:
                sumVal += 1
        return tree, sumVal
    else:
        if len(expected) == 0:
            newLeaf = train.dTreeNode(1)
            return newLeaf.info, 0
        #print tree['decision']
        if attrDict[tree['decision']] == 'c':
            subsets, occurence = makeNewContinuousSubset(tree, dataset)
        else:
            subsets, occurence = train.makeSubsetsDiscrete(dataset, tree['decision'])

        total = 0

        for subset in subsets.keys():
            labelSubset = []
            dataSubset = []
            for index in subsets[subset]:
                dataSubset.append(dataset[index])
                labelSubset.append(expected[index])
            subtree, subAcc = pruneWrapper(tree['branch'][subset], dataSubset, labelSubset, attrDict)
            tree['branch'][subset] = subtree
            total += subAcc
        totAcc = total / len(expected)
        # validate, prune
        prunedAcc = sum(expected) / len(expected)
        leaf = 1
        if prunedAcc < 0.5:
            prunedAcc = 1 - prunedAcc
            leaf = 0

        if prunedAcc > totAcc:
            newLeaf = train.dTreeNode(leaf)
            return newLeaf.info, prunedAcc*len(expected)
        else:
            return tree, total

def makeNewContinuousSubset(tree, dataset):
    attr = tree['decision']
    # make a subset again .. F
    subsets = {}
    knownVal = {}

    if tree['decision'] == attr:
        bins = tree['branch'].keys()
        bins.sort()

        for i in range(len(bins)):
            subsets[bins[i]] = []
            knownVal[bins[i]] = 0

        for i in range(len(bins)):
            for j in range(len(dataset)):
                myValue = dataset[i][tree['decision']]
                if i == 0 and bins[i] > myValue:
                    subsets[bins[i]].append(j)
                    knownVal[bins[i]] += 1
                elif i == (len(bins) - 1):
                    subsets[bins[i]].append(j)
                    knownVal[bins[i]] += 1
                elif bins[i] < myValue and bins[i+1] > myValue:
                    subsets[bins[i]].append(j)
                    knownVal[bins[i]] += 1

    return subsets, knownVal

