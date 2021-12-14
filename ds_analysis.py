import pandas as pd
import argparse
import os
from common import Data         #common module
import statistics as stat       #statistics module
import chart                    #chart module

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help="path to input file")
args = parser.parse_args()

file = Data()

#충전기 선택
select_file = file.file_name[4]
print("Select File: {}".format(select_file))

dsr_file = pd.read_csv(args.data_path + select_file + "_dsr.csv")
dsr_ack_file = pd.read_csv(args.data_path + select_file + "_dsr_ack.csv")
dsr_file = stat.convert_datetime(dsr_file)
dsr_ack_file = stat.convert_datetime(dsr_ack_file)

dsr_cols = ['RegDt', 'ChargerId', 'DeviceStatus', 'AccessId', 'ChargerNumber']
dsr = dsr_file[dsr_cols]
dsr = dsr.copy()
dsr['RegDt'] = pd.to_datetime(dsr['RegDt'], format='%Y-%m-%d %H:%M:%S')

#delete NAN data
dsr = stat.check_nan_value(dsr)

#Device Status Code
print("\n-Device Status Type Ratio")
# dsr_status_cnt = chart.show_value_cnt(dsr, select_file, "DeviceStatus")
dsr_ratio = dsr['DeviceStatus'].value_counts().to_frame()
dsr_status_cnt = chart.show_device_status_ratio(select_file, dsr_ratio, 1)

# Device Status Code --> Error
# ds_error = chart.show_device_status(dsr, 'Error')
# ds_cable_error = chart.show_device_status(dsr, '충전케이블 연결오류')
# ds_emergency = chart.show_device_status(dsr, '비상버튼 작동')


# v = dsr[dsr["DeviceStatus"]=='충전케이블 연결오류']
#
# t = stat.get_date(dsr, '202107211013', 13, 'min')
# t1 = t[t['DeviceStatus']=='충전케이블 연결오류']
#
# dsr_charging = dsr.loc[dsr['DeviceStatus'] == 'Charging'].reset_index(drop=True)


# chart.show_density(csr, 'AccumulatedWatt')
#
# t = csr.loc[csr['RegDt'].dt.month == 7]
# chart.show_variable_relation(t, 'RegDt', 'ChargeCurrent', 'AccumulatedWatt')
#
# chart.show_feature_correlation(csr, 'RegDt', 'AccumulatedWatt')



