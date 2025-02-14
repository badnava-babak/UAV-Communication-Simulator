import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 22, })


def extract_dl_info(rma2000):
    t = rma2000[:, 0]
    rsrp = 10 * np.log10(rma2000[:, 4])
    sinr = 10 * np.log10(rma2000[:, 5])
    return t, rsrp, sinr


def extract_ul_sinr(rma2000):
    t = rma2000[:, 0]
    sinr = 10 * np.log10(rma2000[:, 4])
    return t, sinr


dl_0 = pd.read_csv('./exp-1/DlRsrpSinrStats.txt', delimiter='	').to_numpy()
ul_0 = pd.read_csv('./exp-1/UlSinrStats.txt', delimiter='	').to_numpy()

dl_t, dl_rsrp, dl_sinr = extract_dl_info(dl_0)

ul_t, ul_sinr = extract_ul_sinr(ul_0)

########################### plot Down Link Stats ##############################
plt.figure(figsize=(16, 9))

plt.scatter(dl_t, dl_sinr, label='DL')
plt.scatter(ul_t, ul_sinr, label='UL')

plt.legend()
plt.xlabel('Time (second)')
plt.ylabel('SINR (db)')
plt.tight_layout()
plt.show()