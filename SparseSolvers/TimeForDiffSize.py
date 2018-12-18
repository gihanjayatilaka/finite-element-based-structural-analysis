import numpy as np
import scipy
import scipy.sparse
import scipy.sparse.linalg as la
import sys
import time


if __name__ == "__main__":
    NN=range(1000,int(sys.argv[1]),1000)
    TIME=np.zeros((len(NN)),dtype=np.float32)
    RESIDUE=np.zeros((len(NN)),dtype=np.float32)
    NUMBERS_PER_ROW=int(sys.argv[2])
    ALGORITHM = sys.argv[3]

    for n in range(len(NN)):
        N=NN[n]
        A=np.zeros((N,N),dtype=np.float32)
        y=np.zeros((N),dtype=np.float32)
        x=np.zeros(N,dtype=np.float32)

        for r in range(N):
            A[r, r] = np.random.uniform(-100, 100)
            for c in range(NUMBERS_PER_ROW-1):
                cc=np.mod((np.random.randint(-1*NUMBERS_PER_ROW/2,NUMBERS_PER_ROW/2)),N)
                A[r,cc]=np.random.uniform(-100,100)
            y[r]=np.random.uniform(-100,100)


        xCorrect = np.linalg.solve(A, y)

        startT = time.process_time()
        if ALGORITHM=="general":
            x=np.linalg.solve(A,y)
        elif ALGORITHM=="sparse":
            x=la.spsolve(A,y)
        elif ALGORITHM=="biconjugate-gradient-iter":
            x=la.bicg(A,y)
            print(x.shape)
            print(A.shape,y.shape)
        elif ALGORITHM=="biconjugate-gradient-stabilized":
            x=la.bicgstab(A,y)
        elif ALGORITHM=="conjugate-gradient-iter":
            x=la.cg(A,y)
        elif ALGORITHM == "conjugate-gradient-squared":
            x = la.cgs(A, y)
        elif ALGORITHM == "conjugate-gradient-squared":
            x = la.cgs(A, y)
        elif ALGORITHM == "generalized-min-res":
            x = la.gmres(A, y)
        elif ALGORITHM == "improved-generalized-min-res":
            x = la.lgmres(A, y)
        elif ALGORITHM =="min-res":
            x=la.minres(A,y)
        elif ALGORITHM =="quasi-min-res":
            x=la.qmr(A,y)


        endT=time.process_time()

        '''print(x)
        print(xCorrect)'''
        residue=np.average(np.average(np.abs(x-xCorrect)))/np.average(np.average(np.abs(xCorrect)))

        print("Algorith: "+ALGORITHM+"\tMat Size: "+str(N)+"\tTime: "+str(endT-startT)+"\t Residue: "+str(residue))

        TIME[n]=endT-startT
        RESIDUE[n]=residue

    print("Time List:")
    for n in range(len(NN)):
        print("%.10f"%TIME[n])

    print("Residue List:")
    for n in range(len(NN)):
        print("%.10f"%RESIDUE[n])


