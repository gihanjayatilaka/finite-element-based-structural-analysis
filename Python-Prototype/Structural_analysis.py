from JsonRead import readFile,writeFile
from Truss_class import Truss
import sys

if __name__ == "__main__":
    structure = readFile(sys.argv[1])
    truss = Truss(structure)

    # nodal deformation and Internal Forces
    d, fr = truss.main_func()

    out = truss.gen_output(d, fr)
    writeFile(out, sys.argv[2])

