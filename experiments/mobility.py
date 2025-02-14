import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 22, })

mob_0 = pd.read_csv('./exp-1/mobility-trace-example.mob', delimiter=',').to_numpy()


def extract_loc_data(mob_0):
    node_0_data = mob_0[np.argwhere(mob_0[:, 1] == 0)[:, 0]]
    node_0_loc = np.array([r.split(':') for r in node_0_data[:, 2]], dtype=float)
    node_0_t = node_0_data[:, 0]
    return node_0_t, node_0_loc


node_0_t, node_0_loc = extract_loc_data(mob_0)


def get_distanc(node_0_loc):
    diff = np.subtract(node_0_loc[1:], node_0_loc[0])
    diff2D = diff[:, :2] ** 2
    diff2D = np.sum(diff2D, axis=1)
    diff2D = np.sqrt(diff2D)
    return diff2D


diff2d = get_distanc(node_0_loc)

plt.scatter(node_0_loc[:, 1], node_0_loc[:, 2])
plt.show()
