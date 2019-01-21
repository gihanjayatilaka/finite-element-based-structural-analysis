'''
python FullProg2.py ../Structure-Files/structure00/structure00.json ./aa.txt



'''

import json
import sys
import numpy as np
import numpy.linalg as la

DOF_PER_NODE = 6
NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE * NODES_PER_ELEMENT


def dumpResultToFile(displacementVector,dumpFileName):
    dictToDump={}
    dispList=[]

    for nodeNo in range(np.shape(displacementVector)[0]/DOF_PER_NODE):
        tempDict={}
        tempDict['point_id']=nodeNo

        tempDictTrans={}
        tempDictRot={}
        tempDictTrans['x']=displacementVector[DOF_PER_NODE*nodeNo + 0]
        tempDictTrans['y']=displacementVector[DOF_PER_NODE*nodeNo + 1]
        tempDictTrans['z']=displacementVector[DOF_PER_NODE*nodeNo + 2]
        tempDictRot['x']=displacementVector[DOF_PER_NODE*nodeNo + 3]
        tempDictRot['y']=displacementVector[DOF_PER_NODE*nodeNo + 4]
        tempDictRot['z']=displacementVector[DOF_PER_NODE*nodeNo + 5]

        tempDict['translation']=tempDictTrans
        tempDict['rotation']=tempDictRot

        dispList.append(tempDict)

    dictToDump['displacement']=dispList

    with open(dumpFileName, 'w') as file:
        json.dump(data, file, indent=4)
    print("Finished writing to file")


def buildLocalK(elementTypeDict):
    # To be completed
    if True or elementTypeDict=='':
        ar=np.full((DOF_PER_ELEMENT, DOF_PER_ELEMENT),1.0)
        return ar

def linearSolver(A,Y):
    '''
        This is the heaviest function in the program
        We are using a generic approach here (first implementation)
        We hope someone will improve this :-)
    '''
    return np.dot(la.inv(A), Y)

def buildNode(nodeDict):
    return np.array([nodeDict['x'], nodeDict['y'], nodeDict['z']])


def rotateK(k, ang):
    if True:
        k[0,0]*=1.0
        k[0,1]*=1.0
        k[0,2]*=1.0
        k[0,3]*=1.0
        k[0,4]*=1.0
        k[0,5]*=1.0

        k[1,0]*=1.0
        k[1,1]*=1.0
        k[1,2]*=1.0
        k[1,3]*=1.0
        k[1,4]*=1.0
        k[1,5]*=1.0

        k[2,0]*=1.0
        k[2,1]*=1.0
        k[2,2]*=1.0
        k[2,3]*=1.0
        k[2,4]*=1.0
        k[2,5]*=1.0

        k[3,0]*=1.0
        k[3,1]*=1.0
        k[3,2]*=1.0
        k[3,3]*=1.0
        k[3,4]*=1.0
        k[3,5]*=1.0

        k[4,0]*=1.0
        k[4,1]*=1.0
        k[4,2]*=1.0
        k[4,3]*=1.0
        k[4,4]*=1.0
        k[4,5]*=1.0


        k[5,0]*=1.0
        k[5,1]*=1.0
        k[5,2]*=1.0
        k[5,3]*=1.0
        k[5,4]*=1.0
        k[5,5]*=1.0



    return k


def angle(startNode, endNode):
    #This function returns the 3 angles along 3 axes

    L=np.sqrt(np.sum(np.power(endNode-startNode,2)))
    an=np.ndarray((3),dtype=np.float32)
    an[0]=np.arccos((endNode[0]-startNode[0])/L)
    an[1]=np.arccos((endNode[1]-startNode[1])/L)
    an[2]=np.arccos((endNode[2]-startNode[2])/L)


    return an




