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
        n_dof = n_dim*n_en              # number of dof per node

        self.n_n = n_n                  # number of nodes
        self.n_el = n_el                # number of elements
        self.n_en = n_en                # number of nodes in an element
        self.n_dof = n_dof              # number of dof per node

        self.coordinates = None
        self.ECM = None
        self.A = None
        self.Y = None
        self.L = None
        self.LCM = None
        self.F = None
        self.BC = None
        self.angle = None

        nodes = js["nodes"]
        element_type = js["element_type"]
        elements = js["elements"]
        loads = js["loads"]
        fixed_points = js["fixed_points"]


        if len(nodes) != self.n_n:
            raise ValueError('All Nodes not defined')
        else:
            nodes = sorted(nodes, key=lambda x: x["id"])
            try:
                self.coordinates = np.array([(nodes[i]["x"], nodes[i]["y"], nodes[i]["z"]) for i in range(n_n)], dtype=int)
            except:
                self.todo("Dimension not 3D")

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
            self.get_AY(elements, element_type)


        # Calculate length
        self.get_L()

        # Calculate angle matrix
        self.get_angle()




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
            return np.pi*dim["radius"]**2
        else:
            self.todo()

    def get_angle(self):
        # Called by parent
        if self.angle is None:
            cord = self.ECM[self.coordinates]
            print(cord)
            self.todo()
        return self.angle

    def get_AY(self, elements =  None, element_type = None):
        # Called by parent
        if self.A is None or self.Y is  None:
            if elements is None or element_type is None:
                raise ValueError("A and Y not defined")

            area = {}
            youngs_mod = {}

            for el in element_type:
                id = el["id"]
                youngs_mod[id] = el["youngs_mod"]
                # Get area
                try:
                    area[id] = self.get_area(el["shape"], el["dimensions"])
                except:
                    try:
                        area[id] = el["area"]
                    except:
                        self.todo("Dimension not defined")


            elements = sorted(elements, key=lambda x: x["id"])
            type = [el["element_type"] for el in elements]

            self.A = np.array([area[t] for t in type])
            self.Y = np.array([youngs_mod[t] for t in type])

        else:
            return self.A,self.Y

    def get_L(self):
        if self.L is None:
            if self.ECM is None or self.coordinates is None:
                self.todo("Length parameters not defined")
            print(self.ECM)
            print(self.coordinates)
            L = self.coordinates[self.ECM]
            self.L = np.sqrt(np.sum(np.square(L[:, 0, :] - L [:, 1, :]), axis=1))
        else:
            return self.L




    def get_k_local(self):

        # c = np.cos(self.ang)
        # s = np.sin(self.ang)
        #
        # cc = c * c
        # ss = s * s
        # cs = s * c
        #
        # arr = np.array([[cc, cs, -cc, -cs],
        #                 [cs, ss, -cs, -ss],
        #                 [-cc, -cs, cc, cs],
        #                 [-cs, -ss, cs, ss]])

        return arr

    def get_k_global(self):
        k = self.get_k_local()
        const = self.A * self.E / self.L
        return const * k

    def get_K(self, k_local):
        t_dof = self.n_n * self.n_dof
        el_dof = self.n_en * self.n_dof

        K = np.zeros((t_dof, t_dof))

        for i in range(self.n_el):
            ind = np.repeat(self.LCM[:, i], el_dof).reshape(el_dof, el_dof)
            # print(k_local[:, :, i], ind)
            K[ind, ind.T] += k_local[:, :, i]

        return K

    def apply_BC(self, K):
        t_dof = self.n_n * self.n_dof

        z = np.zeros(t_dof, dtype=int)

        K[self.BC] = z
        K[self.BC, self.BC] = 1

        return K


    ''' Modify only this function to optimize inverse'''
    def inv(self, K):
        return np.linalg.inv(K)





    def main_func(self):

        k_local = self.get_k_global()

        K = self.get_K(k_local)
        Kf = K.copy()

        F = self.get_force_vect()

        K_inv = self.inv(K)

        d = np.dot(K_inv, F)
        # print('d', d)

        fr = np.dot(Kf, d)
        # print('fr', fr)

        self.todo()

        return fr




    def todo(self,td = "NOT YET COMPLETE"):
        raise ValueError("TO DO : " + td)

