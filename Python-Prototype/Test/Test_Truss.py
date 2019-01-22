import sys

sys.path.append('C:/Users/User/Documents/GitHub/finite-element-based-structural-analysis/Python-Prototype')

import unittest
from Truss_class import Truss
import numpy as np
import JsonRead

class Test_Truss(unittest.TestCase):

    def test_area(self):
        type = ["rectangle", "rectangle", "circle", "circle"]
        dim = [
            {"y": 5.2, "z": 2},
            {"y": 0, "z": -1},
            {"radius": 4},
            {"radius": .2}
        ]

        ans = [10.4, 0, 50.265482457436, 0.125663706143]

        for t, d, a in zip(type, dim, ans):
            self.assertAlmostEqual(Truss.get_area(None, t, d), a)

    def test_inverse(self):
        for i in range(5):
            arr = np.random.rand(20, 20)
            self.assertAlmostEqual(np.linalg.inv(arr).all(), Truss.inv(None, arr).all(), "Inverse function is incorrect")

    def test_ECM(self):
        js = JsonRead.readFile("../structure00.json")
        truss = Truss(js)
        ECM = truss.get_ECM()
        ans = np.array([[0, 1],[1, 3],[1, 2]], dtype=int)
        self.assertEqual(ECM.all(), ans.all(), "Inverse function is incorrect")




if __name__ == '__main__':
    unittest.main()