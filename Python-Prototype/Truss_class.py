import numpy as np

class Truss:
    def __init__(self, js):
        n_n = js["no_of_nodes"]
        n_el = js["no_of_elements"]
        n_loads = js["no_of_loads"]
        n_cs = js["no_of_crosssection_types"]
        n_bc = js["no_of_fixed_points"]
        n_dim = 3                       # dimensions
        n_en = 2                        # number of elements per node
        n_dof = 6                       # number of dof per node

        self.n_n = n_n                  # number of nodes
        self.n_el = n_el                # number of elements
        self.n_en = n_en                # number of nodes in an element
        self.n_dof = n_dof              # number of dof per node
        self.coordinates = None
        self.ECM = None
        self.A = None
        self.L = None
        self.LCM = None
        self.F = None
        self.BC = None

        nodes = js["nodes"]
        element_type = js["element_type"]
        elements = js["elements"]
        loads = js["loads"]
        fixed_points = js["fixed_points"]


        if len(nodes) != self.n_n:
            raise ValueError('All Nodes not defined')
        else:
            nodes = sorted(nodes, key=lambda x: x["id"])
            if n_dim == 3:
                self.coordinates = [(nodes[i]["x"], nodes[i]["y"], nodes[i]["z"]) for i in range(n_n)]
            else:
                self.todo()

        if len(elements) != self.n_el:
            raise ValueError('All Elements not defined')
        else:
            self.get_ECM(elements)      # Populate ECM matrix

        if len(loads) != n_loads:
            raise ValueError('All Loads not defined')
        else:
            self.get_force_vect(loads)  # Populate Ext_force matrix

        if len(fixed_points) != n_bc:
            raise ValueError('Fixed points not defined')
        else:
            self.get_BC(fixed_points)   # Populate BC matrix (binary)

        if len(element_type) != n_cs:
            raise ValueError('All Element types not defined')
        else:
            area = {}
            youngs_mod = {}

            for el in element_type:
                id = el["id"]
                area[id] = self.get_area(el["shape"], el["dimensions"])
                youngs_mod[id] = el["youngs_mod"]

            self.todo()



    def get_ECM(self, elements = None):
        # Called by parent
        if elements is not None:
            elements = sorted(elements, key=lambda x: x["id"])
            self.ECM = np.array([[elements[i]["start_node_id"], elements[i]["end_node_id"]] for i in range(self.n_el)], dtype = int)
        else:
            return self.ECM

    def get_LCM(self):
        if self.LCM is None:
            dof_node = (np.arange(self.n_dof * self.n_n).reshape((self.n_n, self.n_dof)))

            LCM = dof_node[self.ECM, :]
            self.LCM = (LCM.reshape(self.n_el, self.n_en * self.n_dof)).T

        return self.LCM

    def get_force_vect(self, loads = None):
        # Called by parent
        if loads is not None:
            n_loads = len(loads)
            self.F = np.zeros((self.n_n, self.n_dof))
            if self.n_dof == 6:
                dirs = ["x", "y", "z"]
                ft = ["force", "torque"]
                for i in range(n_loads):
                    id = loads[i]["point_id"]
                    for j in range(2):
                        for k in range(3):
                            self.F[id][3*j+k] = loads[i][ft[j]][dirs[k]]
            else:
                raise ValueError("NOT YET COMPLETE")

        elif self.F is not None:
            return self.F.flatten()
        else:
            raise ValueError("Force vector not defined")

    def get_BC(self, fixed_points = None):
        # Called by parent
        if fixed_points is not None:
            n_bc = len(fixed_points)
            self.BC = np.ones((self.n_n, self.n_dof), dtype=int)
            if self.n_dof == 3:
                raise ValueError("NOT YET COMPLETE")
                pass
            elif self.n_dof == 6:
                dirs = ["x", "y", "z"]
                ft = ["translation", "rotation"]
                for i in range(n_bc):
                    id = fixed_points[i]["point_id"]
                    for j in range(2):
                        for k in range(3):
                            if fixed_points[i][ft[j]][dirs[k]]:
                                self.BC[id][3*j+k] = 0
        elif self.BC is not None:
            return self.BC.flatten()
        else:
            raise ValueError("Boundary condition not defined")

    def get_area(self, type, dim):
        if type == "rectangle":
            return dim["y"] * dim["z"]
        elif type == "circle":
            return np.pi*dim["radium"]**2
        else:
            self.todo()

    def todo(self):
        raise ValueError("NOT YET COMPLETE")