if __name__ == "__main__":
    with open(sys.argv[1]) as data_file:
        data = json.load(data_file)

    noNodes = data['no_of_nodes']
    noFixedNodes = data['no_of_fixed_points']
    noElements = data['no_of_elements']
    noElementTypes = data['no_of_crosssection_types']
    noLoads=data['no_of_loads']

    kLocal = np.zeros((noElementTypes,DOF_PER_ELEMENT,DOF_PER_ELEMENT),dtype=np.float32)

    nodes = np.ndarray((noNodes, 3), dtype=np.float32)

    kGlobal = np.ndarray((noNodes * DOF_PER_NODE, noNodes * DOF_PER_NODE))
    fGlobal = np.ndarray((noNodes * DOF_PER_NODE))

    for n in range(noNodes):
        nodes[n] = buildNode(data['nodes'][n])

    for eType in range(noElementTypes):
        kLocal[eType] = buildLocalK(data['element_type'][eType])

    for e in range(noElements):
        ele = data['elements'][e]
        startNode = ele['start_node_id']
        endNode = ele['end_node_id']
        eleType = ele['element_type']
        k = rotateK(kLocal[eleType], angle(nodes[startNode], nodes[endNode]))

        y1 = DOF_PER_NODE * startNode
        y2 = y1 + DOF_PER_NODE
        x1 = DOF_PER_NODE * startNode
        x2 = x1 + DOF_PER_NODE
        kGlobal[y1:y2, x1:x2] += k[:DOF_PER_NODE, :DOF_PER_NODE]

        y1 = DOF_PER_NODE * startNode
        y2 = y1 + DOF_PER_NODE
        x1 = DOF_PER_NODE * endNode
        x2 = x1 + DOF_PER_NODE
        kGlobal[y1:y2, x1:x2] += k[:DOF_PER_NODE, DOF_PER_NODE:]

        y1 = DOF_PER_NODE * endNode
        y2 = y1 + DOF_PER_NODE
        x1 = DOF_PER_NODE * startNode
        x2 = x1 + DOF_PER_NODE
        kGlobal[y1:y2, x1:x2] += k[DOF_PER_NODE:, :DOF_PER_NODE]

        y1 = DOF_PER_NODE * endNode
        y2 = y1 + DOF_PER_NODE
        x1 = DOF_PER_NODE * endNode
        x2 = x1 + DOF_PER_NODE
        kGlobal[y1:y2, x1:x2] += k[DOF_PER_NODE:, DOF_PER_NODE:]


    for l in range(noLoads):
        load=data['loads'][l]
        node=load['point_id']
        fGlobal[node*DOF_PER_NODE+0]=load['force']['x']
        fGlobal[node*DOF_PER_NODE+1]=load['force']['y']
        fGlobal[node*DOF_PER_NODE+2]=load['force']['z']
        fGlobal[node*DOF_PER_NODE+3]=load['torque']['x']
        fGlobal[node*DOF_PER_NODE+4]=load['torque']['y']
        fGlobal[node*DOF_PER_NODE+5]=load['torque']['z']









    nodeIsFixed = np.full((DOF_PER_NODE * noNodes), False, dtype=bool, )

    for f in range(noFixedNodes):
        n = data['fixed_points'][f]['point_id']
        if data['fixed_points'][f]['translation']['x']:
            nodeIsFixed[n + 0] = True
        if data['fixed_points'][f]['translation']['y']:
            nodeIsFixed[n + 1] = True
        if data['fixed_points'][f]['translation']['z']:
            nodeIsFixed[n + 2] = True
        if data['fixed_points'][f]['rotation']['x']:
            nodeIsFixed[n + 3] = True
        if data['fixed_points'][f]['rotation']['y']:
            nodeIsFixed[n + 4] = True
        if data['fixed_points'][f]['rotation']['z']:
            nodeIsFixed[n + 5] = True

    '''
    These variables are useful in converting between the reduced 
        and original matrices
    '''
    reducedNodeNoToOriginalNodeNo=np.zeros((noNodes*DOF_PER_NODE - noFixedNodes),dtype=np.int32)
    tempIdx=noNodes*DOF_PER_NODE - noFixedNodes-1

    kGlobalReduced=np.copy(kGlobal)
    fGlobalReduced=np.copy(fGlobal)
    for n in range(nodeIsFixed.shape[0] - 1, -1, -1):
        if not nodeIsFixed[n]:
            np.delete(kGlobalReduced, n, 0)  # delete row
            np.delete(kGlobalReduced, n, 1)  # delete col

            np.delete(fGlobalReduced,n,0) #Delete row
        else:
            reducedNodeNoToOriginalNodeNo[tempIdx]=n
            tempIdx-=1

    dispGlobalReduced=linearSolver(kGlobal,fGlobal)
    dispGlobal=np.zeros(noNodes*DOF_PER_NODE,dtype=np.float32)


    for idx in range(dispGlobalReduced.shape[0]):
        dispGlobal[reducedNodeNoToOriginalNodeNo[idx]]=dispGlobalReduced[idx]

    dumpResultToFile(dispGlobal,sys.argv[2])













    print(fGlobal.shape)
    print(kGlobal.shape)
    print(dispGlobal.shape)





