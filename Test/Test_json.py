import os, sys

parent = os.path.dirname(os.getcwd())
sys.path.append(parent)


import unittest
from JsonRead import readFile, writeFile

class Test_Truss(unittest.TestCase):

    def test_read(self):
        js = {
                "no_of_crosssection_types":2,
                "no_of_nodes":4,
                "no_of_elements": 3,
                "no_of_loads" : 1,
                "no_of_fixed_points" : 3,

                "nodes":[
                    {   "id":0,"x":1,"y":0,"z":0    },
                    {   "id":1,"x":3,"y":3,"z":0    },
                    {   "id":2,"x":5,"y":4,"z":0    },
                    {   "id":3,"x":5,"y":0,"z":0    }
                ],

                "element_type":[
                    {
                        "id":0,
                        "shape":"rectangle",
                        "youngs_mod":150,
                        "density":0,
                        "dimensions":
                            {"y":0.10,"z":0.20}
                    },
                    {
                        "id":1,
                        "shape":"circle",
                        "youngs_mod":150,
                        "density":0,
                        "dimensions":
                            {"radius":0.07}
                    }

                ],

                "elements": [
                    {
                        "id": 0,
                        "start_node_id":0,
                        "end_node_id":1,
                        "element_type": 0,
                        "local_x_dir":
                            {"x":2.0,"y":3.0,"z":1.0},
                        "local_y_dir":
                            {"x":0.0,"y":0.0,"z":-1.0},
                        "local_z_dir":
                            {"x":-3.0,"y":2.0,"z":0.0}
                    },
                    {
                        "id": 1,
                        "start_node_id": 1,
                        "end_node_id": 3,
                        "element_type": 0,
                        "local_x_dir":
                            {"x":2.0,"y":-3.0,"z":0.0},
                        "local_y_dir":
                            {"x":0.0,"y":0.0,"z":-1.0},
                        "local_z_dir":
                            {"x":3.0,"y":2.0,"z":0.0}

                    },
                    {
                        "id": 2,
                        "start_node_id": 1,
                        "end_node_id": 2,
                        "element_type": 1,
                        "local_x_dir":
                            {"x":2.0,"y":1.0,"z":0.0},
                        "local_y_dir":
                            {"x":0.0,"y":0.0,"z":1.0},
                        "local_z_dir":
                            {"x":-1.0,"y":2.0,"z":0.0}
                    }
                ],


                "loads": [
                    {
                        "id": 0,
                        "point_id":1,
                        "force":
                        {   "x":10, "y":0, "z":0},
                        "torque":
                        {   "x":0, "y":0, "z":0 }
                    }
                ],



                "fixed_points": [
                    {
                        "id" : 0,
                        "point_id":0,
                        "translation":
                        {  "x":True,"y":True,"z":True},
                        "rotation":
                        {  "x":True,"y":True,"z":False}
                    },
                    {
                        "id" : 1,
                        "point_id":2,
                        "translation":
                        {  "x":True,"y":False,"z":True},
                        "rotation":
                        {  "x":True,"y":True,"z":False}
                    },
                    {
                        "id" : 2,
                        "point_id":3,
                        "translation":
                        {  "x":True,"y":True,"z":True},
                        "rotation":
                        {  "x":True,"y":True,"z":True}
                    }



                ]
            }
        file = "Structures/structure00.json"
        self.assertDictEqual(readFile(file), js)

    def test_write(self):
        js = {
                "no_of_crosssection_types":2,
                "no_of_nodes":4,
                "no_of_elements": 3,
                "no_of_loads" : 1,
                "no_of_fixed_points" : 3,

                "nodes":[
                    {   "id":0,"x":1,"y":0,"z":0    },
                    {   "id":1,"x":3,"y":3,"z":0    },
                    {   "id":2,"x":5,"y":4,"z":0    },
                    {   "id":3,"x":5,"y":0,"z":0    }
                ],

                "element_type":[
                    {
                        "id":0,
                        "shape":"rectangle",
                        "youngs_mod":150,
                        "density":0,
                        "dimensions":
                            {"y":0.10,"z":0.20}
                    },
                    {
                        "id":1,
                        "shape":"circle",
                        "youngs_mod":150,
                        "density":0,
                        "dimensions":
                            {"radius":0.07}
                    }

                ],

                "elements": [
                    {
                        "id": 0,
                        "start_node_id":0,
                        "end_node_id":1,
                        "element_type": 0,
                        "local_x_dir":
                            {"x":2.0,"y":3.0,"z":1.0},
                        "local_y_dir":
                            {"x":0.0,"y":0.0,"z":-1.0},
                        "local_z_dir":
                            {"x":-3.0,"y":2.0,"z":0.0}
                    },
                    {
                        "id": 1,
                        "start_node_id": 1,
                        "end_node_id": 3,
                        "element_type": 0,
                        "local_x_dir":
                            {"x":2.0,"y":-3.0,"z":0.0},
                        "local_y_dir":
                            {"x":0.0,"y":0.0,"z":-1.0},
                        "local_z_dir":
                            {"x":3.0,"y":2.0,"z":0.0}

                    },
                    {
                        "id": 2,
                        "start_node_id": 1,
                        "end_node_id": 2,
                        "element_type": 1,
                        "local_x_dir":
                            {"x":2.0,"y":1.0,"z":0.0},
                        "local_y_dir":
                            {"x":0.0,"y":0.0,"z":1.0},
                        "local_z_dir":
                            {"x":-1.0,"y":2.0,"z":0.0}
                    }
                ],


                "loads": [
                    {
                        "id": 0,
                        "point_id":1,
                        "force":
                        {   "x":10, "y":0, "z":0},
                        "torque":
                        {   "x":0, "y":0, "z":0 }
                    }
                ],



                "fixed_points": [
                    {
                        "id" : 0,
                        "point_id":0,
                        "translation":
                        {  "x":True,"y":True,"z":True},
                        "rotation":
                        {  "x":True,"y":True,"z":False}
                    },
                    {
                        "id" : 1,
                        "point_id":2,
                        "translation":
                        {  "x":True,"y":False,"z":True},
                        "rotation":
                        {  "x":True,"y":True,"z":False}
                    },
                    {
                        "id" : 2,
                        "point_id":3,
                        "translation":
                        {  "x":True,"y":True,"z":True},
                        "rotation":
                        {  "x":True,"y":True,"z":True}
                    }



                ]
            }
        file = "Actual_output/test.json"
        writeFile(js, file)
        js_ = readFile(file)
        self.assertDictEqual(js_, js)

if __name__ == '__main__':
    unittest.main()