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


def extract_sumrate_stats(path):
    nb_uavs = int(path[path.find('-nbUAVs:') + 8:path.find('-useCA')])
    stats = np.zeros((nb_uavs, 2, 301))
    for uav_id in range(1, nb_uavs + 1):
        video_0 = pd.read_csv('%s/uav-%s-VideoPacketTrace.txt' % (path, uav_id), delimiter='\t').to_numpy()
        rx_t, rx_sum_rate, tx_t, tx_sum_rate = extract_video_throuput(video_0)  # 6 mhz
        stats[uav_id - 1, 0, tx_t] = tx_sum_rate[tx_t]
        stats[uav_id - 1, 1, rx_t] = rx_sum_rate[rx_t]
    return np.sum(stats, axis=0)


video_quality = '800p'

all_path_2600_bw_100 = [
    '%s/exp-f:2600-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1-useCA:false-nbCC:1' % (base_path, video_quality),
    '%s/exp-f:2600-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:3-useCA:false-nbCC:1' % (base_path, video_quality),
    '%s/exp-f:2600-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:5-useCA:false-nbCC:1' % (base_path, video_quality),
    '%s/exp-f:2600-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:10-useCA:false-nbCC:1' % (base_path, video_quality),
    '%s/exp-f:2600-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:15-useCA:false-nbCC:1' % (base_path, video_quality)]

all_path_2600_bw_15 = [
    '%s/exp-f:2600-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1' % (base_path, video_quality),
    '%s/exp-f:2600-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:3' % (base_path, video_quality),
    '%s/exp-f:2600-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:5' % (base_path, video_quality),
    '%s/exp-f:2600-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:10' % (base_path, video_quality),
    '%s/exp-f:2600-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:15' % (base_path, video_quality)]

all_path_700 = [
    '%s/exp-f:700-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1' % (base_path, video_quality),
    '%s/exp-f:700-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:3' % (base_path, video_quality),
    '%s/exp-f:700-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:5' % (base_path, video_quality),
    '%s/exp-f:700-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:10' % (base_path, video_quality),
    '%s/exp-f:700-bw:100-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:15' % (base_path, video_quality)]

all_path_700_bw_20 = [
    '%s/exp-f:700-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1' % (base_path, video_quality),
    '%s/exp-f:700-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1' % (base_path, video_quality),
    '%s/exp-f:700-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1' % (base_path, video_quality),
    '%s/exp-f:700-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1' % (base_path, video_quality),
    '%s/exp-f:700-bw:15-video:%s-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt-nbUAVs:1' % (base_path, video_quality)]

# for path in all_path:
#     n_row = 2
#     sum_rate = extract_sumrate_stats(path)
#
#     fig, axs = plt.subplots(n_row, 1, figsize=(19, n_row * 9))
#     axs[0].scatter(np.arange(sum_rate.shape[1]), sum_rate[0, :],
#                    label='Transmission (%.3f Mbps)' % np.mean(sum_rate[0, :]))
#     axs[1].scatter(np.arange(sum_rate.shape[1]), sum_rate[1, :],
#                    label='Reception (%.3f Mbps)' % np.mean(sum_rate[1, :]))
#
#     axs[0].legend()
#     axs[1].legend()
# plt.savefig('%s/two-uavs.png' % (save_dir))

