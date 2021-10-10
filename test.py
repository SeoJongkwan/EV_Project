import pandas as pd
import os
import argparse
import psycopg2
import configparser
import argparse
import csv
from common import Data
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from datetime import datetime
from dateutil.relativedelta import relativedelta


path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

# conf = configparser.ConfigParser()
# conf.read('info.init')
#
# dbname = conf.get('DB', 'dbname')
# host = conf.get('DB', 'host')
# user = conf.get('DB', 'user')
# password = conf.get('DB', 'password')
# port = conf.get('DB', 'port')
#
# print("<DB Info>")
# print("name:", dbname + "\nhost:", host + "\nport:", port)
#
# con = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
# cursor = con.cursor()

ar_file = pd.read_csv(args.data_path + "dc_100kW_ar.csv")
ar_cols = ['RegDt','ServerId','ChargerId','AccessId','RequireCurrent','RequireWatt','ChargingTime']
ar = ar_file[ar_cols]
ar = ar.copy()
ar['RegDt'] = pd.to_datetime(ar['RegDt'], format='%Y-%m-%d %H:%M:%S')

dsr_file = pd.read_csv(args.data_path + "dc_100kW_dsr.csv")
dsr_cols = ['RegDt', 'ChargerId', 'DeviceStatus', 'AccessId', 'ChargerNumber']
dsr = dsr_file[dsr_cols]
dsr = dsr.copy()
dsr['RegDt'] = pd.to_datetime(dsr['RegDt'], format='%Y-%m-%d %H:%M:%S')

csr_file = pd.read_csv(args.data_path + "dc_100kW_csr.csv")
csr_cols = ['RegDt','ChargerId','ChargeCurrent','ChargeVoltage','AccumulatedWatt','ChargerNumber']
csr = csr_file[csr_cols]
csr = csr.copy()
csr['RegDt'] = pd.to_datetime(csr['RegDt'], format='%Y-%m-%d %H:%M:%S')

original_file = pd.read_csv(args.data_path + "dc_100kW.csv")

user_file = pd.read_csv(args.data_path + 'dc_100kW_user.csv', encoding='UTF8')

file_name = "dc_100kW.csv"
common_obj = Data(args.data_path + file_name)

def sequence_mt(file):
    file1 = file.copy()
    file1['msg'] = file1['msg'].str.replace(' ', '')

    mt = []
    for type in file1['msg']:
        mt.append(type[18:20])
    file1['mt'] = mt

    msg_type = common_obj.msg_type()
    exp = []
    file1['exp'] = None
    for type in file1['mt']:
        if type in msg_type.keys():
            exp.append(msg_type[type][0])
    file1['exp'] = exp
    file2 = file1[['ChargerId','RegDt','mt','exp']]
    return file2

msg_sequence = sequence_mt(original_file)
msg_sequence['RegDt'] = pd.to_datetime(msg_sequence['RegDt'], format='%Y-%m-%d %H:%M:%S')

msg_sequence['mt'].unique()
msg_sequence['exp'].value_counts().sum()


#
# def ds_charging(df, mt, opt='day'):
#     status_df = df[df['mt'] == mt].reset_index(drop=True)
#     print("{} / mt: {}".format(status_df['exp'][0], mt))
#     cnt = pd.DataFrame()
#     if opt == 'month':
#         cnt = status_df.groupby(status_df['RegDt'].dt.strftime('%m'))['RegDt'].count()
#     elif opt == 'day':
#         cnt = status_df.groupby(status_df['RegDt'].dt.strftime('%m-%d'))['RegDt'].count()
#     elif opt == 'hour':
#         cnt = status_df.groupby(status_df['RegDt'].dt.strftime('%H'))['RegDt'].count()
#
#     cnt1 = cnt.to_frame()
#     ax = cnt1.plot(kind='bar', figsize=(6, 3), color='cornflowerblue', zorder=3)
#     ax.yaxis.set_major_locator(MaxNLocator(integer=True))
#     ax.get_legend().remove()
#     plt.title("{} - {}(0x{}) / by {}".format(status_df['ChargerId'][0], status_df['exp'][0], mt, opt), fontdict={'size':'medium'})
#     plt.xticks(fontsize=7)
#     plt.yticks(fontsize=7)
#     plt.xlabel("RegDt", fontdict={'size':'small'})
#     plt.ylabel("Count", fontdict={'size':'small'})
#     plt.grid(True, axis='y', linestyle='dashed')
#     plt.tight_layout()
#     plt.show()
#     return cnt1



def msg_period_statistics(df, mt):
    print("Access Request Communication\nmonthly, daily, hourly statistics\n")
    status_df = df[df['mt'] == mt].reset_index(drop=True)
    print("{} / mt: {}".format(status_df['exp'][0], mt))

    df1 = pd.DataFrame(status_df.groupby(status_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
    df2 = pd.DataFrame(status_df.groupby(status_df['RegDt'].dt.strftime('%m-%d'))['RegDt'].count())
    df3 = pd.DataFrame(status_df.groupby(status_df['RegDt'].dt.strftime('%H'))['RegDt'].count())

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8))
    sns.barplot(x=df1.index, y=df1['RegDt'], color='cornflowerblue', zorder=3, ax=ax1)
    sns.barplot(x=df2.index, y=df2['RegDt'], color='gold', zorder=3, ax=ax2)
    sns.barplot(x=df3.index, y=df3['RegDt'], color='plum', zorder=3, ax=ax3)

    ax1.set(xlabel="RegDt", ylabel="Count", title="monthly Count")
    ax2.set(xlabel="RegDt", ylabel="Count", title="by daily Count")
    ax3.set(xlabel="RegDt", ylabel="Count", title="by hourly Count")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.grid(True, axis='y', linestyle='dashed')
    ax2.grid(True, axis='y', linestyle='dashed')
    ax3.grid(True, axis='y', linestyle='dashed')
    fig.suptitle("{} - {}(0x{})".format(status_df['ChargerId'][0], status_df['exp'][0], mt))
    plt.tight_layout()
    plt.show()
    return df1, df2, df3


m = msg_period_statistics(msg_sequence, '05')[0]
d = msg_period_statistics(msg_sequence, '05')[1]
h = msg_period_statistics(msg_sequence, '05')[2]


msg_period_statistics(msg_sequence, '16')
msg_period_statistics(msg_sequence, '15')


# a = get_date(csr, '202107211013', 12, opt='min')
