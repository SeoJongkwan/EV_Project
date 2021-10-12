import pandas as pd
import argparse
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import statistics as stat   #statistics function module
import chart                #chart function module


path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

dsr_file = pd.read_csv(args.data_path + "dc_100kW_dsr.csv")
dsr_ack_file = pd.read_csv(args.data_path + "dc_100kW_dsr_ack.csv")
csr_file = pd.read_csv(args.data_path + "dc_100kW_csr.csv")
csr_ack_file = pd.read_csv(args.data_path + "dc_100kW_csr_ack.csv")
ar_file = pd.read_csv(args.data_path + "dc_100kW_ar.csv")
user_file = pd.read_csv(args.data_path + 'dc_100kW_user.csv', encoding='UTF8')

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

#Device Status Code
print("\n-Device Status Type Count")
dsr_status_cnt = chart.show_value_cnt(dsr, "DeviceStatus")
#Device Status Code --> Error
ds_error = chart.show_device_status(dsr, 'Error')
ds_cable_error = chart.show_device_status(dsr, '충전케이블 연결오류')
ds_emergency = chart.show_device_status(dsr, '비상버튼 작동')

ds_cable_error['RegDt']

v = dsr[dsr["DeviceStatus"]=='충전케이블 연결오류']

t = stat.get_date(dsr, '202107211013', 13, 'min')
t1 = t[t['DeviceStatus']=='충전케이블 연결오류']

dsr_charging = dsr.loc[dsr['DeviceStatus'] == 'Charging'].reset_index(drop=True)


# chart.show_density(csr, 'AccumulatedWatt')

# t = csr.loc[csr['RegDt'].dt.month == 7]
# chart.show_variable_relation(t, 'RegDt', 'ChargeCurrent', 'AccumulatedWatt')

# chart.show_feature_correlation(csr, 'RegDt', 'AccumulatedWatt')



