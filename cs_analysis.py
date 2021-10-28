import matplotlib.pyplot as plt
import pandas as pd
import argparse
import os

from common import Data  # common module
import statistics as stat  # statistics  module
import chart  # chart  module

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help="path to input file")
args = parser.parse_args()

file = Data()
file_dic = {}

# charger dataframe declares global variance
for i in range(len(file.file_name)):
    globals()['charger_name{}'.format(i)] = file.file_name[i]
    file_dic['charger_name{}'.format(i)] = file.file_name[i]
    globals()['charger{}'.format(i)] = pd.read_csv(args.data_path + globals()['charger_name{}'.format(i)] + ".csv")
    globals()['charger{}'.format(i)] = stat.convert_datetime(globals()['charger{}'.format(i)])
    globals()['charger{}_seq'.format(i)] = stat.sequence_mt(globals()['charger{}'.format(i)])
print("charger list:\n", file_dic)

charger_no = 1
select_charger = file_dic['charger_name{}'.format(charger_no)]
print("select charger:", select_charger + "\n")

charger_seq = globals()['charger{}_seq'.format(charger_no)]


csr_cols = ['ChargerId', 'RegDt', 'ChargeCurrent', 'ChargeVoltage', 'AccumulatedWatt', 'ChargerNumber']
for i in range(len(file.file_name)):
    globals()['charger{}_csr'.format(i)] = pd.read_csv(args.data_path + globals()['charger_name{}'.format(i)] + "_csr.csv")
    globals()['charger{}_csr'.format(i)] = stat.convert_datetime(globals()['charger{}_csr'.format(i)])
    globals()['charger{}_csr'.format(i)] = globals()['charger{}_csr'.format(i)][csr_cols]
    globals()['charger{}_csr'.format(i)]['RegDt'] = pd.to_datetime(globals()['charger{}_csr'.format(i)]['RegDt'], format='%Y-%m-%d %H:%M:%S')

select_csr = pd.read_csv(args.data_path + select_charger + "_csr.csv")
select_csr = stat.convert_datetime(select_csr)
csr_cols = ['ChargerId', 'RegDt', 'ChargeCurrent', 'ChargeVoltage', 'AccumulatedWatt', 'ChargerNumber']
csr = select_csr[csr_cols]
csr = csr.copy()
csr['RegDt'] = pd.to_datetime(csr['RegDt'], format='%Y-%m-%d %H:%M:%S')


select_csr_ack = pd.read_csv(args.data_path + select_charger + "_csr_ack.csv")
select_csr_ack = stat.convert_datetime(select_csr_ack)
csr_ack_cols = ['RegDt', 'ChargerId', 'RequireWatt', 'ChargingFee']
csr_ack = select_csr_ack[csr_ack_cols]
csr_ack = csr_ack.copy()
csr_ack['RegDt'] = pd.to_datetime(csr_ack['RegDt'], format='%Y-%m-%d %H:%M:%S')

# delete NAN data
csr = stat.check_nan_value(csr)
csr_ack = stat.check_nan_value(csr_ack)


chart.show_density(csr, 'AccumulatedWatt')


# t = csr.loc[csr['RegDt'].dt.month == 9]
# chart.show_variable_relation(csr, 'RegDt', 'ChargeCurrent', 'AccumulatedWatt')

# chart.show_feature_correlation(csr, 'RegDt', 'AccumulatedWatt')


charger_seq['mt'].unique()
charger_seq['exp'].value_counts().sum()

# mag monthly, daily, hourly statistics
chart.show_msg_period_statistics(charger_seq, select_charger, '15')

# msg communication frequency
stat.show_value_cnt(charger_seq, 'exp')

# charger charging count
msg_ar_cnt = []
for i in range(len(file.file_name)):
    msg_ar_cnt.append(globals()['charger{}_seq'.format(i)]['exp'].value_counts()['Access Request'])
chart.show_access_request_freq(msg_ar_cnt, list(map(lambda x: x[:-14], file_dic.values())))

charger0_df = charger0_seq[charger0_seq['mt'] == '05'].reset_index(drop=True)
df0 = pd.DataFrame(charger0_df.groupby(charger0_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
charger1_df = charger1_seq[charger1_seq['mt'] == '05'].reset_index(drop=True)
df1 = pd.DataFrame(charger1_df.groupby(charger1_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
charger2_df = charger2_seq[charger2_seq['mt'] == '05'].reset_index(drop=True)
df2 = pd.DataFrame(charger2_df.groupby(charger2_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
charger3_df = charger3_seq[charger3_seq['mt'] == '05'].reset_index(drop=True)
df3 = pd.DataFrame(charger3_df.groupby(charger3_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
charger4_df = charger4_seq[charger4_seq['mt'] == '05'].reset_index(drop=True)
df4 = pd.DataFrame(charger4_df.groupby(charger4_df['RegDt'].dt.strftime('%m'))['RegDt'].count())


df11 = pd.concat([df0, df1], axis=1)
df12 = pd.concat([df11, df2], axis=1)
df13 = pd.concat([df12, df3], axis=1)
df14 = pd.concat([df13, df4], axis=1)
df14.columns =  [charger_name0[:-14], charger_name1[:-14], charger_name2[:-14], charger_name3[:-14], charger_name4[:-14]]

df14