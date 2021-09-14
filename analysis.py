import pandas as pd
import argparse
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import statistics        #statistics function module


path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

dsr_file = pd.read_csv(args.data_path + "dc_100kW_dsr.csv")
csr_file = pd.read_csv(args.data_path + "dc_100kW_csr.csv")


dsr_cols = ['RegDt', 'ChargerId', 'DeviceStatus', 'AccessId', 'ChargerNumber']
dsr = dsr_file[dsr_cols]
dsr = dsr.copy()
dsr['RegDt'] = pd.to_datetime(dsr['RegDt'], format='%Y-%m-%d %H:%M:%S')

csr_cols = ['RegDt','ChargeCurrent','ChargeVoltage','AccumulatedWatt','ChargerNumber']
csr = csr_file[csr_cols]
csr = csr.copy()
csr['RegDt'] = pd.to_datetime(csr['RegDt'], format='%Y-%m-%d %H:%M:%S')


dsr = statistics.check_nan_value(dsr)
csr = statistics.check_nan_value(csr)


dsr_vc = statistics.show_value_cnt(dsr, "DeviceStatus")

dsr_charging = dsr.loc[dsr['DeviceStatus'] == 'Charging'].reset_index(drop=True)
