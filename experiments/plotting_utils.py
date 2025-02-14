import matplotlib.pyplot as plt

from data_utils import *


def plot_transmission_rate(ax, path, save_enabled, save_dir, save_format):
    mu = []
    # fig, ax = plt.subplots(figsize=(16, 9))
    try:
        video_0 = pd.read_csv('%s/VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()
    except:
        video_0 = pd.read_csv('%s/uav-1-VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()
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


def plot_reception_rate(ax, path, save_enabled, save_dir, save_format):
    mu = []
    # fig, ax = plt.subplots(figsize=(16, 9))
    try:
        video_0 = pd.read_csv('%s/VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()
    except:
        video_0 = pd.read_csv('%s/uav-1-VideoPacketTrace.txt' % path, delimiter='\t').to_numpy()
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


def plot_dl_rsrp(ax, path, save_enabled, save_dir, save_format):
    # plt.figure(figsize=(16, 9))
    dl_0 = pd.read_csv('%s/DlRsrpSinrStats.txt' % path, delimiter='	').to_numpy()
    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:]
    dl_t, dl_rsrp, dl_sinr = extract_dl_info(dl_0)
    ax.scatter(dl_t, dl_rsrp, label='DL (f=%s, bw=%s, vq=%s)' % (freq, bw, video_quality))
    # ax.legend()
    # ax.set_xlabel('Time (second)')
    ax.set_ylabel('DL RSRP (db)')
    # plt.tight_layout()
    if (save_enabled):
        plt.savefig('%s/DL-RSRP.%s' % (save_dir, save_format))
    # plt.show()


def plot_dl_sinr(ax, path, save_enabled, save_dir, save_format):
    # plt.figure(figsize=(16, 9))
    dl_0 = pd.read_csv('%s/DlRsrpSinrStats.txt' % path, delimiter='	').to_numpy()
    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:]
    dl_t, dl_rsrp, dl_sinr = extract_dl_info(dl_0)
    ax.scatter(dl_t, dl_sinr, label='DL (f=%s, bw=%s, vq=%s)' % (freq, bw, video_quality))
    # ax.legend()
    # ax.set_xlabel('Time (second)')
    ax.set_ylabel('DL SINR (db)')
    # ax.tight_layout()
    if (save_enabled):
        plt.savefig('%s/DL-SINR.%s' % (save_dir, save_format))
    # plt.show()


def plot_ul_sinr(ax, path, save_enabled, save_dir, save_format):
    # plt.figure(figsize=(16, 9))
    ul_0 = pd.read_csv('%s/UlSinrStats.txt' % path, delimiter='	').to_numpy()
    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:]
    ul_t, ul_sinr = extract_ul_sinr(ul_0)
    ax.scatter(ul_t, ul_sinr, label='UL (f=%s, bw=%s, vq=%s)' % (freq, bw, video_quality))
    # ax.legend()
    # ax.set_xlabel('Time (second)')
    ax.set_ylabel('UL SINR (db)')
    # ax.tight_layout()
    if (save_enabled):
        plt.savefig('%s/UL-SINR.%s' % (save_dir, save_format))
    # plt.show()


def plot_ul_tx_mcs(ax, path, save_enabled, save_dir, save_format):
    # fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_title('UL TX MCS')
    video_0 = pd.read_csv('%s/UlTxPhyStats.txt' % path, delimiter='\t').to_numpy()
    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:]
    mcs = video_0[:, 5]
    t = video_0[:, 0] / 1000
    ax.scatter(t, mcs, label='MCS (f=%s, bw=%s, vq=%s)' % (freq, bw, video_quality))
    # ax.legend(loc='lower right')
    # ax.set_xlabel('Time (s)')
    ax.set_ylabel('UL TX MCS')
    ax.set_ylim(0, 28)
    if (save_enabled):
        plt.savefig('%s/UL-Tx-MCS.%s' % (save_dir, save_format))
    # plt.show()


