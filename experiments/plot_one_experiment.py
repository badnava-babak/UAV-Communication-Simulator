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

base_path = '/home/b502b586/ardupilot-workspace/experiments'
# base_path = '/home/b502b586/ardupilot-workspace/experiments/archive-complex-wildfire-track'
os.chdir(base_path)

path = '%s/exp-f:700-bw:15-video:800p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt' % base_path
# path = '%s/exp-f:700-bw:75-video:1920p-fr:LteFfrSoftAlgorithm-pc:t-sched:FdMt' % base_path
path= '/home/b502b586/ardupilot-workspace/ns3-mavsdk/build/src/ardupilot/examples/'

save_dir = '%s/saved_results' % path
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

n_row = 12

fig, axs = plt.subplots(n_row, 1, figsize=(30, n_row * 9))
############################# Plotting transmission rate ###############################
plot_transmission_rate(axs[0], path, save_enabled, save_dir, save_format)

############################# Plotting Reception rate ###############################
plot_reception_rate(axs[1], path, save_enabled, save_dir, save_format)

############################# Plotting DL SINR ###############################


plot_dl_rsrp(axs[2], path, save_enabled, save_dir, save_format)
plot_dl_sinr(axs[3], path, save_enabled, save_dir, save_format)

plot_ul_sinr(axs[4], path, save_enabled, save_dir, save_format)

plot_ul_rx_mcs(axs[5], path, save_enabled, save_dir, save_format)
plot_ul_tx_mcs(axs[6], path, save_enabled, save_dir, save_format)

plot_ul_mac_stats(axs[7], path, save_enabled, save_dir, save_format)

# plot_trajectory(axs[8], path, save_enabled, save_dir, save_format)

plot_distance(axs[8], path, save_enabled, save_dir, save_format)
plot_pucch_power(axs[9], path, save_enabled, save_dir, save_format)
plot_pusch_power(axs[10], path, save_enabled, save_dir, save_format)
plot_srs_power(axs[11], path, save_enabled, save_dir, save_format)

# fig.tight_layout()

plt.savefig('%s/two-uavs.png' % (save_dir))
plt.show()
