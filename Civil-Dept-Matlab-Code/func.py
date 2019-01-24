import json
import numpy as np

def getCordinates():
    x=[0, 6, 12, 18, 24, 18, 12, 6]
    y=[0, 0, 0, 0, 0, 6, 6, 6]
    return x, y

def getECM():
    ECM=[[1, 2, 3, 4, 5, 6, 7, 1, 2, 2, 3, 4, 4], [2, 3, 4, 5, 6, 7, 8, 8, 8, 7, 7, 7, 6]]
    return np.array(ECM, dtype = int).T-1

def get_angle():
    pi = np.pi
    return np.array([0, 0, 0, 0, pi / 4 * 3, pi, pi, pi / 4, pi / 2, pi / 4, pi / 2, pi / 4 * 3, pi / 2])

def get_k_global(A, E, L, ang):
    k = get_k_local(ang)
    const = A * E / L
    print(const)
    return const*k

def get_BC():
    return np.array([1, 2, 10], dtype=int)-1  # ; %restrained dof

def get_force_vect():
    return np.array([0, 0, 0, -200, 0, -100, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0])


def get_k_local(ang):
    c = np.cos(ang)
    s = np.sin(ang)

    cc = c*c
    ss = s*s
    cs = s*c

    arr = np.array([[cc, cs, -cc, -cs],
                    [cs, ss, -cs, -ss],
                    [-cc, -cs, cc, cs],
                    [-cs, -ss, cs, ss]])

    return arr


def readFile(fileName):
    '''

    :param fileName: The json file name
    :return: Return a dictionary of the file content
    '''
    with open(fileName) as json_file:
        json_data = json.load(json_file)
        return json_data

def writeFile(data, fileName):
    '''

    :param data: disctionary to be written to file
    :param fileName: The json file name
    '''
    with open(fileName, 'w') as file:
        json.dump(data, file, indent=4)




