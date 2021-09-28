import pandas as pd
import argparse
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import statistics as stat       #statistics function module

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

dsr_file = pd.read_csv(args.data_path + "dc_100kW_dsr.csv")
dsr_ack_file = pd.read_csv(args.data_path + "dc_100kW_dsr_ack.csv")
csr_file = pd.read_csv(args.data_path + "dc_100kW_csr.csv")
csr_ack_file = pd.read_csv(args.data_path + "dc_100kW_csr_ack.csv")

dsr_cols = ['RegDt', 'ChargerId', 'DeviceStatus', 'AccessId', 'ChargerNumber']
dsr = dsr_file[dsr_cols]
dsr = dsr.copy()
dsr['RegDt'] = pd.to_datetime(dsr['RegDt'], format='%Y-%m-%d %H:%M:%S')

csr_cols = ['RegDt','ChargerId','ChargeCurrent','ChargeVoltage','AccumulatedWatt','ChargerNumber']
csr = csr_file[csr_cols]
csr = csr.copy()
csr['RegDt'] = pd.to_datetime(csr['RegDt'], format='%Y-%m-%d %H:%M:%S')

csr_ack_cols = ['RegDt','ChargerId','RequireWatt','ChargingFee']
csr_ack = csr_ack_file[csr_ack_cols]
csr_ack = csr_ack.copy()
csr_ack['RegDt'] = pd.to_datetime(csr_ack['RegDt'], format='%Y-%m-%d %H:%M:%S')

#delete NAN data
dsr = stat.check_nan_value(dsr)
csr = stat.check_nan_value(csr)
csr_ack = stat.check_nan_value(csr_ack)

dsr_status_cnt = stat.show_value_cnt(dsr, "DeviceStatus")
dsr_charging = dsr.loc[dsr['DeviceStatus'] == 'Charging'].reset_index(drop=True)

stat.show_density(csr, 'AccumulatedWatt')

t = csr.loc[csr['RegDt'].dt.month == 7]
stat.show_variable_relation(t, 'RegDt', 'ChargeCurrent', 'AccumulatedWatt')

stat.show_feature_correlation(csr, 'RegDt', 'AccumulatedWatt')