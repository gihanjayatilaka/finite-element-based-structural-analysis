from Truss_class import *
from func import *
from JsonRead import *
import numpy as np

js = readFile('structure00.json')

truss = Truss(js)

out = truss.main_func()