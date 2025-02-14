import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 22, })

telmetry_1 = pd.read_csv('/home/b502b586/ardupilot-workspace/experiments/exp-f:700-bw:6/uav-1-telemetry-info.txt',
                         delimiter=',').to_numpy()


def extract_delay_data(telemetry_data):
    node_0_data = telemetry_data[np.argwhere(np.array(telemetry_data[:, 1], dtype=int) == 1)[:, 0]]
    node_0_delay = node_0_data[:, 4]
    node_0_t = node_0_data[:, 0]
    return node_0_t, node_0_delay

t, delay = extract_delay_data(telmetry_1)

plt.figure(figsize=(16, 9))

plt.scatter(t, delay, label='Telemetry Delay')

plt.legend()
plt.xlabel('Time (second)')
plt.ylabel('Delay (ms)')
plt.tight_layout()

plt.show()
