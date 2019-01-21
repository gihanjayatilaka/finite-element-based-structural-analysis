import json
import sys
import numpy as np

DOF_PER_NODE = 6
NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE * NODES_PER_ELEMENT


def buildLocalK(elementTypeDict):
    # To be implemented
    if True or elementTypeDict=='':
        ar=np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))


        return ar


def buildNode(nodeDict):
    return np.array([nodeDict['x'], nodeDict['y'], nodeDict['z']])


def rotateK(k, ang):
    if True:
        k[0,0]=0
        k[0,1]=0
        k[0,2]=0
        k[0,3]=0
        k[0,4]=0
        k[0,5]=0

        k[1,0]=0
        k[1,1]=0
        k[1,2]=0
        k[1,3]=0
        k[1,4]=0
        k[1,5]=0

        k[2,0]=0
        k[2,1]=0
        k[2,2]=0
        k[2,3]=0
        k[2,4]=0
        k[2,5]=0

        k[3,0]=0
        k[3,1]=0
        k[3,2]=0
        k[3,3]=0
        k[3,4]=0
        k[3,5]=0

        k[4,0]=0
        k[4,1]=0
        k[4,2]=0
        k[4,3]=0
        k[4,4]=0
        k[4,5]=0


        k[5,0]=0
        k[5,1]=0
        k[5,2]=0
        k[5,3]=0
        k[5,4]=0
        k[5,5]=0



    return k


def angle(startNode, endNode):
    ''' To be implemented
        This function returns the 3 angles along 3 axes
    '''
    return np.array([0, 0, 0], dtype=np.float32)




if __name__ == "__main__":
    with open(sys.argv[1]) as data_file:
        data = json.load(data_file)

    noNodes = data['no_of_nodes']
    noFixedNodes = data['no_of_fixed_points']
    noElements = data['no_of_elements']
    noElementTypes = data['no_of_crosssection_types']
    noLoads=data['no_of_loads']

    kLocal = #  Make a list of *functions* of the size
    #           (noElementTypes, DOF_PER_ELEMENT, DOF_PER_ELEMENT)


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

    for n in range(nodeIsFixed.shape[0] - 1, -1, -1):
        if not nodeIsFixed[n]:
            np.delete(kGlobal, n, 0)  # delete row
            np.delete(kGlobal, n, 1)  # delete col



    print(nodes.shape, nodes)
    print(kLocal.shape, kLocal)






