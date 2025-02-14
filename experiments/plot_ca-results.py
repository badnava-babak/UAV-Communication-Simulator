import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# plt.style.use('Solarize_Light2')
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 30, })
plt.rcParams['axes.labelsize'] = 24
plt.rcParams['axes.titlesize'] = 24

dl_data = pd.read_csv(
    '/home/b502b586/edge-comp-workspace/ns-3-dev-git/build/utils/carrier_aggregation_results_dl_uav.txt',
    delimiter=' ', header=None).to_numpy()
ul_data = pd.read_csv(
    '/home/b502b586/edge-comp-workspace/ns-3-dev-git/build/utils/carrier_aggregation_results_ul_uav.txt',
    delimiter=' ', header=None).to_numpy().astype(np.float)

dl_data_noca = pd.read_csv(
    '/home/b502b586/edge-comp-workspace/ns-3-dev-git/build/utils/carrier_aggregation_results_dl_uav-noca.txt',
    delimiter=' ', header=None).to_numpy()
ul_data_noca = pd.read_csv(
    '/home/b502b586/edge-comp-workspace/ns-3-dev-git/build/utils/carrier_aggregation_results_ul_uav-noca.txt',
    delimiter=' ', header=None).to_numpy().astype(np.float)

print(dl_data)

dl_noca = dl_data_noca[np.where(dl_data_noca[:, 1] == 1)[0]]
dl_2ca = dl_data[np.where(dl_data[:, 1] == 2)[0]]
dl_3ca = dl_data[np.where(dl_data[:, 1] == 3)[0]]

dl_noca_dis0 = dl_noca[np.where(dl_noca[:, 3] == 0)[0]]
dl_noca_dis48 = dl_noca[np.where(dl_noca[:, 3] == 4800)[0]]
dl_noca_dis10k = dl_noca[np.where(dl_noca[:, 3] == 7000)[0]]

dl_2ca_dis0 = dl_2ca[np.where(dl_2ca[:, 3] == 0)[0]]
dl_2ca_dis48 = dl_2ca[np.where(dl_2ca[:, 3] == 4800)[0]]
dl_2ca_dis10k = dl_2ca[np.where(dl_2ca[:, 3] == 7000)[0]]

dl_3ca_dis0 = dl_3ca[np.where(dl_3ca[:, 3] == 0)[0]]
dl_3ca_dis48 = dl_3ca[np.where(dl_3ca[:, 3] == 4800)[0]]
dl_3ca_dis10k = dl_3ca[np.where(dl_3ca[:, 3] == 7000)[0]]

plt.figure(figsize=(16, 9))
# plt.plot(dl_noca_dis0[:, 0], dl_noca_dis0[:, 2] / 1000000, label='No Carrier Aggregation', marker='o', linewidth=8, markersize=16)
plt.plot(dl_noca_dis48[:, 0], dl_noca_dis48[:, 2] / 1000000, label='No Carrier Aggregation', marker='o', linewidth=8, markersize=16)
# plt.plot(dl_noca_dis10k[:, 0], dl_noca_dis10k[:, 2] / 1000000, label='No Carrier Aggregation', marker='o', linewidth=8, markersize=16)

# plt.plot(dl_2ca_dis0[:, 0], dl_2ca_dis0[:, 2] / 1000000, label='2 Component Carriers', marker='o', linewidth=8, markersize=16)
plt.plot(dl_2ca_dis48[:, 0], dl_2ca_dis48[:, 2] / 1000000, label='2 Component Carriers', marker='o', linewidth=8, markersize=16)
# plt.plot(dl_2ca_dis10k[:, 0], dl_2ca_dis10k[:, 2] / 1000000, label='2 Component Carriers', marker='o', linewidth=8, markersize=16)

# plt.plot(dl_2ca_dis48[:, 0], dl_2ca_dis48[:, 2] / 1000000, label='PR SDL 2 at 4.8 Km distance', marker='o', linewidth=8, markersize=16)
# plt.plot(dl_2ca_dis10k[:, 0], dl_2ca_dis10k[:, 2] / 1000000, label='PR SDL 2 at 10Km distance', marker='o', linewidth=8, markersize=16)

# plt.plot(dl_3ca_dis0[:, 0], dl_3ca_dis0[:, 2] / 1000000, label='3 Component Carriers', marker='o', linewidth=8, markersize=16)
plt.plot(dl_3ca_dis48[:, 0], dl_3ca_dis48[:, 2] / 1000000, label='3 Component Carriers', marker='o', linewidth=8, markersize=16)
# plt.plot(dl_3ca_dis10k[:, 0], dl_3ca_dis10k[:, 2] / 1000000, label='3 Component Carriers', marker='o', linewidth=8, markersize=16)

