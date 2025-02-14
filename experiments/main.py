import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt



plt.rcParams.update({'font.size': 22, })



def plot_video_stats(video_0, plt_label):
    rx_rows = np.where(video_0[:, 1] == 'rx')
    tx_rows = np.where(video_0[:, 1] == 'tx')
    rx_info = video_0[rx_rows][:, [0, 2]]
    # second_indices = [np.where(np.array(rx_info[:, 0], dtype=int) == i) for i in range(300)]
    # t1 = np.array(rx_info[:, 0], dtype=int)
    tx_info = video_0[tx_rows][:, [0, 2]]
    rx_sum_rate = 8 * np.array([np.sum(rx_info[np.where(np.array(rx_info[:, 0], dtype=int) == i), 1]) for i in
                                range(int(np.max(rx_info[:, 0])))])
    tx_sum_rate = 8 * np.array([np.sum(tx_info[np.where(np.array(tx_info[:, 0], dtype=int) == i), 1]) for i in
                                range(int(np.max(tx_info[:, 0])))])

    # plt.scatter(np.arange(rx_sum_rate.shape[0]), rx_sum_rate / (2 ** 20), label='Rx (%s)' % plt_label)
    # plt.scatter(np.arange(tx_sum_rate.shape[0]), tx_sum_rate / (2 ** 20), label='Tx (%s)' % plt_label)

    window_size = 5

    rx_data = pd.Series(rx_sum_rate)
    windows = rx_data.rolling(window_size)
    rx_sum_rate = windows.mean()
    rx_data = pd.Series(rx_info[:, 0])
    windows = rx_data.rolling(window_size)
    rx_t = windows.mean()

    tx_data = pd.Series(tx_sum_rate)
    windows = tx_data.rolling(window_size)
    tx_sum_rate = windows.mean()
    tx_data = pd.Series(tx_info[:, 0])
    windows = tx_data.rolling(window_size)
    tx_t = windows.mean()

    plt.scatter(np.arange(rx_sum_rate.shape[0]), rx_sum_rate / (2 ** 20), label='Reception (%s)' % plt_label)
    plt.scatter(np.arange(tx_sum_rate.shape[0]), tx_sum_rate / (2 ** 20), label='Transmission (%s)' % plt_label)




video_0 = pd.read_csv('./exp-1/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_1 = pd.read_csv('simulations-results/wildfire-4/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_2 = pd.read_csv('simulations-results/wildfire-7/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_3 = pd.read_csv('simulations-results/wildfire-8/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_4 = pd.read_csv('simulations-results/wildfire-9/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_5 = pd.read_csv('simulations-results/wildfire-10/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_6 = pd.read_csv('simulations-results/wildfire-11/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_7 = pd.read_csv('simulations-results/wildfire-12/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_8 = pd.read_csv('simulations-results/wildfire-13/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_9 = pd.read_csv('simulations-results/wildfire-14/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_10 = pd.read_csv('simulations-results/wildfire-15/VideoPacketTrace.txt', delimiter='\t').to_numpy()
# video_11 = pd.read_csv('simulations-results/wildfire-16/VideoPacketTrace.txt', delimiter='\t').to_numpy()


plt.figure(figsize=(16, 9))

# plot_video_stats(video_0, '10 MHz')
# plot_video_stats(video_1, '100 MHz')
# plot_video_stats(video_2, '6 MHz')
# plot_video_stats(video_4, '6 MHz')
# plot_video_stats(video_3, '15 MHz RR')
# plot_video_stats(video_5, '50 MHz')
# plot_video_stats(video_6, '15 MHz')
# plot_video_stats(video_7, '15 MHz')
# plot_video_stats(video_8, '6 MHz')
# plot_video_stats(video_9[:int(240 * video_9.shape[0] / 300)], '1280x720')  # 6 mhz
# plot_video_stats(video_10, '6 MHz')
plot_video_stats(video_0, '800x600')  # 6 mhz

# t = int(250 * video_3.shape[0] / 300)
# plot_video_stats(video_3[:video_4.shape[0]], '15 MHz')

# plot_video_stats(video_5, '50 MHz')

plt.legend()
plt.xlabel('Time (second)')
plt.ylabel('Throughput (Mb/s)')
plt.tight_layout()
plt.show()
