
# prune
# pruning the tree to avoid overfitting and increase accuracy

import validate
import train

def pruneWrapper(tree, dataset, expected, attrDict):
    treeRoot = tree

    acc = validate.validate(tree, dataset, expected, attrDict)




def prune(root):
    treeRoot = root
    acc = perfCheck(treeRoot)  # accuracy without pruning

    for branch in tree['branch']:


    pruneOrNot = False    # when pruneOrNot is true, this means this child branch is a leaf node and therefore can be pruned
    # terminatin condition
    if len(root.branch) == 0:
        return True, root
    else:
        branchLength = len(root.branch)
        for i in range(branchLength):
            pruneOrNot, child = prune(root.branch[i])  # child is necessary for undoing removal of a node
            if pruneOrNot:
                root.branch[i] = none
                if (perfCheck(treeRoot) > acc):   # if accuracy better, update the accuracy measure
                    acc = perfCheck(treeRoot)
                else:                             # if accuracy worse, undo the removal of the child node and continue the loop
                    root.addBranch(child)   
        return False, root


