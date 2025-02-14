import matplotlib.pyplot as plt
import numpy as np

from data_utils import *
from plotting_utils import *

# plt.style.use('fivethirtyeight')
plt.style.use('Solarize_Light2')
plt.rcParams.update({'font.size': 30, })
plt.rcParams['axes.labelsize'] = 24
plt.rcParams['axes.titlesize'] = 24

save_enabled = False
save_format = "png"

base_path = '/home/b502b586/ardupilot-workspace/experiments'
# base_path = '/home/b502b586/ardupilot-workspace/experiments/archive-complex-wildfire-track'
os.chdir(base_path)

path = '%s/exp-f:700-bw:15-video:800p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt' % base_path
path = '%s/exp-f:2600-bw:100-video:800p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1-useCA:false-nbCC:1' % base_path
# path = '%s/exp-f:700-bw:75-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt' % base_path
# path = '/home/b502b586/ardupilot-workspace/ns3-mavsdk/build/src/ardupilot/examples/'

save_dir = '%s/saved_results' % path
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


def plot_reception_rate(ax, path, uav_id, save_enabled, save_dir, save_format):
    mu = []
    # fig, ax = plt.subplots(figsize=(16, 9))
    video_0 = pd.read_csv('%s/uav-%s-VideoPacketTrace.txt' % (path, uav_id), delimiter='\t').to_numpy()
    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:path.find('-fr:')]
    fr_alg = path[path.find('-fr:') + 4:]
    rx_t, rx_sum_rate, tx_t, tx_sum_rate = extract_video_throuput(video_0)  # 6 mhz
    # smoothed_rx_t, smoothed_rx_sum_rate = smooth(rx_sum_rate)
    ax.scatter(rx_t, rx_sum_rate, label='Reception (f=%s, bw=%s, vq=%s)' % (freq, bw, video_quality))
    mu.append('$Avg. Rate=%.2f Mb/s, \quad STD=%.2f$' % (rx_sum_rate.mean(), rx_sum_rate.std()))
    handles, labels = ax.get_legend_handles_labels()
    first_legend = ax.legend(handles, mu, loc='upper left')
    ax.add_artist(first_legend)
    # ax.legend()
    # ax.set_xlabel('Time (second)')
    ax.set_ylabel('Rx Rate (Mb/s)')
    if (save_enabled):
        plt.savefig('%s/Reception-Throughput.%s' % (save_dir, save_format))
    # plt.show()


def plot_distance(ax, path, save_enabled, save_dir, save_format):
    mob_0 = pd.read_csv('%s/mobility-trace-example.mob' % path, delimiter=',').to_numpy()
    node_0_t, node_0_loc = extract_loc_data(mob_0)
    node_0_t /= 1000

    ul_0 = pd.read_csv('%s/UlSinrStats.txt' % path, delimiter='	').to_numpy()
    ul_0 = ul_0[np.where(ul_0[:, 2] == 1)]
    # cellid = ul_0[:, 1]
    # imsi = ul_0[:, 2]
    timesteps = np.array(ul_0[:, 0], dtype=int)
    cellid = np.array([np.max(ul_0[np.where(np.array(ul_0[:, 0], dtype=int) == i), 1]) for i in
                       timesteps])
    bs_loc_each_second = np.array([enb_info[cid - 1] for cid in cellid])
    loc_time_index = np.array(node_0_t, dtype=int)
    bs_loc = np.array([bs_loc_each_second[i - 1] for i in loc_time_index])

    diff2d = get_distanc(node_0_loc, bs_loc)
    # plt.figure(figsize=(16, 9))
    ax.scatter(node_0_t, diff2d)
    ax.set_xlabel('Time (second)')
    ax.set_ylabel('Distance (Km)')
    if (save_enabled):
        plt.savefig('%s/Distance.%s' % (save_dir, save_format))
    # plt.show()


