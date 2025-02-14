import matplotlib.pyplot as plt

from data_utils import *
from plotting_utils import *

# plt.style.use('fivethirtyeight')
plt.style.use('Solarize_Light2')
# plt.rcParams.update({'font.size': 34, })
# plt.rcParams['axes.labelsize'] = 24
# plt.rcParams['axes.titlesize'] = 24

save_enabled = False
save_format = "png"

base_path = '/home/b502b586/ardupilot-workspace/experiments'
# base_path = '/home/b502b586/ardupilot-workspace/experiments/archive-complex-wildfire-track'
os.chdir(base_path)

path = '%s/exp-f:700-bw:15-video:800p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt' % base_path
# path = '%s/exp-f:700-bw:75-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt' % base_path
path = '/home/b502b586/ardupilot-workspace/ns3-mavsdk/build/src/ardupilot/examples/'

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
    bs_loc = np.array([bs_loc_each_second[i-1] for i in loc_time_index])


    diff2d = get_distanc(node_0_loc, bs_loc)
    # plt.figure(figsize=(16, 9))
    ax.scatter(node_0_t , diff2d)
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


n_row = 4
fig, axs = plt.subplots(n_row, 1, figsize=(19, n_row * 9))
############################# Plotting transmission rate ###############################
plot_transmission_rate(axs[0], path, 1, save_enabled, save_dir, save_format)
plot_transmission_rate(axs[1], path, 2, save_enabled, save_dir, save_format)

############################# Plotting Reception rate ###############################
plot_reception_rate(axs[2], path, 1, save_enabled, save_dir, save_format)
plot_reception_rate(axs[3], path, 2, save_enabled, save_dir, save_format)

# plt.savefig('%s/two-uavs.png' % (save_dir))
plt.show()
