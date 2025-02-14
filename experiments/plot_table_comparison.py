import numpy as np
import os

import subprocess
from subprocess import Popen

import matplotlib.pyplot as plt

from data_utils import *
from plotting_utils import *

# plt.style.use('fivethirtyeight')
plt.style.use('Solarize_Light2')
plt.rcParams.update({'font.size': 34, })
plt.rcParams['axes.labelsize'] = 24
plt.rcParams['axes.titlesize'] = 24

save_enabled = False
save_format = "png"

executable_path = "/home/b502b586/ardupilot-workspace/ns3-mavsdk/build/src/ardupilot/examples/"

working_dir = '/home/b502b586/ardupilot-workspace/experiments/archive-complex-wildfire-track'
working_dir = '/home/b502b586/ardupilot-workspace/experiments'
os.chdir(working_dir)

sim_time = 300
valid_frequencies = ["700", "1500", "2600"]
# valid_frequencies = ["700", "1500"]
# valid_bw = ["6", "15", "25", "50", "75", "100"]
valid_bw = ["15", "50", "100"]
# valid_bw = ["100"]
valid_scenarios = ["UMa", "UMi", "RMa"]
valid_video_qualities = ["800p", "1280p", "1920p"]
valid_fr_algs = ["ns3::LteFrNoOpAlgorithm", "ns3::LteFrHardAlgorithm", "ns3::LteFrStrictAlgorithm",
                 "ns3::LteFrSoftAlgorithm", "ns3::LteFfrSoftAlgorithm", "ns3::LteFfrEnhancedAlgorithm"]

fr_alg = valid_fr_algs[4]
power_contorl = 'true'

# Analyse effect of frequency and proportional bandwidth
avg_rx_rate_results = -1 * np.ones((3, 3, 3))  # F, BW, VQ, FR
avg_tx_rate_results = -1 * np.ones((3, 3, 3))  # F, BW, VQ, FR
std_rx_rate_results = -1 * np.ones((3, 3, 3))  # F, BW, VQ, FR

for freq in valid_frequencies:
    for bw in valid_bw:
        for video_quality in valid_video_qualities:
            print('###########################')
            os.chdir(working_dir)

            path = '%s/exp-f:%s-bw:%s-video:%s-fr:%s-pc:%s-sched:FdMt' % (
                working_dir, freq, bw, video_quality, fr_alg[5:], power_contorl[0])
            save_path = 'Reception-Throughput-CDF-DiffFreq-VQ:%s-ProportionalBW:' % path[path.find('-video:') + 7:]
            try:
                video_0 = pd.read_csv('%s/VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()
            except:
                video_0 = pd.read_csv('%s/uav-1-VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()

            freq = path[path.find('f:') + 2: path.find('-bw')]
            bw = path[path.find('-bw:') + 4:path.find('-video')]
            video_quality = path[path.find('-video:') + 7:path.find('-fr:')]
            # fr_alg = path[path.find('-fr:') + 4:path.find('-pc:')]

            freq_idx = np.argwhere(np.array(valid_frequencies) == freq)[0]
            bw_idx = np.argwhere(np.array(valid_bw) == bw)[0]
            video_quality_idx = np.argwhere(np.array(valid_video_qualities) == video_quality)[0]
            # fr_alg_idx = np.argwhere(np.array(valid_fr_algs) == 'ns3::' + fr_alg)[0]

            rx_t, rx_sum_rate, tx_t, tx_sum_rate = extract_video_throuput(video_0)  # 6 mhz
            avg_rx_rate_results[freq_idx, bw_idx, video_quality_idx] = rx_sum_rate.sum() / 300
            avg_tx_rate_results[freq_idx, bw_idx, video_quality_idx] = tx_sum_rate.sum() / 300
            std_rx_rate_results[freq_idx, bw_idx, video_quality_idx] = rx_sum_rate.std()

            # mu.append('$Avg. Rate=%.2f Mb/s, \quad STD=%.2f$' % (rx_sum_rate.mean(), rx_sum_rate.std()))


def print_f_bw_comparison(data):
    print("{:<4}: # ".format('f\\bw'), end='')
    # print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(*valid_bw))
    print("{:<8} {:<8} {:<8}".format(*valid_bw))
    print("#" * 56)
    avg_rx_rate_results = np.round(data, 4)
    avg_rx_rate_results[data == -1] = 0
    for f_i, f in enumerate(valid_frequencies):
        print("{:<4}: # ".format(f), end='')
        print("{:<8} {:<8} {:<8}".format(*np.round(data[f_i], decimals=4)))


# print('Avg. reception rate of VQ:800p and no Freq. reuse:')
# print_f_bw_comparison(avg_rx_rate_results[:, :, 0])
# print('\n\n')
#
# print('Avg. reception rate of VQ:1280p and no Freq. reuse:')
# print_f_bw_comparison(avg_rx_rate_results[:, :, 1])
# print('\n\n')
#
# print('Avg. reception rate of VQ:1920p and no Freq. reuse:')
# print_f_bw_comparison(avg_rx_rate_results[:, :, 2])
# print('\n\n')

# print('Avg. transmission rate of VQ:800p and LteFfrSoftAlgorithm:')
# print_f_bw_comparison(avg_tx_rate_results[:, :, 0])
# print('\n\n')
#
# print('Avg. transmission rate of VQ:1280p and LteFfrSoftAlgorithm:')
# print_f_bw_comparison(avg_tx_rate_results[:, :, 1])
# print('\n\n')
#
# print('Avg. transmission rate of VQ:1920p and LteFfrSoftAlgorithm:')
# print_f_bw_comparison(avg_tx_rate_results[:, :, 2])
# print('\n\n')



print('Avg. reception rate of VQ:800p and LteFfrSoftAlgorithm:')
print_f_bw_comparison(avg_rx_rate_results[:, :, 0])
print('\n\n')

print('Avg. reception rate of VQ:1280p and LteFfrSoftAlgorithm:')
print_f_bw_comparison(avg_rx_rate_results[:, :, 1])
print('\n\n')

print('Avg. reception rate of VQ:1920p and LteFfrSoftAlgorithm:')
print_f_bw_comparison(avg_rx_rate_results[:, :, 2])
print('\n\n')