def plot_transmission_rate(ax, path, uav_id, save_enabled, save_dir, save_format):
    mu = []
    # fig, ax = plt.subplots(figsize=(16, 9))
    video_0 = pd.read_csv('%s/uav-%s-VideoPacketTrace.txt' % (path, uav_id), delimiter='\t').to_numpy()
    video_quality = path[path.find('-video:') + 7:path.find('-fr:')]
    rx_t, rx_sum_rate, tx_t, tx_sum_rate = extract_video_throuput(video_0)  # 6 mhz
    # smoothed_tx_t, smoothed_tx_sum_rate = smooth(tx_sum_rate)

    ax.scatter(tx_t, tx_sum_rate, label='Transmission (vq=%s)' % (video_quality))
    mu.append('$Avg. Rate=%.2f Mb/s, \quad STD=%.2f$' % (tx_sum_rate.mean(), tx_sum_rate.std()))
    handles, labels = ax.get_legend_handles_labels()
    first_legend = ax.legend(handles, mu, loc='center')
    ax.add_artist(first_legend)
    # ax.legend(loc='upper left')
    # ax.set_xlabel('Time (second)')
    ax.set_ylabel('Tx Rate (Mb/s)')
    if (save_enabled):
        save_path = 'Transmission-Throughput-F:%s-BW:' % path[path.find('f:') + 2: path.find('-bw')]
        plt.savefig('%s/%s.%s' % (save_dir, save_path[:-1], save_format))
    # plt.show()


def extract_sumrate_stats(path, sim_time):
    nb_uavs = int(path[path.find('-nbUAVs:') + 8:path.find('-useCA')])
    stats = np.zeros((nb_uavs, 2, sim_time))
    for uav_id in range(1, nb_uavs + 1):
        video_0 = pd.read_csv('%s/uav-%s-VideoPacketTrace.txt' % (path, uav_id), delimiter='\t').to_numpy()
        rx_t, rx_sum_rate, tx_t, tx_sum_rate = extract_video_throuput(video_0)  # 6 mhz
        stats[uav_id - 1, 0, tx_t] = tx_sum_rate[tx_t]
        stats[uav_id - 1, 1, rx_t] = rx_sum_rate[rx_t]
    return np.mean(stats, axis=-1)


def plot_data(data_uma, data_umi, data_rma, title=''):
    w = 1
    x = np.arange(len(simulated_nb_users)) * 4 * w
    fig, axs = plt.subplots(1, 1, figsize=(19, 9))
    plt.title(title)
    # axs.plot(x, data_uma[:, 1], label='UMa')
    # axs.plot(x + w, data_umi[:, 1], label='UMi')
    # axs.plot(x + 2 * w, data_rma[:, 1], label='RMa')
    axs.bar(x - w, np.clip(data_uma[:, 1], 1.e-7, np.inf), label='UMa', width=w)
    axs.bar(x, np.clip(data_umi[:, 1], 1.e-7, np.inf), label='UMi', width=w)
    axs.bar(x + w, np.clip(data_rma[:, 1], 1.e-7, np.inf), label='RMa', width=w)
    axs.set_xticks(x)
    axs.set_xticklabels(simulated_nb_users)
    axs.set_xlabel('Number of UAVs')
    axs.set_ylabel('Throughput per UAV [Mbps]')
    axs.legend(prop={'size': 16})
    # plt.show()


def plot_data_per_distance(data_uma, data_umi, data_rma, title=''):
    w = 1
    x = np.arange(len(valid_distances)) * 4 * w
    fig, axs = plt.subplots(1, 1, figsize=(19, 9))
    plt.title(title)
    # axs.plot(x, data_uma[:, 1], label='UMa')
    # axs.plot(x + w, data_umi[:, 1], label='UMi')
    # axs.plot(x + 2 * w, data_rma[:, 1], label='RMa')
    axs.bar(x - w, np.clip(data_uma[:, 1], 1.e-7, np.inf), label='UMa', width=w)
    axs.bar(x, np.clip(data_umi[:, 1], 1.e-7, np.inf), label='UMi', width=w)
    axs.bar(x + w, np.clip(data_rma[:, 1], 1.e-7, np.inf), label='RMa', width=w)
    axs.set_xticks(x)
    axs.set_xticklabels(valid_distances)
    axs.set_xlabel('Distance from base station [m]')
    axs.set_ylabel('Throughput per UAV [Mbps]')
    axs.legend(prop={'size': 16})

    # plt.show()