if True:
    stats_2600_bw_100 = np.zeros((len(all_path_2600_bw_100), 3))
    for i, path in enumerate(all_path_2600_bw_100):
        n_row = 2
        sum_rate = extract_sumrate_stats(path)
        nb_uavs = int(path[path.find('-nbUAVs:') + 8:path.find('-useCA:')])

        transmission = np.mean(sum_rate[0, :]) / nb_uavs  # Mbp/s/nbUsers
        reception = np.mean(sum_rate[1, :]) / nb_uavs  # Mbp/s/nbUsers
        stats_2600_bw_100[i, 0] = nb_uavs
        stats_2600_bw_100[i, 1] = transmission
        stats_2600_bw_100[i, 2] = reception

    stats_2600_bw_15 = np.zeros((len(all_path_2600_bw_15), 3))
    for i, path in enumerate(all_path_2600_bw_15):
        n_row = 2
        sum_rate = extract_sumrate_stats(path)
        nb_uavs = int(path[path.find('-nbUAVs:') + 8:])

        transmission = np.mean(sum_rate[0, :]) / nb_uavs  # Mbp/s/nbUsers
        reception = np.mean(sum_rate[1, :]) / nb_uavs  # Mbp/s/nbUsers
        stats_2600_bw_15[i, 0] = nb_uavs
        stats_2600_bw_15[i, 1] = transmission
        stats_2600_bw_15[i, 2] = reception

    stats_700_bw_100 = np.zeros((len(all_path_700), 3))
    for i, path in enumerate(all_path_700):
        n_row = 2
        sum_rate = extract_sumrate_stats(path)
        nb_uavs = int(path[path.find('-nbUAVs:') + 8:])

        transmission = np.mean(sum_rate[0, :]) / nb_uavs  # Mbp/s/nbUsers
        reception = np.mean(sum_rate[1, :]) / nb_uavs  # Mbp/s/nbUsers
        stats_700_bw_100[i, 0] = nb_uavs
        stats_700_bw_100[i, 1] = transmission
        stats_700_bw_100[i, 2] = reception

    stats_700_bw_15 = np.zeros((len(all_path_700_bw_20), 3))
    for i, path in enumerate(all_path_700_bw_20):
        n_row = 2
        sum_rate = extract_sumrate_stats(path)
        nb_uavs = int(path[path.find('-nbUAVs:') + 8:])

        transmission = np.mean(sum_rate[0, :]) / nb_uavs  # Mbp/s/nbUsers
        reception = np.mean(sum_rate[1, :]) / nb_uavs  # Mbp/s/nbUsers
        stats_700_bw_15[i, 0] = nb_uavs
        stats_700_bw_15[i, 1] = transmission
        stats_700_bw_15[i, 2] = reception

    np.save('stats_700_bw_15', stats_700_bw_15)
    np.save('stats_700_bw_100', stats_700_bw_100)
    np.save('stats_2600_bw_15', stats_2600_bw_15)
    np.save('stats_2600_bw_100', stats_2600_bw_100)
else:
    stats_700_bw_15 = np.load('stats_700_bw_15.npy')
    stats_700_bw_100 = np.load('stats_700_bw_100.npy')
    stats_2600_bw_15 = np.load('stats_2600_bw_15.npy')
    stats_2600_bw_100 = np.load('stats_2600_bw_100.npy')

w = 1

x = np.arange(stats_700_bw_15[:, 0].shape[0]) * 7

fig, axs = plt.subplots(1, 1, figsize=(19, 9))
# axs.plot(stats_2600[:, 0], stats_2600[:, 1], label='Transmission (2600 MHz)')
# axs.plot(stats_2600[:, 0], stats_2600[:, 2], label='Reception (2600 MHz)')

# axs.plot(stats_700[:, 0], stats_700[:, 1], label='Transmission (700 MHz)')
axs.bar(x + w - w / 4, np.clip(stats_700_bw_15[:, 2], 0.05, np.inf), label='700 MHz, BW: 3 MHz', width=w, hatch='',
        color='deepskyblue')
axs.bar(x + 2 * w - w / 4, np.clip(stats_700_bw_100[:, 2], 0.05, np.inf), label='700 MHz, BW: 20 MHz', width=w,
        hatch='', color='steelblue')

axs.bar(x - 2 * w + w / 4, np.clip(stats_2600_bw_15[:, 2], 0.05, np.inf), label='2600 MHz, BW: 3 MHz', width=w,
        hatch='', color='salmon')
axs.bar(x - w + w / 4, np.clip(stats_2600_bw_100[:, 2], 0.05, np.inf), label='2600 MHz, BW: 20 MHz', width=w, hatch='',
        color='darkred')

axs.set_xticks(x)
axs.set_xticklabels(['1', '3', '5', '10', '15'])

axs.set_xlabel('Number of Users')
axs.set_ylabel('Throughput [Mbps per number of users]')
axs.legend(prop={'size': 16})
plt.show()
