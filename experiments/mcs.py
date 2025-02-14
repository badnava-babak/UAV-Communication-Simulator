import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

import numpy as np
import os

import subprocess
from subprocess import Popen
import matplotlib.patches as mpatches

base_path = '/home/b502b586/ardupilot-workspace/experiments'
os.chdir(base_path)

experiment_path = './exp-f:700-bw:6-video:1280p'

if not os.path.exists(experiment_path):
    os.makedirs(experiment_path)
os.chdir(experiment_path)

plt.rcParams.update({'font.size': 22, })


def extract_video_throuput(video_0):
    rx_rows = np.where(video_0[:, 1] == 'rx')
    tx_rows = np.where(video_0[:, 1] == 'tx')

    rx_info = video_0[rx_rows][:, [0, 2]]
    tx_info = video_0[tx_rows][:, [0, 2]]

    rx_sum_rate = 8 * np.array([np.sum(rx_info[np.where(np.array(rx_info[:, 0], dtype=int) == i), 1]) for i in
                                range(int(np.max(rx_info[:, 0])))])
    tx_sum_rate = 8 * np.array([np.sum(tx_info[np.where(np.array(tx_info[:, 0], dtype=int) == i), 1]) for i in
                                range(int(np.max(tx_info[:, 0])))])

    return np.arange(rx_sum_rate.shape[0]), rx_sum_rate / (2 ** 20), np.arange(tx_sum_rate.shape[0]), tx_sum_rate / (
                2 ** 20)


def smooth(rx_sum_rate):
    window_size = 15

    rx_data = pd.Series(rx_sum_rate)
    windows = rx_data.rolling(window_size)
    rx_sum_rate = windows.mean()

    return np.arange(rx_sum_rate.shape[0]), rx_sum_rate



############### Comparing Different Experiments with eachothers ##################
os.chdir(base_path)
# Analyse effect of bandwidth while the frequency is fixed
# Analyse effect of bandwidth while the frequency is fixed
experiments_path = [
    # 'exp-f:700-bw:6-video:800p',
    # 'exp-f:700-bw:6-video:1280p',

    # 'exp-f:700-bw:6-video:1920p',
    # 'exp-f:700-bw:15-video:1920p',
    # 'exp-f:700-bw:25-video:1920p',

    # 'exp-f:1500-bw:15-video:800p',
    # 'exp-f:1500-bw:15-video:1280p',

    # 'exp-f:1500-bw:15-video:1920p',
    # 'exp-f:1500-bw:25-video:1920p',
    # 'exp-f:1500-bw:50-video:1920p',

    # 'exp-f:2600-bw:50-video:800p',
    # 'exp-f:2600-bw:50-video:1280p',

    'exp-f:2600-bw:25-video:1920p',
    'exp-f:2600-bw:50-video:1920p',
    # 'exp-f:2600-bw:75-video:1920p',
]

save_path = 'Reception-Throughput-DiffBW-F:%s-VQ:%s' % (
experiments_path[0][experiments_path[0].find('f:') + 2: experiments_path[0].find('-bw')],
experiments_path[0][experiments_path[0].find('-video:') + 7:])

print(save_path)


# HIST_BINS = np.linspace(min_throughput, max_throughput, 100)
# plt.figure(figsize=(16, 9))
fig, ax = plt.subplots(figsize=(16, 9))
for i, path in enumerate(experiments_path):
    video_0 = pd.read_csv('./%s/UlTxPhyStats.txt' % path, delimiter='\t').to_numpy()

    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:]

    mcs = video_0[:, 5]
    t = video_0[:, 0] / 1000

    ax.scatter(t, mcs, label='MCS (f=%s, bw=%s, vq=%s)' % (freq, bw, video_quality))



# plt.xlim(min_throughput, max_throughput)
ax.legend(loc='lower right')
plt.xlabel('Throughput (Mb/s)')
plt.ylabel('CDF')

print(save_path[:])

# if (save_enabled):
#     plt.savefig('%s/%s.%s' % (save_dir, save_path[:], save_format))

plt.show()