# plt.plot(dl_3ca_dis48[:, 0], dl_3ca_dis48[:, 2] / 1000000, label='PR SDL 3 at 4.8 Km distance')
# plt.plot(dl_3ca_dis10k[:, 0], dl_3ca_dis10k[:, 2] / 1000000, label='PR SDL 3 at 10 Km distance')

plt.title('Downlink')
plt.xlabel('Number of UAVs')
plt.ylabel('Throughput per UAV [Mbps]')
plt.legend()
plt.tight_layout()

# plt.show()


ul_noca = ul_data_noca[np.where(ul_data_noca[:, 1] == 1)]
ul_2ca = ul_data[np.where(ul_data[:, 1] == 2)]
ul_3ca = ul_data[np.where(ul_data[:, 1] == 3)]

ul_noca_dis0 = ul_noca[np.where(ul_noca[:, 3] == 0)[0]]
ul_noca_dis48 = ul_noca[np.where(ul_noca[:, 3] == 4800)[0]]
ul_noca_dis10k = ul_noca[np.where(ul_noca[:, 3] == 7000)[0]]

ul_2ca_dis0 = ul_2ca[np.where(ul_2ca[:, 3] == 0)[0]]
ul_2ca_dis48 = ul_2ca[np.where(ul_2ca[:, 3] == 4800)[0]]
ul_2ca_dis10k = ul_2ca[np.where(ul_2ca[:, 3] == 7000)[0]]

ul_3ca_dis0 = ul_3ca[np.where(ul_3ca[:, 3] == 0)[0]]
ul_3ca_dis48 = ul_3ca[np.where(ul_3ca[:, 3] == 4800)[0]]
ul_3ca_dis10k = ul_3ca[np.where(ul_3ca[:, 3] == 7000)[0]]

plt.figure(figsize=(16, 9))
# plt.plot(ul_noca_dis0[:, 0], ul_noca_dis0[:, 2] / 1000000, label='No Carrier Aggregation', marker='o', linewidth=8, markersize=16)
plt.plot(ul_noca_dis48[:, 0], ul_noca_dis48[:, 2] / 1000000, label='No Carrier Aggregation', marker='o', linewidth=8, markersize=16)
# plt.plot(ul_noca_dis10k[:, 0], ul_noca_dis10k[:, 2] / 1000000, label='No Carrier Aggregation', marker='o', linewidth=8, markersize=16)

# plt.plot(ul_2ca_dis0[:, 0], ul_2ca_dis0[:, 2] / 1000000, label='2 Component Carriers', marker='o', linewidth=8, markersize=16)
plt.plot(ul_2ca_dis48[:, 0], ul_2ca_dis48[:, 2] / 1000000, label='2 Component Carriers', marker='o', linewidth=8, markersize=16)
# plt.plot(ul_2ca_dis10k[:, 0], ul_2ca_dis10k[:, 2] / 1000000, label='2 Component Carriers', marker='o', linewidth=8, markersize=16)

# plt.plot(ul_2ca_dis48[:, 0], ul_2ca_dis48[:, 2] / 1000000, label='PR SDL 2 at 4.8 Km distance')
# plt.plot(ul_2ca_dis10k[:, 0], ul_2ca_dis10k[:, 2] / 1000000, label='PR SDL 2 at 10Km distance')

# plt.plot(ul_3ca_dis0[:, 0], ul_3ca_dis0[:, 2] / 1000000, label='3 Component Carriers', marker='o', linewidth=8, markersize=16)
plt.plot(ul_3ca_dis48[:, 0], ul_3ca_dis48[:, 2] / 1000000, label='3 Component Carriers', marker='o', linewidth=8, markersize=16)
# plt.plot(ul_3ca_dis10k[:, 0], ul_3ca_dis10k[:, 2] / 1000000, label='3 Component Carriers', marker='o', linewidth=8, markersize=16)

# plt.plot(ul_3ca_dis48[:, 0], ul_3ca_dis48[:, 2] / 1000000, label='PR SDL 3 at 4.8 Km distance')
# plt.plot(ul_3ca_dis10k[:, 0], ul_3ca_dis10k[:, 2] / 1000000, label='PR SDL 3 at 10 Km distance')

plt.title('Uplink')
plt.xlabel('Number of UAVs')
plt.ylabel('Throughput per UAV [Mbps]')
plt.legend()
plt.tight_layout()


plt.show()

ul_2ca_3users = ul_2ca[np.where(ul_2ca[:, 0] == 3)[0]]
ul_2ca_6users = ul_2ca[np.where(ul_2ca[:, 0] == 6)[0]]
ul_2ca_9users = ul_2ca[np.where(ul_2ca[:, 0] == 9)[0]]
ul_2ca_12users = ul_2ca[np.where(ul_2ca[:, 0] == 12)[0]]
ul_2ca_15users = ul_2ca[np.where(ul_2ca[:, 0] == 15)[0]]

