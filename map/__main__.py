import numpy as np


def load_grid(self, filename="filename"):
    grid_csv = np.loadtxt(filename + ".csv", delimiter=',')
    grid_list = np.array(grid_csv).tolist()
    return grid_list