working_dir = '/home/b502b586/ardupilot-workspace/experiments'

sim_time = 10
valid_frequencies = ["700", "1500", "2600"]
valid_bw = ["100"]
valid_scenarios = ["UMa", "UMi", "RMa"]
# valid_video_qualities = ["800p", "1280p", "1920p"]
valid_video_qualities = ["1920p"]
valid_fr_algs = ["ns3::LteFrNoOpAlgorithm", "ns3::LteFrHardAlgorithm", "ns3::LteFrStrictAlgorithm",
                 "ns3::LteFrSoftAlgorithm", "ns3::LteFfrSoftAlgorithm", "ns3::LteFfrEnhancedAlgorithm"]

simulated_nb_users = ['1', '3', '5', '10', '15']
# simulated_nb_users = ['5', '10', '15']
valid_distances = [100, 1000, 2000, 4000]

fr_alg = 'LteFfrSoftAlgorithm'
power_contorl = 't'
use_ca = 'false'
nb_componenet_carriers = '1'

stats = np.zeros((len(valid_frequencies),
                  len(valid_bw),
                  len(valid_scenarios),
                  len(valid_distances),
                  len(simulated_nb_users), 2)
                 )

for f, freq in enumerate(valid_frequencies):
    for b, bw in enumerate(valid_bw):
        for s, scenario in enumerate(valid_scenarios):
            for nb, nb_users in enumerate(simulated_nb_users):
                for d, distance in enumerate(valid_distances):
                    for video_quality in valid_video_qualities:
                        path_format = '%s/exp-f:%s-bw:%s-video:%s-fr:%s-pc:%s-sched:FdMt-nbUAVs:%s-useCA:%s-nbCC:%s-distance:%s-scenario:%s'
                        experiment_path = path_format % (working_dir, freq, bw, video_quality, fr_alg,
                                                         power_contorl, nb_users, use_ca, nb_componenet_carriers,
                                                         distance, scenario)
                        if os.path.exists(experiment_path):
                            print(experiment_path)
                            stats[f, b, s, d, nb, :] = np.mean(extract_sumrate_stats(experiment_path, sim_time),
                                                               axis=0)  # stats per user

print(stats)
# stats *= 2 ** 10

uma_stats = stats[:, :, 0, :, :, :]
umi_stats = stats[:, :, 1, :, :, :]
rma_stats = stats[:, :, 2, :, :, :]

freq_idx = 0

# stats for specific freq, bw, and distance of each scenario
data_uma_d0 = uma_stats[freq_idx, 0, 0]
data_umi_d0 = umi_stats[freq_idx, 0, 0]
data_rma_d0 = rma_stats[freq_idx, 0, 0]

data_uma_d1 = uma_stats[freq_idx, 0, 1]
data_umi_d1 = umi_stats[freq_idx, 0, 1]
data_rma_d1 = rma_stats[freq_idx, 0, 1]

data_uma_d2 = uma_stats[freq_idx, 0, 2]
data_umi_d2 = umi_stats[freq_idx, 0, 2]
data_rma_d2 = rma_stats[freq_idx, 0, 2]

data_uma_d3 = uma_stats[freq_idx, 0, 3]
data_umi_d3 = umi_stats[freq_idx, 0, 3]
data_rma_d3 = rma_stats[freq_idx, 0, 3]

# data_uma = data_uma_d0 + data_uma_d1 + data_uma_d2 + data_uma_d3
# data_umi = data_umi_d0 + data_umi_d1 + data_umi_d2 + data_umi_d3
# data_rma = data_rma_d0 + data_rma_d1 + data_rma_d2 + data_rma_d3
#
# data_uma = data_uma * 2 ** 10 / 4
# data_umi = data_umi * 2 ** 10 / 4
# data_rma = data_rma * 2 ** 10 / 4

