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

#충전기 선택
charger_no = 0
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
chart.show_msg_period_statistics(charger_seq, select_charger, '05')

# msg communication frequency
stat.show_value_cnt(charger_seq, 'exp')

# charger charging count: exp --> Access Request
msg_ar_cnt = []
for i in range(len(file.file_name)):
    msg_ar_cnt.append(globals()['charger{}_seq'.format(i)]['exp'].value_counts()['Access Request'])
# chart.show_access_request_freq(msg_ar_cnt, file_dic.values())

month_charging_cnt = []
for i in range(len(file.file_name)):
    globals()['charger{}_seq'.format(i)] = globals()['charger{}_seq'.format(i)][globals()['charger{}_seq'.format(i)]['exp'] == "Access Request"].reset_index(drop=True)
    month_charging_cnt.append((globals()['charger{}_seq'.format(i)].groupby(globals()['charger{}_seq'.format(i)]['RegDt'].dt.strftime('%m'))['RegDt'].count()))

month_charging = {}
aug = []
oct = []
nov = []
for i in month_charging_cnt:
    aug.append(i[0])
    oct.append(i[1])
    nov.append(i[2])

month_charging["September"] = aug
month_charging["October"] = oct
month_charging["November"] = nov

mm = chart.show_month_charging_cnt(month_charging, file_dic.values())


file_dic.values()
month = [8, 9]
def show_month_charging_cnt(data, name):
    df = pd.DataFrame(data, index=name)
    df['cnt'] = df['September'] + df['October']
    df = df.sort_values('cnt', ascending=False)
    df = df.drop('cnt', axis=1)
    df.plot(kind="bar", stacked=True, figsize=(8, 6))
    plt.title("월별 충전기 충전횟수")
    plt.ylabel('count')
    plt.grid(True, axis='y', linestyle='dashed', alpha=0.4)
    plt.legend(loc=1)
    plt.tight_layout()
    plt.show()
    return df


# hour_charging_cnt = []
# for i in range(len(file.file_name)):
#     globals()['charger{}_seq'.format(i)] = globals()['charger{}_seq'.format(i)][globals()['charger{}_seq'.format(i)]['exp'] == "Access Request"].reset_index(drop=True)
#     hour_charging_cnt.append((globals()['charger{}_seq'.format(i)].groupby(globals()['charger{}_seq'.format(i)]['RegDt'].dt.strftime('%h'))['RegDt'].count()))
#
# hour_charging = {}
# one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve = [], [], [], [], [], [], [], [], [], [], [], []
# for i in hour_charging_cnt:
#     one.append(i[0])
#     two.append(i[1])
#     three.append(i[0])
#     four.append(i[1])
#     five.append(i[0])
#     six.append(i[1])
#     seven.append(i[0])
#     eight.append(i[1])
#     nine.append(i[0])
#     ten.append(i[1])
#     eleven.append(i[0])
#     twelve.append(i[1])
#
# hour_charging["One"] = one
# hour_charging["Two"] = two
# hour_charging["Three"] = three
# hour_charging["Four"] = four
# hour_charging["Five"] = five
# hour_charging["Six"] = six
# hour_charging["Seven"] = seven
# hour_charging["Eight"] = eight
# hour_charging["Nine"] = nine
# hour_charging["Ten"] = ten
# hour_charging["Eleven"] = eleven
# hour_charging["Twelve"] = twelve
#
#
#
# def show_hour_charging_cnt(data, name):
#     df = pd.DataFrame(data, index=name)
#     df['cnt'] = df['One']+df['Two']+df['Three']+df['Four']+df['Five']+df['Six']+df['Seven']+df['Eight']+df['Nine']+df['Ten']+df['Eleven']+df['Twelve']
#     df = df.sort_values('cnt', ascending=False)
#     df = df.drop('cnt', axis=1)
#     df.plot(kind="barh", stacked=True, figsize=(8, 6))
#     plt.title("월별 충전기 충전횟수")
#     plt.ylabel('count')
#     plt.grid(True, axis='y', linestyle='dashed', alpha=0.4)
#     plt.legend(loc=1)
#     plt.tight_layout()
#     plt.show()
#     return df
#
# hh = show_hour_charging_cnt(hour_charging, file_dic.values())





# charger0_df = charger0_seq[charger0_seq['mt'] == '05'].reset_index(drop=True)
# df0 = pd.DataFrame(charger0_df.groupby(charger0_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
# charger1_df = charger1_seq[charger1_seq['mt'] == '05'].reset_index(drop=True)
# df1 = pd.DataFrame(charger1_df.groupby(charger1_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
# charger2_df = charger2_seq[charger2_seq['mt'] == '05'].reset_index(drop=True)
# df2 = pd.DataFrame(charger2_df.groupby(charger2_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
# charger3_df = charger3_seq[charger3_seq['mt'] == '05'].reset_index(drop=True)
# df3 = pd.DataFrame(charger3_df.groupby(charger3_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
# charger4_df = charger4_seq[charger4_seq['mt'] == '05'].reset_index(drop=True)
# df4 = pd.DataFrame(charger4_df.groupby(charger4_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
#
#
# df11 = pd.concat([df0, df1], axis=1)
# df12 = pd.concat([df11, df2], axis=1)
# df13 = pd.concat([df12, df3], axis=1)
# df14 = pd.concat([df13, df4], axis=1)
# df14.columns =  [charger_name0[:-14], charger_name1[:-14], charger_name2[:-14], charger_name3[:-14], charger_name4[:-14]]
#
