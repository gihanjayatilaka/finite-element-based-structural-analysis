import os
import sys

parent = os.path.dirname(os.getcwd())
sys.path.append(parent)

import unittest
import numpy as np

from Truss_class import Truss
from JsonRead import readFile, writeFile
from Test import deeptest

class Test_Truss_integration(unittest.TestCase):

    def test_main(self):
        self.maxDiff = None
        struct_files = ['structure00.json', 'structure01.json']
        out_files = ['output00.json', 'output01.json']

        for x, y in zip(struct_files, out_files):
            structure = readFile('Structures/' + x)
            truss = Truss(structure)
            d, fr = truss.main_func()
            out = truss.gen_output(d, fr)

            deeptest.assertDeepAlmostEqual(self, readFile('Expected_output/' + y), out)


if __name__ == '__main__':
    unittest.main()