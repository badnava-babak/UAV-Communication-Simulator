import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

import numpy as np
import os

import subprocess
from subprocess import Popen


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
experiments_path = ['exp-f:700-bw:6-video:800p',
                    'exp-f:700-bw:6-video:1280p',
                    'exp-f:1500-bw:15-video:800p',
                    'exp-f:2600-bw:50-video:800p',
                   ]
experiments_freq = ['700 MHz', '700 MHz', '1500 MHz', '2600 MHz']
experiments_bw = ['6 MHz', '6 MHz', '15 MHz', '50 MHz']
experiments_vq = ['880p', '1280p', '880p', '880p']


min_throughput = 1000
max_throughput = 0
for i, path in enumerate(experiments_path):
    video_0 = pd.read_csv('./%s/VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()
    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:]

    rx_t, rx_sum_rate, tx_t, tx_sum_rate = extract_video_throuput(video_0)  # 6 mhz
    min_throughput = min(rx_sum_rate.min(), min_throughput)
    max_throughput = max(rx_sum_rate.max(), max_throughput)


HIST_BINS = np.linspace(min_throughput, max_throughput, 100)
plt.figure(figsize=(16, 9))
for i, path in enumerate(experiments_path):
    video_0 = pd.read_csv('./%s/VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()

    rx_t, rx_sum_rate, tx_t, tx_sum_rate = extract_video_throuput(video_0)  # 6 mhz

    smoothed_rx_t, smoothed_rx_sum_rate = smooth(rx_sum_rate)

    plt.hist(rx_sum_rate, bins=HIST_BINS, range=(min_throughput, max_throughput), cumulative=True, density=True, histtype='step', linewidth=4,
             label='Reception (f=%s, bw=%s, vq=%s)' % (experiments_freq[i], experiments_bw[i], experiments_vq[i]))
    # plt.scatter(smoothed_tx_t, smoothed_tx_sum_rate, label='Transmission (f=%s, bw=%s)' % (experiments_freq[i], experiments_bw[i]))

plt.xlim(min_throughput, max_throughput)
plt.legend(loc='lower right')
plt.xlabel('Throughput (Mb/s)')
plt.ylabel('CDF')
plt.show()