# plot_data(data_uma_d0, data_umi_d0, data_rma_d0, 'Freq: %s MHz, BW: 20 MHz, Distance: 100 m' % valid_frequencies[freq_idx])
# plt.savefig('saturation-analysis-results/%sMHz-%sMHz-dis:%d.png' % (valid_frequencies[freq_idx], valid_bw[0], 100))
# plot_data(data_uma_d1, data_umi_d1, data_rma_d1, 'Freq: %s MHz, BW: 20 MHz, Distance: 1 Km'% valid_frequencies[freq_idx])
# plt.savefig('saturation-analysis-results/%sMHz-%sMHz-dis:%d.png' % (valid_frequencies[freq_idx], valid_bw[0], 1000))
# plot_data(data_uma_d2, data_umi_d2, data_rma_d2, 'Freq: %s MHz, BW: 20 MHz, Distance: 2 Km'% valid_frequencies[freq_idx])
# plt.savefig('saturation-analysis-results/%sMHz-%sMHz-dis:%d.png' % (valid_frequencies[freq_idx], valid_bw[0], 2000))
# plot_data(data_uma_d3, data_umi_d3, data_rma_d3, 'Freq: %s MHz, BW: 20 MHz, Distance: 4 Km'% valid_frequencies[freq_idx])
# plt.savefig('saturation-analysis-results/%sMHz-%sMHz-dis:%d.png' % (valid_frequencies[freq_idx], valid_bw[0], 4000))
#
# plt.show()

freq_idx = 0

data_uma_1u = uma_stats[freq_idx, 0, :, 0]
data_umi_1u = umi_stats[freq_idx, 0, :, 0]
data_rma_1u = rma_stats[freq_idx, 0, :, 0]

data_uma_3u = uma_stats[freq_idx, 0, :, 1]
data_umi_3u = umi_stats[freq_idx, 0, :, 1]
data_rma_3u = rma_stats[freq_idx, 0, :, 1]

data_uma_5u = uma_stats[freq_idx, 0, :, 2]
data_umi_5u = umi_stats[freq_idx, 0, :, 2]
data_rma_5u = rma_stats[freq_idx, 0, :, 2]

data_uma_10u = uma_stats[freq_idx, 0, :, 3]
data_umi_10u = umi_stats[freq_idx, 0, :, 3]
data_rma_10u = rma_stats[freq_idx, 0, :, 3]

data_uma_15u = uma_stats[freq_idx, 0, :, 4]
data_umi_15u = umi_stats[freq_idx, 0, :, 4]
data_rma_15u = rma_stats[freq_idx, 0, :, 4]

plot_data_per_distance(data_uma_1u, data_umi_1u, data_rma_1u,
                       'Freq: %s MHz, BW: 20 MHz, NB UAVs: 1' % valid_frequencies[freq_idx])
plt.savefig('saturation-analysis-results/%sMHz-%sMHz-%d_UAVs.png' % (valid_frequencies[freq_idx], valid_bw[0], 1))
plot_data_per_distance(data_uma_3u, data_umi_3u, data_rma_3u,
                       'Freq: %s MHz, BW: 20 MHz, NB UAVs: 3' % valid_frequencies[freq_idx])
plt.savefig('saturation-analysis-results/%sMHz-%sMHz-%d_UAVs.png' % (valid_frequencies[freq_idx], valid_bw[0], 3))
plot_data_per_distance(data_uma_5u, data_umi_5u, data_rma_5u,
                       'Freq: %s MHz, BW: 20 MHz, NB UAVs: 5' % valid_frequencies[freq_idx])
plt.savefig('saturation-analysis-results/%sMHz-%sMHz-%d_UAVs.png' % (valid_frequencies[freq_idx], valid_bw[0], 5))
plot_data_per_distance(data_uma_10u, data_umi_10u, data_rma_10u,
                       'Freq: %s MHz, BW: 20 MHz, NB UAVs: 10' % valid_frequencies[freq_idx])
plt.savefig('saturation-analysis-results/%sMHz-%sMHz-%d_UAVs.png' % (valid_frequencies[freq_idx], valid_bw[0], 10))
plot_data_per_distance(data_uma_15u, data_umi_15u, data_rma_15u,
                       'Freq: %s MHz, BW: 20 MHz, NB UAVs: 15' % valid_frequencies[freq_idx])
plt.savefig('saturation-analysis-results/%sMHz-%sMHz-%d_UAVs.png' % (valid_frequencies[freq_idx], valid_bw[0], 15))

plt.show()
