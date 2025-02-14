import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

import numpy as np
import os

import subprocess
from subprocess import Popen

valid_frequencies = ["700", "1500", "2600"]
valid_bw = ["6", "15", "25", "50", "75", "100"]
valid_scenarios = ["UMa", "UMi", "RMa"]
valid_video_qualities = ["800p", "1280p", "1920p"]
valid_fr_algs = ["ns3::LteFrNoOpAlgorithm", "ns3::LteFrHardAlgorithm", "ns3::LteFrStrictAlgorithm",
                 "ns3::LteFrSoftAlgorithm", "ns3::LteFfrSoftAlgorithm", "ns3::LteFfrEnhancedAlgorithm"]


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


def extract_loc_data(mob_0):
    node_0_data = mob_0[np.argwhere(mob_0[:, 1] == 0)[:, 0]]
    node_0_loc = np.array([r.split(':') for r in node_0_data[:, 2]], dtype=float)
    node_0_t = node_0_data[:, 0]
    return node_0_t, node_0_loc

import haversine as hs
from haversine import Unit

def get_distanc(node_0_loc, bs_loc):
    dis = np.array([hs.haversine(node_0_loc[p, :2], bs_loc[p], unit=Unit.KILOMETERS) for p in range(node_0_loc.shape[0])])
    # diff = np.subtract(node_0_loc, node_0_loc[0])
    # diff2D = diff[:, :2] ** 2
    # diff2D = np.sum(diff2D, axis=1)
    # diff2D = np.sqrt(diff2D)
    return dis


def extract_dl_info(rma2000):
    t = rma2000[:, 0]
    rsrp = 10 * np.log10(rma2000[:, 4])
    sinr = 10 * np.log10(rma2000[:, 5])
    return t, rsrp, sinr


def extract_ul_sinr(rma2000):
    t = rma2000[:, 0]
    sinr = 10 * np.log10(rma2000[:, 4])
    return t, sinr


# os.chdir(experiment_path)

def extract_delay_data(telemetry_data):
    node_0_data = telemetry_data[np.argwhere(np.array(telemetry_data[:, 1], dtype=int) == 1)[:, 0]]
    node_0_delay = node_0_data[:, 4]
    node_0_t = node_0_data[:, 0]
    return node_0_t, node_0_delay