def plot_ul_rx_mcs(ax, path, save_enabled, save_dir, save_format):
    # fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_title('UL RX MCS')
    video_0 = pd.read_csv('%s/UlRxPhyStats.txt' % path, delimiter='\t').to_numpy()
    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:]
    mcs = video_0[:, 5]
    t = video_0[:, 0] / 1000
    ax.scatter(t, mcs, label='MCS (f=%s, bw=%s, vq=%s)' % (freq, bw, video_quality))
    # ax.legend(loc='lower right')
    # ax.set_xlabel('Time (s)')
    ax.set_ylabel('UL RX MCS')
    ax.set_ylim(0, 28)
    if (save_enabled):
        plt.savefig('%s/UL-Rx-MCS.%s' % (save_dir, save_format))
    # plt.show()


def plot_ul_mac_stats(ax, path, save_enabled, save_dir, save_format):
    # fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_title('UL MAC MCS')
    video_0 = pd.read_csv('%s/UlMacStats.txt' % path, delimiter='\t').to_numpy()
    video_0 = video_0[np.argwhere(video_0[:, 2] == 1)[:, 0]]
    freq = path[path.find('f:') + 2: path.find('-bw')]
    bw = path[path.find('-bw:') + 4:path.find('-video')]
    video_quality = path[path.find('-video:') + 7:]
    mcs = video_0[:, 6]
    t = video_0[:, 0]
    ax.scatter(t, mcs, label='MCS (f=%s, bw=%s, vq=%s)' % (freq, bw, video_quality))
    # ax.legend(loc='lower right')
    # ax.set_xlabel('Time (s)')
    ax.set_ylabel('UL MAC MCS')
    plt.ylim(0, 28)
    if (save_enabled):
        plt.savefig('%s/UL-MAC-MCS.%s' % (save_dir, save_format))
    # plt.show()


def plot_trajectory(ax, path, save_enabled, save_dir, save_format):
    mob_0 = pd.read_csv('%s/mobility-trace-example.mob' % path, delimiter=',').to_numpy()
    node_0_t, node_0_loc = extract_loc_data(mob_0)
    # plt.figure(figsize=(16, 9))
    ax.scatter(node_0_loc[:, 0], node_0_loc[:, 1])
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    if (save_enabled):
        plt.savefig('%s/Trajectory.%s' % (save_dir, save_format))
    # plt.show()


enb_info = {
    0: (34.5264173, -119.9760841),
    1: (34.4648433, -120.0679317),
    2: (34.6102712, -120.0808299),
    3: (34.5954165, -120.137612),
    4: (34.6084597, -120.1926335),
    5: (34.5736732, -120.1935138),
    6: (34.50986, -120.2260865),
    7: (34.482652, -120.2304882)
}


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


def plot_pucch_power(ax, path, save_enabled, save_dir, save_format):
    mob_0 = pd.read_csv('%s/uav-1-pucchTxPower-info.txt' % path, delimiter='\t').to_numpy()
    # plt.figure(figsize=(16, 9))
    ax.scatter(mob_0[:, 0], mob_0[:, 3])
    # ax.set_xlabel('Time (second)')
    ax.set_ylabel('PUCCH TX Power')
    if (save_enabled):
        plt.savefig('%s/pucchTxPower.%s' % (save_dir, save_format))
    # plt.show()


def plot_pusch_power(ax, path, save_enabled, save_dir, save_format):
    mob_0 = pd.read_csv('%s/uav-1-puschTxPower-info.txt' % path, delimiter='\t').to_numpy()
    # plt.figure(figsize=(16, 9))
    ax.scatter(mob_0[:, 0], mob_0[:, 3])
    # ax.set_xlabel('Time (second)')
    ax.set_ylabel('PUSCH TX Power')
    if (save_enabled):
        plt.savefig('%s/puschTxPower.%s' % (save_dir, save_format))
    # plt.show()


def plot_srs_power(ax, path, save_enabled, save_dir, save_format):
    mob_0 = pd.read_csv('%s/uav-1-srsTxPower-info.txt' % path, delimiter='\t').to_numpy()
    # plt.figure(figsize=(16, 9))
    ax.scatter(mob_0[:, 0], mob_0[:, 3])
    # ax.set_xlabel('Time (second)')
    ax.set_ylabel('SRS TX Power')
    if (save_enabled):
        plt.savefig('%s/srsTxPower.%s' % (save_dir, save_format))
    # plt.show()