ul_3ca_3users = ul_3ca[np.where(ul_3ca[:, 0] == 3)[0]]
ul_3ca_6users = ul_3ca[np.where(ul_3ca[:, 0] == 6)[0]]
ul_3ca_9users = ul_3ca[np.where(ul_3ca[:, 0] == 9)[0]]
ul_3ca_12users = ul_3ca[np.where(ul_3ca[:, 0] == 12)[0]]
ul_3ca_15users = ul_3ca[np.where(ul_3ca[:, 0] == 15)[0]]

plt.figure()
# plt.plot(ul_2ca_3users[:, 3], ul_2ca_3users[:, 2] / 1000000, label='PR SDL 2 with 3 users')
# plt.plot(ul_2ca_6users[:, 3], ul_2ca_6users[:, 2] / 1000000, label='PR SDL 2 with 6 users')
# plt.plot(ul_2ca_9users[:, 3], ul_2ca_9users[:, 2] / 1000000, label='PR SDL 2 with 9 users')
# plt.plot(ul_2ca_12users[:, 3], ul_2ca_12users[:, 2] / 1000000, label='PR SDL 2 with 12 users')
plt.plot(ul_2ca_15users[:, 3], ul_2ca_15users[:, 2] / 1000000, label='PR SDL 2 with 15 users')

# plt.plot(ul_3ca_3users[:, 3], ul_3ca_3users[:, 2] / 1000000, label='PR SDL 3 with 3 users')
# plt.plot(ul_3ca_6users[:, 3], ul_3ca_6users[:, 2] / 1000000, label='PR SDL 3 with 6 users')
# plt.plot(ul_3ca_9users[:, 3], ul_3ca_9users[:, 2] / 1000000, label='PR SDL 3 with 9 users')
# plt.plot(ul_3ca_12users[:, 3], ul_3ca_12users[:, 2] / 1000000, label='PR SDL 3 with 12 users')
plt.plot(ul_3ca_15users[:, 3], ul_3ca_15users[:, 2] / 1000000, label='PR SDL 3 with 15 users')

plt.title('Uplink')
plt.xlabel('Distance [m]')
plt.ylabel('Throughput per UE [Mbps]')
plt.legend()

dl_2ca_3users = dl_2ca[np.where(dl_2ca[:, 0] == 3)[0]]
dl_2ca_6users = dl_2ca[np.where(dl_2ca[:, 0] == 6)[0]]
dl_2ca_9users = dl_2ca[np.where(dl_2ca[:, 0] == 9)[0]]
dl_2ca_12users = dl_2ca[np.where(dl_2ca[:, 0] == 12)[0]]
dl_2ca_15users = dl_2ca[np.where(dl_2ca[:, 0] == 15)[0]]

dl_3ca_3users = dl_3ca[np.where(dl_3ca[:, 0] == 3)[0]]
dl_3ca_6users = dl_3ca[np.where(dl_3ca[:, 0] == 6)[0]]
dl_3ca_9users = dl_3ca[np.where(dl_3ca[:, 0] == 9)[0]]
dl_3ca_12users = dl_3ca[np.where(dl_3ca[:, 0] == 12)[0]]
dl_3ca_15users = dl_3ca[np.where(dl_3ca[:, 0] == 15)[0]]

plt.figure()
# plt.plot(dl_2ca_3users[:, 3], dl_2ca_3users[:, 2] / 1000000, label='PR SDL 2 with 3 users')
# plt.plot(dl_2ca_6users[:, 3], dl_2ca_6users[:, 2] / 1000000, label='PR SDL 2 with 6 users')
# plt.plot(dl_2ca_9users[:, 3], dl_2ca_9users[:, 2] / 1000000, label='PR SDL 2 with 9 users')
# plt.plot(dl_2ca_12users[:, 3], dl_2ca_12users[:, 2] / 1000000, label='PR SDL 2 with 12 users')
plt.plot(dl_2ca_15users[:, 3], dl_2ca_15users[:, 2] / 1000000, label='PR SDL 2 with 15 users')

# plt.plot(dl_3ca_3users[:, 3], dl_3ca_3users[:, 2] / 1000000, label='PR SDL 3 with 3 users')
# plt.plot(dl_3ca_6users[:, 3], dl_3ca_6users[:, 2] / 1000000, label='PR SDL 3 with 6 users')
# plt.plot(dl_3ca_9users[:, 3], dl_3ca_9users[:, 2] / 1000000, label='PR SDL 3 with 9 users')
# plt.plot(dl_3ca_12users[:, 3], dl_3ca_12users[:, 2] / 1000000, label='PR SDL 3 with 12 users')
plt.plot(dl_3ca_15users[:, 3], dl_3ca_15users[:, 2] / 1000000, label='PR SDL 3 with 15 users')

plt.title('Down link')
plt.xlabel('Distance [m]')
plt.ylabel('Throughput per UE [Mbps]')
plt.legend()
plt.show()

# print(dl_2ca)
# print(dl_3ca)
