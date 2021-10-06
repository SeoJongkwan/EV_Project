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

mt_info = sequence_mt(original_file)
mt_info['RegDt'] = pd.to_datetime(mt_info['RegDt'], format='%Y-%m-%d %H:%M:%S')

mt_info['mt'].unique()
mt_info['exp'].value_counts()

def ds_charging(df, mt):
    status_df = df[df['mt'] == mt].reset_index(drop=True)
    print("{} / mt: {}".format(status_df['exp'][0], mt))
    cnt = status_df.groupby(status_df['RegDt'].dt.strftime('%m-%d'))['RegDt'].count()
    cnt1 = cnt.to_frame()
    ax = cnt1.plot(kind='bar', figsize=(6, 3), color='salmon', zorder=3)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.get_legend().remove()
    plt.title("{} / mt: {}".format(status_df['exp'][0], mt), fontdict={'size':'medium'})
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.xlabel("RegDt", fontdict={'size':'small'})
    plt.ylabel("count", fontdict={'size':'small'})
    plt.grid(True, axis='y', linestyle='dashed')
    plt.tight_layout()
    plt.show()
    return cnt1


# status_df = mt_info[mt_info['mt'] == '16'].reset_index(drop=True)
# print("mt: {} / {}".format('16', status_df['exp'][0]))
# cnt = status_df.groupby(status_df['RegDt'].dt.strftime('%m-%d %H'))['RegDt'].count()
# cnt1 = cnt.to_frame()

ds_charging(mt_info, '16')
ds_charging(mt_info, '05')
