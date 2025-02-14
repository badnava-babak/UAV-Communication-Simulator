import numpy as np
import os

import subprocess
from subprocess import Popen

base_path = '/home/b502b586/ardupilot-workspace/experiments'
os.chdir(base_path)

save_dir = '%s/saved_results' % base_path
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
save_enabled = True

# experiment_path = './exp-f:700-bw:6-video:1280p'

# if not os.path.exists(experiment_path):
#     os.makedirs(experiment_path)
# os.chdir(experiment_path)


import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

valid_frequencies = ["700", "1500", "2600"]
valid_bw = ["6", "15", "25", "50", "75", "100"]
valid_scenarios = ["UMa", "UMi", "RMa"]
valid_video_qualities = ["800p", "1280p", "1920p"]
valid_fr_algs = ["ns3::LteFrNoOpAlgorithm", "ns3::LteFrHardAlgorithm", "ns3::LteFrStrictAlgorithm",
                 "ns3::LteFrSoftAlgorithm", "ns3::LteFfrSoftAlgorithm", "ns3::LteFfrEnhancedAlgorithm"]

plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 20, })


def extract_video_throuput(video_0):
    rx_rows = np.where(video_0[:, 1] == 'rx')
    tx_rows = np.where(video_0[:, 1] == 'tx')

    rx_info = video_0[rx_rows][:, [0, 2]]
    tx_info = video_0[tx_rows][:, [0, 2]]

    tx_sum_rate = 8 * np.array([np.sum(tx_info[np.where(np.array(tx_info[:, 0], dtype=int) == i), 1]) for i in
                                range(int(np.max(tx_info[:, 0])))])

    if rx_info.shape[0] > 0:
        rx_sum_rate = 8 * np.array([np.sum(rx_info[np.where(np.array(rx_info[:, 0], dtype=int) == i), 1]) for i in
                                    range(int(np.max(rx_info[:, 0])))])
    else:
        rx_sum_rate = np.zeros_like(tx_sum_rate)

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
save_format = "png"

# Analyse effect of frequency
experiments_path = [
    # 'exp-f:700-bw:15-video:800p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:700-bw:15-video:1280p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:700-bw:15-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',

    # 'exp-f:700-bw:15-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:700-bw:50-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:700-bw:100-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    'exp-f:1500-bw:100-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1-useCA:false-nbCC:1-scenario:RMa-nbENB:1-run:0',
    'exp-f:1500-bw:100-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1-useCA:false-nbCC:1-scenario:RMa-nbENB:3-run:0',
    'exp-f:1500-bw:100-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1-useCA:false-nbCC:1-scenario:RMa-nbENB:5-run:0',

    # 'exp-f:700-bw:15-video:1280p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:1500-bw:15-video:1280p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:2600-bw:15-video:1280p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',

    # 'exp-f:700-bw:15-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:1500-bw:15-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:2600-bw:15-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',

    # 'exp-f:700-bw:50-video:1280p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:1500-bw:50-video:1280p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
    # 'exp-f:2600-bw:50-video:1280p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt',
]

mu = []
fig, ax = plt.subplots(figsize=(16, 9))

for i, path in enumerate(experiments_path):
    try:
        video_0 = pd.read_csv('./%s/VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()
    except:
        video_0 = pd.read_csv('./%s/uav-1-VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()

    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:path.find('-fr:')]
    fr_alg = path[path.find('-fr:') + 4:]
    nbENB = path[path.find('-nbENB:') + 7:path.find('-run')]

    rx_t, rx_sum_rate, tx_t, tx_sum_rate = extract_video_throuput(video_0)  # 6 mhz
    smoothed_rx_t, smoothed_rx_sum_rate = smooth(rx_sum_rate)

    # plt.scatter(smoothed_rx_t, smoothed_rx_sum_rate, label='Reception (f=%s, bw=%s, vq=%s)' % (freq, bw, video_quality))
    plt.scatter(smoothed_rx_t, smoothed_rx_sum_rate,
                label='$Avg. \, Reception \, Rate=%.2f Mb/s, \, STD=%.2f$ (Number of ENBs=%s)' % (
                    tx_sum_rate.mean(), tx_sum_rate.std(), nbENB))
    # mu.append('$Avg. Rate=%.2f Mb/s, \quad STD=%.2f$' % (rx_sum_rate.mean(), rx_sum_rate.std()))

# handles, labels = ax.get_legend_handles_labels()
# first_legend = ax.legend(handles, mu, loc='upper left')
# ax.add_artist(first_legend)

plt.legend()
plt.xlabel('Time (second)')
plt.ylabel('Throughput (Mb/s)')
if (save_enabled):
    plt.savefig('%s/Reception-Throughput-DiffFreq.%s' % (save_dir, save_format))
plt.show()
